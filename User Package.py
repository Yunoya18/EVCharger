# Class User
class User:
    def __init__(self, user_id, email, password, firstname, surname, phone, profile, status):
        self.__user_id = user_id
        self.__email = email
        self.__password = password
        self.__firstname = firstname
        self.__surname = surname
        self.__phone = phone
        self.__profile = profile
        self.__status = status

    # Getter methods
    def get_user_id(self):
        return self.__user_id

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def get_firstname(self):
        return self.__firstname

    def get_surname(self):
        return self.__surname

    def get_phone(self):
        return self.__phone

    def get_profile(self):
        return self.__profile

    def get_status(self):
        return self.__status

    # Setter methods
    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

    def set_firstname(self, firstname):
        self.__firstname = firstname

    def set_surname(self, surname):
        self.__surname = surname

    def set_phone(self, phone):
        self.__phone = phone

    def set_profile(self, profile):
        self.__profile = profile

    def set_status(self, status):
        self.__status = status

# Class Location
class Location:
    def __init__(self, location_id, address):
        self.__location_id = location_id
        self.__address = address

    # Getter methods
    def get_location_id(self):
        return self.__location_id

    def get_address(self):
        return self.__address

    # Setter methods
    def set_address(self, address):
        self.__address = address
# Class Station
class Station(Location):
    def __init__(self, location_id, address, station_id, station_name, status, price_per_hour):
        super().__init__(location_id, address)
        self.__station_id = station_id
        self.__station_name = station_name
        self.__status = status
        self.__price_per_hour = price_per_hour

    # Getter methods
    def get_station_id(self):
        return self.__station_id

    def get_station_name(self):
        return self.__station_name

    def get_status(self):
        return self.__status

    def get_price_per_hour(self):
        return self.__price_per_hour

    # Setter methods
    def set_station_name(self, station_name):
        self.__station_name = station_name

    def set_status(self, status):
        self.__status = status

    def set_price_per_hour(self, price_per_hour):
        self.__price_per_hour = price_per_hour

# Class All_Station
class All_Station:
    def __init__(self):
        self.__station_list = self.getAllStation()
    
    def getAllStation(self):
        return [1,2,3] #เชื่อมดาต้าเบส
    
    # Getter methods
    def get_station_list(self):
        return self.__station_list
    
    # Setter methods
    def set_station_list(self,station_list):
        self.__station_list = station_list
# Class Payment
class Payment:
    def __init__(self, payment_id, amount, payment_time):
        self.__payment_id = payment_id
        self.__amount = amount
        self.__payment_time = payment_time

    # Getter methods
    def get_payment_id(self):
        return self.__payment_id

    def get_amount(self):
        return self.__amount

    def get_payment_time(self):
        return self.__payment_time

    # Setter methods
    def set_amount(self, amount):
        self.__amount = amount

    def set_payment_time(self, payment_time):
        self.__payment_time = payment_time

# Class Booking
class Booking:
    def __init__(self, booking_id, user, station, payment, start_time, end_time, status):
        self.__booking_id = booking_id
        self.__user = user  # สมมติว่า user เป็นอ็อบเจกต์ของคลาส User
        self.__station = station  # สมมติว่า station เป็นอ็อบเจกต์ของคลาส Station
        self.__payment = payment
        self.__start_time = start_time
        self.__end_time = end_time
        self.__status = status

    # Getter methods
    def get_booking_id(self):
        return self.__booking_id

    def get_user(self):
        return self.__user

    def get_station(self):
        return self.__station

    def get_payment(self):
        return self.__payment

    def get_start_time(self):
        return self.__start_time

    def get_end_time(self):
        return self.__end_time

    def get_status(self):
        return self.__status

    # Setter methods
    def set_user(self, user):
        self.__user = user

    def set_station(self, station):
        self.__station = station

    def set_payment(self, payment):
        self.__payment = payment

    def set_start_time(self, start_time):
        self.__start_time = start_time

    def set_end_time(self, end_time):
        self.__end_time = end_time

    def set_status(self, status):
        self.__status = status

#Class History
class History:
    def __init__(self):
        self.__booking_list = self.getAllBooking()
    
    def getAllBooking(self):
        return ['book'] #เชื่อมดาต้าเบส
    
    # Getter methods
    def get_booking_list(self):
        return self.__booking_list
    
    # Setter methods
    def set_booking_list(self,booking_list):
        self.__booking_list = booking_list
