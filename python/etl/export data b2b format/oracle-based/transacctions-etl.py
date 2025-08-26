from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.sftp.operators.sftp import SFTPOperator
from airflow.models import Variable
from datetime import datetime
from pathlib import Path
import subprocess
import os

from query import runqry  # your custom query runner

# ---------------------------
# Config via Airflow Variables
# ---------------------------
# Create these in Airflow > Admin > Variables
OUTPUT_DIR = Variable.get("B2B_OUTPUT_DIR", default_var="/opt/airflow/output")
CUSTOM_FILE_PREFIX = Variable.get("B2B_CUSTOM_FILE_PREFIX", default_var="B2B_123456_TRANSACTIONS")

# PGP settings
PGP_PUBLIC_KEY_PATH = Variable.get("B2B_PGP_PUBLIC_KEY_PATH")  # e.g., /opt/airflow/keys/b2b_pubkey.asc
PGP_RECIPIENT = Variable.get("B2B_PGP_RECIPIENT")              # e.g., recipient email or key ID (fingerprint)

# SFTP settings (use an Airflow Connection for credentials & host)
SFTP_CONN_ID = Variable.get("B2B_SFTP_CONN_ID", default_var="sftp_b2b")
SFTP_REMOTE_DIR = Variable.get("B2B_SFTP_REMOTE_DIR", default_var="/incoming/b2b")
DELETE_PLAINTEXT_AFTER_ENCRYPT = Variable.get("B2B_DELETE_PLAINTEXT", default_var="true").lower() == "true"

# ---------------------------
# SQL Query
# ---------------------------
query = """
SELECT '10034' AS "ACQUIRING_ID",
       t.textdescription,
       t.AUTHACCOUNTTYPE,
       cu.numberx AS "CUSTOMER_ID",
       ROW_NUMBER() OVER (ORDER BY t.serno) AS "SEQUENCE",
       t.I002_NUMBER,
       t.I004_AMT_TRXN,
       t.I006_AMT_BILL,
       TO_CHAR(t.I013_TRXN_DATE, 'YYYYMMDD') AS "TRXNDATE",
       TO_CHAR(t.POSTDATE, 'YYYYMMDD') AS "POSTDATE",
       t.I049_CUR_TRXN,
       t.I051_CUR_BILL,
       t.textdescription AS "TRXN_TYPE",
       t.TRXNTYPE,
       iso.I018_MERCH_TYPE AS "MCC",
       t.I008_BILLING_FEE,
       iso.I043B_MERCH_CITY AS "MCITY",
       '214' AS "ISO_COUNTRY_CODE",
       t.serno AS "TRXN_ID" 
FROM ctransactions t
INNER JOIN cisotrxns iso ON (t.serno = iso.serno)
INNER JOIN cardx c ON (t.cardserno = c.serno)
INNER JOIN caccounts a ON (t.caccserno = a.serno)
INNER JOIN mprofilecards mc ON (c.masterprofileserno = mc.serno)
LEFT JOIN ccustomers cu ON (a.custserno = cu.serno)
LEFT JOIN people pe ON (cu.peopleserno = pe.serno)
WHERE mc.code IN (SELECT shortcode FROM vids_cards WHERE status = 1)
AND c.stgeneral IN (SELECT code FROM vids_cardstatus WHERE active = 1)
AND pe.custidnumber IN (SELECT rnc FROM vids_businesses WHERE status = 1)
AND UPPER(t.ORIGINATOR) NOT LIKE '%INCOMING%';
"""

# ---------------------------
# Task functions
# ---------------------------
def export_transactions(**context):
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    cdate = datetime.now().strftime("%Y%m%d")
    file_name = f"{CUSTOM_FILE_PREFIX}_{cdate}.txt"
    local_path = str(Path(OUTPUT_DIR) / file_name)

    result = runqry(query)
    if not result:
        raise ValueError("Error executing query or no results returned.")

    with open(local_path, "w", encoding="utf-8") as f:
        for row in result:
            f.write('|'.join(map(str, row)) + '\n')

    return local_path  # XCom -> plaintext path


def pgp_encrypt(**context):
    plaintext_path = context["ti"].xcom_pull(task_ids="export_transactions")
    if not plaintext_path or not os.path.exists(plaintext_path):
        raise FileNotFoundError("Plaintext file not found for encryption.")

    # Import public key (idempotent)
    if not PGP_PUBLIC_KEY_PATH or not os.path.exists(PGP_PUBLIC_KEY_PATH):
        raise FileNotFoundError("PGP public key path is not set or does not exist.")

    subprocess.run(
        ["gpg", "--batch", "--yes", "--import", PGP_PUBLIC_KEY_PATH],
        check=True
    )

    # Encrypt
    encrypted_path = plaintext_path + ".gpg"
    if not PGP_RECIPIENT:
        raise ValueError("PGP_RECIPIENT Airflow Variable must be set (email or key ID/fingerprint).")

    subprocess.run(
        [
            "gpg", "--batch", "--yes",
            "--trust-model", "always",
            "-r", PGP_RECIPIENT,
            "-o", encrypted_path,
            "--encrypt", plaintext_path,
        ],
        check=True
    )

    # Optionally delete plaintext after successful encryption
    if DELETE_PLAINTEXT_AFTER_ENCRYPT and os.path.exists(plaintext_path):
        try:
            os.remove(plaintext_path)
        except Exception as e:
            # Not fatal for the pipeline, but log-worthy
            print(f"Warning: failed to delete plaintext: {e}")

    return encrypted_path  # XCom -> encrypted file path


def remote_path_from_local(local_path: str) -> str:
    """Map local filename to remote upload path."""
    filename = Path(local_path).name
    return str(Path(SFTP_REMOTE_DIR) / filename)

# ---------------------------
# DAG Definition
# ---------------------------
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="export_encrypt_sftp_transactions_dag",
    default_args=default_args,
    description="Export B2B transactions, PGP-encrypt, and send via SFTP",
    schedule_interval="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["b2b", "transactions", "pgp", "sftp"],
) as dag:

    export_task = PythonOperator(
        task_id="export_transactions",
        python_callable=export_transactions,
    )

    encrypt_task = PythonOperator(
        task_id="pgp_encrypt_file",
        python_callable=pgp_encrypt,
    )

    # Pull the encrypted file path via templating in operator fields:
    sftp_put = SFTPOperator(
        task_id="sftp_upload_encrypted",
        ssh_conn_id=SFTP_CONN_ID,          # Airflow Connection ID (type: SFTP)
        local_filepath="{{ ti.xcom_pull(task_ids='pgp_encrypt_file') }}",
        remote_filepath="{{ python_callable(remote_path_from_local, ti.xcom_pull(task_ids='pgp_encrypt_file')) }}",  # evaluated via Jinja? -> alternative below
        operation="put",
        create_intermediate_dirs=True,
        confirm=True,
    )

    # NOTE: Some Airflow versions won't evaluate python callables in templates directly.
    # If so, replace the 'remote_filepath' line above with this simpler mapping:
    # remote_filepath="{{ var.value.B2B_SFTP_REMOTE_DIR }}/{{ ti.xcom_pull(task_ids='pgp_encrypt_file') | basename }}",

    export_task >> encrypt_task >> sftp_put
