from conn import initialize

def runqry(query, commit=False):
    #"""
    #Execute a SQL query on Oracle and optionally commit changes
    #"""
    connection = initialize()
    if connection is None:
        print("Connection to Oracle failed.")
        return None

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            if commit:
                connection.commit()
            rows = cursor.fetchall()
            return rows
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        if connection:
            connection.close()
            print("Connection closed.")
