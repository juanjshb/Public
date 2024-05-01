from query import runqry
from datetime import datetime

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

# Generate current date in YYYYMMDD format
current_date = datetime.now().strftime("%Y%m%d")

# Prompt user for custom file name
custom_file_name = input("Enter custom file name (without extension): ")

result = runqry(query)

if result:
    file_name = f"{custom_file_name}_{current_date}.txt"
    with open(file_name, "w") as f:
        for row in result:
            f.write(','.join(map(str, row)) + '\n')
    print(f"Query results exported to {file_name}")
else:
    print("Error executing query.")
