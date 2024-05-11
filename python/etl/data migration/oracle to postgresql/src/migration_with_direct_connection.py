import requests
from ora_conn import OracleConnection
from postgres_conn import PostgresConnection

# Function to fetch database credentials from the API
def fetch_database_credentials(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            credentials = response.json()
            return credentials
        else:
            print("Failed to fetch database credentials from the API.")
            return None
    except Exception as e:
        print(f"Error occurred while fetching database credentials: {str(e)}")
        return None

# API URL to fetch database credentials
api_url = 'your_api_url_here'

# Fetch database credentials from the API
credentials = fetch_database_credentials(api_url)
if credentials:
    # Extract Oracle and PostgreSQL credentials
    oracle_credentials = credentials.get('oracle', {})
    postgres_credentials = credentials.get('postgres', {})

    # Connect to Oracle database
    oracle_conn = OracleConnection(**oracle_credentials)
    oracle_conn.connect()

    # Connect to PostgreSQL database
    postgres_conn = PostgresConnection(**postgres_credentials)
    postgres_conn.connect()

    # Fetch data from Oracle and insert into PostgreSQL
    oracle_cursor = oracle_conn.connection.cursor()
    postgres_cursor = postgres_conn.connection.cursor()

    oracle_cursor.execute("SELECT * FROM your_oracle_table")
    for row in oracle_cursor:
        # Assuming your PostgreSQL table has the same schema as the Oracle table
        postgres_cursor.execute("INSERT INTO your_postgres_table VALUES (%s, %s, ...)", row)

    # Commit changes and close connections
    postgres_conn.connection.commit()
    postgres_cursor.close()
    postgres_conn.close()
    oracle_cursor.close()
    oracle_conn.close()

else:
    print("Database credentials could not be fetched. Exiting...")
