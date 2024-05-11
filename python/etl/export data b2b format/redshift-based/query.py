from conn import create_connection

def runqry(query, commit=False):
    """
    Execute a SQL query on Redshift
    """
    connection = create_connection()
    if connection is None:
        print("Connection to Redshift failed.")
        return

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            if commit:
                connection.commit()
            print("Query executed successfully!")
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        if connection:
            connection.close()
            print("Connection closed.")
