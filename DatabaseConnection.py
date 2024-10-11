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
            print(bool(user_id),bool(email),bool(firstname),bool(surname),bool(hash_password),bool(phone),bool(picture_data))
            if (firstname):
                query = "UPDATE user SET firstname = %s WHERE user_id = %s;"
                cursor.execute(query, (firstname,user_id,))
                self.connection.commit()
            if (surname):
                query = "UPDATE user SET surname = %s WHERE user_id = %s;"
                cursor.execute(query, (surname,user_id,))
                self.connection.commit()
            if (hash_password):
                query = "UPDATE user SET password = %s WHERE user_id = %s;"
                cursor.execute(query, (hash_password,user_id,))
                self.connection.commit()
            if (email):
                query = "UPDATE user SET email = %s WHERE user_id = %s;"
                cursor.execute(query, (email,user_id,))
                self.connection.commit()
            if (phone):
                query = "UPDATE user SET phone = %s WHERE user_id = %s;"
                cursor.execute(query, (phone,user_id,))
                self.connection.commit()
            if (picture_data):
                query = "UPDATE user SET profile = %s WHERE user_id = %s;"
                cursor.execute(query, (picture_data,user_id,))
                self.connection.commit()

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

    def getbooking_same(self,booking_date,booking_time_start,booking_time_end):
        if self.connection is None or not self.connection.is_connected():
            self.test_connection()
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM history WHERE booking_date = %s AND (start_time = %s OR end_time = %s) AND status NOT IN ('completed','canceled') "
            cursor.execute(query, (booking_date,booking_time_start,booking_time_end,))
            databooking = cursor.fetchone()
            return databooking
        except Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
    
    def CreateBooking(self,user_id,station_id,booking_time_start,booking_time_end,booking_date,code,status="pending"):
        if self.connection is None or not self.connection.is_connected():
            self.test_connection()
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO history (user_id,station_id,start_time,end_time,booking_date,codebooking,status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (user_id,station_id,booking_time_start,booking_time_end,booking_date,code,status,))
            self.connection.commit()
            print("INSERT history")
        except Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()