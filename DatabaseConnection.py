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
    def getALLStation(self):
        from User_Package import Station
        if self.connection is None or not self.connection.is_connected():
            self.test_connection()
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM ev_stations"
            cursor.execute(query)
            allstation = cursor.fetchall()
            query = "SELECT * FROM locations"
            cursor.execute(query)
            location = cursor.fetchall()
            location_dict = {item[0]: (float(item[1]), float(item[1])) for item in location}
            list_allstaion = []
            for data in allstation:
                address = location_dict.get(data[1], "No location")
                station = Station(data[1],address[0],address[1],data[0],data[2],data[3],float(data[4]))
                list_allstaion.append(station)
            return list_allstaion
        except Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
    
    def editProfileDB(self,user_id,email,firstname,surname,hash_password,phone,picture_data):
        if self.connection is None or not self.connection.is_connected():
            self.test_connection()
        
        try:
            cursor = self.connection.cursor()
            query = "UPDATE user SET firstname = %s, surname = %s, password = %s,email = %s, phone = %s, profile = %s WHERE user_id = %s;"
            cursor.execute(query, (firstname,surname,hash_password,email,phone,picture_data,user_id,))
            self.connection.commit()
            return 0
        except Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()

    def getUserInfo(self, user_id):
        from User_Package import User
        if self.connection is None or not self.connection.is_connected():
            self.test_connection()
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM user WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            data_user = cursor.fetchone()
            user = User(*data_user)
            return user
        except Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()