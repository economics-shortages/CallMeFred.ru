import pymysql.cursors
import os

class Connection:
    def __init__(self) -> None:
        self.DB = os.environ.get('MYSQL_DATABASE')
        self.PORT = int(os.environ.get('MYSQL_PORT')) or 3306;
        self.HOST = os.environ.get('MYSQL_HOST')
        self.USER = os.environ.get('MYSQL_USER')
        self.PASS = os.environ.get('MYSQL_PASSWORD')

    def connect(self):
        return pymysql.connect(host=self.HOST,
                        port=self.PORT,
                        user=self.USER,
                        password=self.PASS,
                        database=self.DB,
                        cursorclass=pymysql.cursors.DictCursor)

    def __enter__(self):
        self.connection = self.connect()
        return self.connection
    
    def __exit__(self):
        self.connection.close();
    
    