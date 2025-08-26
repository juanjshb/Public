from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from query import runqry  # your custom query runner

# ---------------------------
# Query
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
WHERE mc.code IN (SELECT shortcode FROM vids_cards WHERE status = 1) --- PERFILES DE TC PERMITIDOS
AND c.stgeneral IN (SELECT code FROM vids_cardstatus WHERE active = 1) ---- STATUS DE TC PERMITIDOS
AND pe.custidnumber IN (SELECT rnc FROM vids_businesses WHERE status = 1) --- RNC DE EMPRESAS
AND UPPER(t.ORIGINATOR) NOT LIKE '%INCOMING%';
"""

# ---------------------------
# Task function
# ---------------------------
def export_transactions(**context):
    cdate = datetime.now().strftime("%Y%m%d")
    custom_file_name = "B2B_123456_TRANSACTIONS"
    result = runqry(query)

    if not result:
        raise ValueError("Error executing query or no results returned.")

    file_name = f"{custom_file_name}_{cdate}.txt"
    with open(file_name, "w") as f:
        for row in result:
            f.write('|'.join(map(str, row)) + '\n')

    print(f"Query results exported to {file_name}")
    return file_name

# ---------------------------
# DAG Definition
# ---------------------------
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
}

with DAG(
    dag_id='export_transactions_dag',
    default_args=default_args,
    description='Run query and export B2B transactions to file',
    schedule_interval='@daily',  # change as needed
    start_date=datetime(2025, 1, 1),  # adjust start date
    catchup=False,
    tags=['b2b', 'transactions'],
) as dag:

    export_task = PythonOperator(
        task_id='export_transactions',
        python_callable=export_transactions,
        provide_context=True,
    )

    export_task
