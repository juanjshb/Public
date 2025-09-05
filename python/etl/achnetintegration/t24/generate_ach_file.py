from airflow import DAG
from airflow.providers.oracle.hooks.oracle import OracleHook
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime
import os

# Query de transacciones
SQL_TXNS = """
SELECT 
    FT.TRANSACTION_REF   AS TRANSACTION_ID,
    FT.DEBIT_ACCT_NO     AS SOURCE_ACCOUNT,
    FT.CREDIT_ACCT_NO    AS DEST_ACCOUNT,
    FT.AMOUNT            AS AMOUNT,
    FT.VALUE_DATE        AS VALUE_DATE,
    FT.BENEFICIARY_NAME  AS BENEF_NAME,
    B.ACH_CODE           AS DEST_BANK_CODE,
    FT.PAYMENT_DETAILS   AS COMMENT
FROM FBNK_FUNDS_TRANSFER FT
JOIN ACH_BANKS B 
    ON FT.CREDIT_BANK_ID = B.T24_BANK_ID
WHERE FT.VALUE_DATE = TRUNC(SYSDATE)
  AND FT.AUTHORIZED = 'Y'
"""

# Query de mapping con longitud
SQL_MAPPING = """
SELECT FIELD_NAME, START_POS, LENGTH
FROM ACH_MAPPING
ORDER BY START_POS
"""

def export_ach_file(**context):
    hook = OracleHook(oracle_conn_id="t24_db")

    # Variables Airflow
    output_dir = Variable.get("ACH_OUTPUT_DIR", "/tmp")
    origin_bank_code = Variable.get("ACH_ORIGIN_BANK_CODE", "000000")

    # Leer mapping
    mapping_records = hook.get_records(SQL_MAPPING)
    mapping = {m[0].upper(): (m[1], m[2]) for m in mapping_records}

    # Leer transacciones
    records = hook.get_records(SQL_TXNS)

    fecha = datetime.now().strftime("%Y%m%d")
    filepath = os.path.join(output_dir, f"ach_{fecha}.txt")

    with open(filepath, "w", encoding="utf-8") as f:
        for row in records:
            txn = {
                "TRANSACTION_ID": row[0],
                "SOURCE_ACCOUNT": row[1],
                "DEST_ACCOUNT": row[2],
                "AMOUNT": f"{row[3]:.2f}",
                "VALUE_DATE": row[4].strftime("%Y%m%d"),
                "BENEF_NAME": row[5],
                "DEST_BANK_CODE": row[6],
                "COMMENT": row[7] if row[7] else "",
                "ORIGIN_BANK_CODE": origin_bank_code
            }

            # Tamaño total de la línea = max(START_POS + LENGTH - 1)
            line_size = max(start + length - 1 for (_, (start, length)) in mapping.items())
            line = [" "] * line_size

            for field, (start, length) in mapping.items():
                value = str(txn.get(field, ""))
                value_fmt = value.ljust(length)[:length]
                line[start-1:start-1+length] = value_fmt

            f.write("".join(line) + "\n")

    print(f"Archivo generado: {filepath}")

# Definición del DAG
with DAG(
    dag_id="generate_ach_file",
    default_args={"start_date": datetime(2023, 1, 1)},
    schedule_interval="@daily",  # o "0 6 * * 1-5"
    catchup=False,
    tags=["t24", "ach", "etl"]
) as dag:

    task_generate = PythonOperator(
        task_id="export_ach_file",
        python_callable=export_ach_file,
        provide_context=True
    )

    task_generate
