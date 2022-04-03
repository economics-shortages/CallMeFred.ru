from parser.core.db.connection import Connection

class Connections:
    connection = None
    
    @classmethod
    def get_connection(cls, new:bool = False):
        if new or not cls.connection:
            cls.connection = Connection().connect()
        return cls.connection;

    @classmethod
    def query(cls, query, vars: tuple = ()):
        connection = cls.get_connection()

        try:
            cursor = connection.cursor()
        except pyodbc.ProgrammingError:
            connection = cls.get_connection(new=True)
            cursor = connection.cursor()
        cursor.execute(query, vars)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    @classmethod
    def query_single(cls, query, vars: tuple = ()):
        connection = cls.get_connection()

        try:
            cursor = connection.cursor()
        except pyodbc.ProgrammingError:
            connection = cls.get_connection(new=True)
            cursor = connection.cursor()
        cursor.execute(query, vars)
        result = cursor.fetchone()
        cursor.close()
        return result
    
    @classmethod
    def query_insert(cls, query, vars: tuple = ()):
        connection = cls.get_connection()

        try:
            cursor = connection.cursor()
        except pyodbc.ProgrammingError:
            connection = cls.get_connection(new=True)
            cursor = connection.cursor()
        cursor.execute(query, vars)
        connection.commit()
        inserted = cls.query_single('SELECT LAST_INSERT_ID() as id;', ())
        return inserted

        