import mysql.connector
from mysql.connector import Error
from configparser import ConfigParser

class MySQLConnection:
    @staticmethod
    def load_config(config_path='../config.ini'):
        config = ConfigParser()
        config.read(config_path)
        db_config = config['MYSQL']
        return {
            'host': db_config.get('host', 'localhost'),
            'port': db_config.getint('port', 3306),
            'user': db_config.get('user', 'root'),
            'password': db_config.get('password', ''),
            'database': db_config.get('database', '')
        }

    @staticmethod
    def connect(config_path='config.ini'):
        try:
            config = MySQLConnection.load_config(config_path)
            connection = mysql.connector.connect(**config)
            if connection.is_connected():
                #print("Connection successful!")
                return connection
            return None
        except Error as e:
            #print(f"Connection error: {e}")
            return None

    @staticmethod
    def close(connection):
        if connection and connection.is_connected():
            connection.close()
            #print("Connection closed.")
