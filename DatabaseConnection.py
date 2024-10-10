import mysql.connector

class db:
    def __init__(self):
        self.host = "sql12.freesqldatabase.com"
        self.user = "sql12736570"
        self.password = "BDNeWGZ58K"
        self.database = "sql12736570"

    def test_connection(self):
            try:
                connection = mysql.connector.connect(
                    host = self.host,
                    user = self.user,
                    password = self.password,
                    database = self.database)
                cursor = connection.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                print(result)
            except mysql.connector.Error as err:
                print("AAAAAAAAAAAAAAAAAAAAAAAA")

