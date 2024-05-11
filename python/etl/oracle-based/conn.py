import cx_Oracle

def initialize():
    #"""
    #Create a connection to Oracle
    #"""
    try:
        connection = cx_Oracle.connect(
            user="your_username",
            password="your_password",
            dsn="localhost:1521/SERVICENAME"
        )
        return connection
    except cx_Oracle.Error as e:
        print(f"Error connecting to Oracle: {e}")
        return None
