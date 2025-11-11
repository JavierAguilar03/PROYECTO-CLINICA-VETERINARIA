import mysql.connector 
from mysql.connector import Error
import sys
import os
from typing import Optional, Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..')))



class DatabaseConnection:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection: Optional[mysql.connector.connection.MySQLConnection] = None

    def connect(self) -> bool:
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return self.connection.is_connected()
        except Error:
            return False

    def disconnect(self) -> None:
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def execute_query(self, query: str, params: Optional[tuple] = None) -> bool:
        if not self.connection or not self.connection.is_connected():
            raise ConnectionError("Database not connected")
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
            return True
        except Error:
            self.connection.rollback()
            return False
        finally:
            cursor.close()

    def fetch_one(self, query: str, params: Optional[tuple] = None) -> Optional[Any]:
        if not self.connection or not self.connection.is_connected():
            raise ConnectionError("Database not connected")
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        return result

    def validate_user(self, username: str, password: str) -> bool:
        if not self.connection or not self.connection.is_connected():
            raise ConnectionError("Database not connected")
        query = """
            SELECT * FROM empleados
            WHERE usuario = %s AND contraseña = %s
        """
        result = self.fetch_one(query, (username, password))
        return result is not None
