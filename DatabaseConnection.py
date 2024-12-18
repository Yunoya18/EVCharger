import mysql.connector
from mysql.connector import Error


class Database:
    def __init__(self):
        self.host = "sql12.freesqldatabase.com"
        self.user = "sql12742420"
        self.password = "AbCrurkfC5"
        self.database = "sql12742420"
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
            self.close_connection()
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
            self.close_connection()
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
            location_dict = {item[0]: (float(item[1]), float(item[2])) for item in location}
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
            self.close_connection()
    def editProfileDB(self,user_id,email,firstname,surname,hash_password,phone,picture_data):
        if self.connection is None or not self.connection.is_connected():
            self.test_connection()
        
        try:
            cursor = self.connection.cursor()
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
            self.close_connection()
    def getUserInfo(self, user_id):
        from User_Package import User
        if self.connection is None or not self.connection.is_connected():
            self.test_connection()
        try:
            user_list = []
            cursor = self.connection.cursor()
            if user_id:
                query = "SELECT * FROM user WHERE user_id = %s"
                cursor.execute(query, (user_id,))
                data_user = cursor.fetchone()
                user = User(*data_user)
                return user
            else:
                query = "SELECT * FROM user"
                cursor.execute(query)
                data_user = cursor.fetchall()
            for user in data_user:
                nuser = User(*user)
                user_list.append(nuser)
            return user_list
        except Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
            self.close_connection()
    def getbooking_same(self,booking_date,booking_time_start,booking_time_end,station_id):
        if self.connection is None or not self.connection.is_connected():
            self.test_connection()
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM history WHERE booking_date = %s AND (start_time = %s OR end_time = %s) AND status NOT IN ('completed','canceled') AND station_id = %s"
            cursor.execute(query, (booking_date,booking_time_start,booking_time_end,station_id,))
            databooking = cursor.fetchone()
            return databooking
        except Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
            self.close_connection()
    def CreateBooking(self,user_id,station_id,booking_time_start,booking_time_end,booking_date,code,status="pending"):
        if self.connection is None or not self.connection.is_connected():
            self.test_connection()
        try:
            cursor = self.connection.cursor()
            print(booking_time_start, booking_time_end)
            query = "INSERT INTO history (user_id,station_id,start_time,end_time,booking_date,codebooking,status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (user_id,station_id,booking_time_start,booking_time_end,booking_date,code,status,))
            self.connection.commit()
            print("INSERT history")
        except Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
            self.close_connection()
    def gethistory(self,user_id):
        from User_Package import Booking
        if self.connection is None or not self.connection.is_connected():
            self.test_connection()
        try:
            history = []
            cursor = self.connection.cursor()
            if user_id:
                query = "SELECT * FROM history WHERE user_id = %s"
                cursor.execute(query, (user_id,))
                databooking = cursor.fetchall()
            else:
                query = "SELECT * FROM history"
                cursor.execute(query)
                databooking = cursor.fetchall()
            for booking in databooking:
                nbooking = Booking(*booking)
                history.append(nbooking)
            return history
        except Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
            self.close_connection()
    def getBooking(self,booking_id):
        from User_Package import Booking
        from datetime import datetime
        if self.connection is None or not self.connection.is_connected():
            self.test_connection()
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM history WHERE history_id = %s"
            cursor.execute(query, (booking_id,))
            databooking = cursor.fetchone()
            time1 = datetime.strptime(str(databooking[4]), "%H:%M:%S").time()
            time2 = datetime.strptime(str(databooking[5]), "%H:%M:%S").time()
            nbooking = Booking(databooking[0],databooking[1],databooking[2],databooking[3],time1,time2,databooking[6],databooking[7],databooking[8],)
            return nbooking
        except Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
            self.close_connection()
    def UpdateBooking(self,booking_id,booking_time_start=None,booking_time_end=None,booking_date=None,status=None):
        if self.connection is None or not self.connection.is_connected():
            self.test_connection()
        try:
            cursor = self.connection.cursor()
            if booking_time_start and booking_time_end and booking_date:
                query = "UPDATE history SET start_time = %s, end_time = %s, booking_date = %s WHERE history_id = %s;"
                cursor.execute(query, (booking_time_start,booking_time_end,booking_date,booking_id,))
            else:
                query = "UPDATE history SET status = %s WHERE history_id = %s;"
                cursor.execute(query, (status, booking_id,))
            self.connection.commit()
        except Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
            self.close_connection()
    def UpdateBookingALL(self, today,timetoday):
        if self.connection is None or not self.connection.is_connected():
            self.test_connection()
        try:
            cursor = self.connection.cursor()
            query = "UPDATE history SET status = %s WHERE (booking_date < %s OR (booking_date = %s AND end_time < %s)) AND status NOT IN (%s,%s);"
            cursor.execute(query, ("canceled",today,today,timetoday,"completed","ended",))
            self.connection.commit()
            query = "UPDATE history SET status = %s WHERE (booking_date < %s OR (booking_date = %s AND end_time < %s)) AND status = %s;"
            cursor.execute(query, ("ended",today,today,timetoday,"completed",))
            self.connection.commit()
            print(today,timetoday)
        except Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
            self.close_connection()
    def updateStaionStatus(self, station_id):
        if self.connection is None or not self.connection.is_connected():
            self.test_connection()
        try:
            cursor = self.connection.cursor()
            query = "UPDATE ev_stations SET status = 'unavailable' WHERE station_id = %s"
            cursor.execute(query, (station_id,))
            self.connection.commit()
            return {"message": f"Station with ID {station_id} has been updated successfully."}
        except Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
            self.close_connection()
    def showHistory(self, user_id):
        if self.connection is None or not self.connection.is_connected():
            self.test_connection()
        try:
            cursor = self.connection.cursor()
            query = "SELECT e.station_name, h.payment_id, h.start_time, h.end_time, h.booking_date, h.status FROM history h JOIN ev_stations e USING(station_id) WHERE h.user_id = %s"
            cursor.execute(query, (user_id,))
            data = cursor.fetchall()
            return data
        except Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
            self.close_connection()
    def updateUserStatus(self, user_id):
        if self.connection is None or not self.connection.is_connected():
            self.test_connection()
        try:
            cursor = self.connection.cursor()
            query = "UPDATE user SET status = 'suspend' WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            self.connection.commit()
            return {"message": f"Station with ID {user_id} has been updated successfully."}
        except Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
            self.close_connection()
    def getUserWithCancel(self):
        if self.connection is None or not self.connection.is_connected():
            self.test_connection()
        try:
            cursor = self.connection.cursor()
            query = "SELECT user_id, username, COUNT(history.status) FROM history JOIN user USING (user_id) WHERE history.status = 'canceled' GROUP BY user_id ORDER BY COUNT(history.status) DESC LIMIT 5"
            cursor.execute(query)
            data = cursor.fetchall()
            return data
        except Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
            self.close_connection()
