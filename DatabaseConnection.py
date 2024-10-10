import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.host = "sql12.freesqldatabase.com"
        self.user = "sql12736570"
        self.password = "BDNeWGZ58K"
        self.database = "sql12736570"
        self.connection = None

    def test_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Connection successful!")
                return True
        except Error as err:
            print(f"Error: {err}")
            return False

    def insert_user(self, username: str, email: str, password: str):
        if self.connection is None or not self.connection.is_connected():
            self.test_connection()

        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO user (username, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, email, password))
            self.connection.commit()
            print("User registered successfully!")
        except Error as err:
            print(f"Error: {err}")
            return False  # Indicate failure
        finally:
            cursor.close()
        return True  # Indicate success

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")

    def validate_user(self, username: str, password: str):
        if self.connection is None or not self.connection.is_connected():
            self.test_connection()

        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM user WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            return user  # Returns user info if found, otherwise None
        except Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()

