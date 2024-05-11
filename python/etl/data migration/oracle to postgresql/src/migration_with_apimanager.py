import requests
import base64
import cx_Oracle
import psycopg2

# Function to fetch database credentials from the API
def fetch_database_credentials(api_url, account_id, api_key, api_secret):
    try:
        # Encode API key and secret for Authorization header
        credentials_encoded = base64.b64encode(f"{api_key}:{api_secret}".encode()).decode()

        # Prepare headers with Authorization
        headers = {
            "Authorization": f"Basic {credentials_encoded}",
            "Content-Type": "application/json"
        }

        # JSON payload for the API request
        payload = {
            "ACCUNTID": account_id,
            "APIKEY": api_key
        }

        # Make POST request to API
        response = requests.post(api_url, json=payload, headers=headers)
        if response.status_code == 200:
            credentials = response.json()
            return credentials
        else:
            print(f"Failed to fetch database credentials from the API. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error occurred while fetching database credentials: {str(e)}")
        return None

# Function to retrieve table structure from a database
def get_table_structure(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}'")
    return cursor.fetchall()

# Function to compare table structures
def compare_table_structures(oracle_structure, postgres_structure):
    if oracle_structure == postgres_structure:
        print("Table structures match.")
        return True
    else:
        print("Table structures do not match. Differences found.")
        return False

# API URL to fetch database credentials
api_url = 'https://connect.apimanager.test/creds/'

# API key, secret, and account ID
account_id = "TEST_ACCOUNT"
api_key = '1234567890'
api_secret = 'ABCDEFGHIJK'

# Fetch database credentials from the API
credentials = fetch_database_credentials(api_url, account_id, api_key, api_secret)
if credentials:
    # Extract Oracle and PostgreSQL credentials
    oracle_credentials = credentials.get('oracle', {})
    postgres_credentials = credentials.get('postgres', {})

    # Connect to Oracle database
    oracle_conn = cx_Oracle.connect(**oracle_credentials)
    oracle_cursor = oracle_conn.cursor()

    # Connect to PostgreSQL database
    postgres_conn = psycopg2.connect(**postgres_credentials)
    postgres_cursor = postgres_conn.cursor()

    # Table name to compare
    table_name = 'customers'

    # Retrieve table structures from Oracle and PostgreSQL
    oracle_table_structure = get_table_structure(oracle_conn, table_name)
    postgres_table_structure = get_table_structure(postgres_conn, table_name)

    # Compare table structures
    if compare_table_structures(oracle_table_structure, postgres_table_structure):
        # Fetch data from Oracle and insert into PostgreSQL
        oracle_cursor.execute(f"SELECT * FROM {table_name}")
        for row in oracle_cursor:
            postgres_cursor.execute(f"INSERT INTO {table_name} VALUES (%s, %s, ...)", row)

        # Commit changes and close connections
        postgres_conn.commit()
        postgres_cursor.close()
        postgres_conn.close()
        oracle_cursor.close()
        oracle_conn.close()
    else:
        print("Table structure mismatch. Please reconcile the differences before migrating data.")
else:
    print("Database credentials could not be fetched. Exiting...")
