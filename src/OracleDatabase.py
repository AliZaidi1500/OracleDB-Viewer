import cx_Oracle as cx

class OracleDatabase:

    def __init__(self):
        self.connection = self.cursor = None

    @property
    def version(self):
        return self.connection.version

    @property
    def host(self):
        return self.connection.dsn.split('HOST=')[1].split(')')[0]

    @property
    def username(self):
        return self.connection.username

    @property
    def isConnected(self):
        return self.connection is not None and self.cursor is not None

    def connect(self, host, port, sid, username, password):
        # Connect to the database
        self.connection = cx.connect(username, password, cx.makedsn(host, port, sid))
        self.cursor = self.connection.cursor()

    def disconnect(self):
        # Close the cursor and connection
        self.cursor.close()
        self.connection.close()
        self.connection = self.cursor = None

    def getTables(self):
        # Get the table names
        self.cursor.execute('SELECT table_name FROM user_tables')
        return [row[0] for row in self.cursor]

    def getViews(self):
        # Get the view names
        self.cursor.execute('SELECT view_name FROM user_views')
        return [row[0] for row in self.cursor]

    def getColumnData(self, table):
        # Get the table column names and data types
        self.cursor.execute(f'SELECT column_name, data_type, data_length FROM user_tab_columns WHERE table_name = \'{table}\'')
        return self.cursor.fetchall()
