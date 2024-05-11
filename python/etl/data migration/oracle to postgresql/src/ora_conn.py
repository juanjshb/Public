import cx_Oracle

class OracleConnection:
    def __init__(self, user, password, host, port, service):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.service = service
        self.connection = None

    def connect(self):
        dsn = cx_Oracle.makedsn(self.host, self.port, service_name=self.service)
        self.connection = cx_Oracle.connect(user=self.user, password=self.password, dsn=dsn)
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()

