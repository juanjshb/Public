from redshift_connector import connect

def create_connection():
    """
    Create a connection to Redshift
    """
    try:
        conn = connect(
            user="your_username",
            password="your_password",
            host="localhost",
            port="5439",
            database="your_database_name"
        )
        return conn
    except Exception as e:
        print(f"Error connecting to Redshift: {e}")
        return None
