import psycopg2

class PostgresConnection:
    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.connection = None

    def connect(self):
        self.connection = psycopg2.connect(user=self.user, password=self.password,
                                           host=self.host, port=self.port, database=self.database)
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()

