from fastapi import FastAPI, Request, APIRouter, Form, Depends, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import HTTPException
from DatabaseConnection import Database
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import RedirectResponse
from datetime import datetime
import base64
import json
from Admin_Page import Admin_main_page,Announcement_page,Customer_page,History_page,Station_edit_page



# Class User
class User:
    def __init__(self, user_id, username, email, password, firstname, surname, phone, profile, status):
        self.__user_id = user_id
        self.__username = username
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
    
    def get_username(self):
        return self.__username
    
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
    def set_username(self, username):
        self.__username = username
        
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
    def __init__(self, location_id, lat, lng):
        self.__location_id = location_id
        self.__lat = lat
        self.__lng = lng

    # Getter methods
    def get_location_id(self):
        return self.__location_id

    def get_lat(self):
        return self.__lat
    
    def get_lng(self):
        return self.__lng

    # Setter methods
    def set_lat(self, lat):
        self.__lat = lat
    
    def set_lng(self, lng):
        self.__lng = lng

# Class Station
class Station(Location):
    def __init__(self, location_id, lat, lng, station_id, station_name, status, price_per_hour):
        super().__init__(location_id, lat, lng)
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
        database = Database()
        station = database.getALLStation()
        return station
    
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
    def __init__(self, booking_id, user, station, payment, start_time, end_time, booking_date, status, codebooking):
        self.__booking_id = booking_id
        self.__user = user
        self.__station = station
        self.__payment = payment
        self.__start_time = start_time
        self.__end_time = end_time
        self.__status = status
        self.__booking_date = booking_date
        self.__codebooking = codebooking

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
        return str(self.__start_time)

    def get_end_time(self):
        return str(self.__end_time)

    def get_status(self):
        return str(self.__status)

    def get_booking_date(self):
        return str(self.__booking_date)

    def get_codebooking(self):
        return self.__codebooking

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

    def set_booking_date(self, booking_date):
        self.__booking_date = booking_date

    def set_codebooking(self, codebooking):
        self.__codebooking = codebooking


#Class History
class History:
    def __init__(self,user_id=None):
        self.__booking_list = self.getAllBooking(user_id)
    
    def getAllBooking(self,user_id=None):
        database = Database()
        list_booking = database.gethistory(user_id)
        return list_booking
    
    # Getter methods
    def get_booking_list(self):
        return self.__booking_list
    
    # Setter methods
    def set_booking_list(self,booking_list):
        self.__booking_list = booking_list

def get_current_user(request: Request):
    # Check for user cookie
    user = request.cookies.get("user_id")
    
    if not user:
        # If no cookie, redirect to login page
        raise HTTPException(status_code=303, detail="Not authenticated", headers={"Location": "/login"})
    return user

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # List of paths that do not require authentication
        exempt_paths = ["/login", "/register", "/static", "/"]

        # If the request path is not in exempt_paths, check if the user is logged in
        if not any(request.url.path.startswith(path) for path in exempt_paths):
            user = request.cookies.get("user_id")
            if not user:
                return RedirectResponse(url="/login")  # Redirect to login if not authenticated

        response = await call_next(request)
        return response

# Class Main_page
class Main_page:
    def __init__(self):
        self.__user = None  # สถานะของผู้ใช้
        self.__app = FastAPI()
        self.__templates = Jinja2Templates(directory="templates")
        self.__app.mount("/static", StaticFiles(directory="static"), name="static")
        self.__database = Database()
        self.__allstation = All_Station()

        #set page
        self.__booking_station_list_page = Booking_Station_list_page()
        self.__login_page = Login_Page(self)
        self.__register_page = Register_Page()
        self.__setting_page = Setting_page()
        self.__profile_page = Profile_page()
        self.__bookinglist_page = Booking_List_page()
        self.__result_page = Result()
        self.__booking_station_page = Booking_Station_page()
        self.__use_page = Use_page()
        self.__admin_main_page = Admin_main_page()
        self.__announcement_page = Announcement_page()
        self.__customer_page = Customer_page()
        self.__history_page = History_page()
        self.__station_edit_page = Station_edit_page()

        self.__app.add_middleware(AuthMiddleware)

        self.setup_routes()
        self.include_routers()

    def set_user(self, user):
        self.__user = user

    def get_user(self):
        return self.__user

    def setup_routes(self):
        @self.__app.get("/", response_class=HTMLResponse)
        async def showmain_page(request: Request):
            user_id = request.cookies.get("user_id")  # Get the username from cookies
            list_allstation = self.__allstation.getAllStation()
            stations_data = [{"lat": station.get_lat(), "lng": station.get_lng(), "name": station.get_station_name()} for station in list_allstation]
            print(stations_data)
            if user_id:
                user = self.__database.getUserInfo(user_id)
                return self.__templates.TemplateResponse("Customer-main.html", {"request": request, "user": user.get_username(),"list_allstation":stations_data})
            else:
                return self.__templates.TemplateResponse("Customer-main.html", {"request": request, "user":None, "list_allstation":stations_data})
        @self.__app.post("/", response_class=HTMLResponse)
        async def get_location_user(request: Request):
            data = await request.json()
            lat = data.get("latitude")
            lng = data.get("longitude")
            response = HTMLResponse(content="Received latitude and longitude")
            response.set_cookie(key="user_location", value=f"lat={lat}&lng={lng}")
            return response

    def include_routers(self):
        # รวม APIRouter จากคลาสอื่นๆ
        self.__app.include_router(self.__booking_station_list_page.get_router())
        self.__app.include_router(self.__login_page.get_router())
        self.__app.include_router(self.__register_page.get_router())
        self.__app.include_router(self.__profile_page.get_router())
        self.__app.include_router(self.__setting_page.get_router())
        self.__app.include_router(self.__bookinglist_page.get_router())
        self.__app.include_router(self.__result_page.get_router())
        self.__app.include_router(self.__booking_station_page.get_router())
        self.__app.include_router(self.__use_page.get_router())
        self.__app.include_router(self.__admin_main_page.get_router())
        self.__app.include_router(self.__announcement_page.get_router())
        self.__app.include_router(self.__customer_page.get_router())
        self.__app.include_router(self.__history_page.get_router())
        self.__app.include_router(self.__station_edit_page.get_router())

    def get_app(self):
        return self.__app

# Class Booking_Station_list_page
class Booking_Station_list_page:
    def __init__(self):
        self.__router = APIRouter()
        self.__templates = Jinja2Templates(directory="templates")
        self.__all_station = All_Station()
        self.setup_routes()

    def setup_routes(self):
        @self.__router.get("/booking", response_class=HTMLResponse)
        async def toBooking_Station_list_page(request: Request):
            user_id = request.cookies.get("user_id")
            address = request.cookies.get("user_location")
            all_station = self.__all_station.get_station_list()
            if address:
                all_station.sort(key=lambda station: self.sortstation(station, request))
            if not user_id:
                return RedirectResponse(url="/login")
            return self.__templates.TemplateResponse("station-list.html", {"request": request, "all_station": all_station})
    
    def sortstation(self, station, request: Request):
        from urllib.parse import parse_qs
        address = request.cookies.get("user_location")
        parsed_address = parse_qs(address)
        lat = float(parsed_address.get('lat', [None])[0])
        lng = float(parsed_address.get('lng', [None])[0])
        
        station_lat = station.get_lat()
        station_lng = station.get_lng()
        
        return self.haversine(lat, lng, station_lat, station_lng)

    def haversine(self, lat1, lon1, lat2, lon2):
        import math
        R = 6371  # Radius of Earth in kilometers
        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        a = math.sin(dLat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c  # Distance in kilometers
    
    def get_router(self):
        return self.__router


# Class Booking_Station_page
class Booking_Station_page:
    def __init__(self):
        self.__router = APIRouter()
        self.__templates = Jinja2Templates(directory="templates")
        self.__date = datetime.now().date()
        self.__database = Database()
        self.__today = f"{self.__date.year}-{self.__date.month}-{self.__date.day}"
        self.setup_routes()

    def setup_routes(self):
        @self.__router.get("/booking/station/{station_id}", response_class=HTMLResponse)
        async def toBooking_Station_page(request: Request, station_id: int):
            user_id = request.cookies.get("user_id")
            if not user_id:
                return RedirectResponse(url="/login")
            return self.__templates.TemplateResponse("station.html", {"request": request, "station_id": station_id, "today":self.__today})
        
        @self.__router.post("/booking/station/{station_id}", response_class=HTMLResponse)
        async def createBooking(request: Request, 
            station_id: int,
            booking_date: str = Form(...),
            booking_time_start: str = Form(...),
            booking_time_end: str = Form(...)
        ):
            user_id = request.cookies.get("user_id")
            booking_same = self.__database.getbooking_same(booking_date,booking_time_start,booking_time_end,station_id)
            if (booking_same):
                return self.__templates.TemplateResponse("station.html", {"request": request, "station_id": station_id, "today":self.__today, "error":"วันและเวลามีผู้อื่นจองแล้ว"})
            else:
                code = self.createCode()
                self.__database.CreateBooking(user_id,station_id,booking_time_start,booking_time_end,booking_date,code,status="pending")
                return RedirectResponse(url="/booking", status_code=303)

    def createCode(self):
        import random
        import string
        characters = string.ascii_letters
        code = ''.join(random.choice(characters) for _ in range(6))
        return code

    def get_router(self):
        return self.__router

# Login page
class Login_Page:
    def __init__(self, main_page):
        self.__router = APIRouter()
        self.__templates = Jinja2Templates(directory="templates")
        self.__database = Database()
        self.setup_routes()

    def setup_routes(self):
        import hashlib
        @self.__router.get("/login", response_class=HTMLResponse)
        async def to_login_page(request: Request):
            return self.__templates.TemplateResponse("login.html", {"request": request})

        @self.__router.post("/login")
        async def login_user(request: Request, username: str = Form(...), password: str = Form(...)):
            hash_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            user = self.__database.validate_user(username, hash_password)
            if user:
                # Successful login: Store user information or set session here if needed
                print(f"User logged in: {user[0]}")  # Log the user's first name
                response = RedirectResponse(url="/", status_code=303)  # Redirect to main page on success
                response.set_cookie(key="user_id", value=user[0])  # Store username in cookie
                return response
            else:
                return JSONResponse(status_code=400, content={"message": "Invalid username or password."})

        @self.__router.post("/logout")
        async def logout_user(request: Request):
            response = RedirectResponse(url="/", status_code=303)
            response.delete_cookie("user_id")  # Clear the username cookie
            return response

    def get_router(self):
        return self.__router

# Register Page
class Register_Page:
    def __init__(self):
        self.__router = APIRouter()
        self.__templates = Jinja2Templates(directory="templates")
        self.__database = Database()
        self.setup_routes()

    def setup_routes(self):
        import hashlib
        @self.__router.get("/register", response_class=HTMLResponse)
        async def to_register_page(request: Request):
            return self.__templates.TemplateResponse("register.html", {"request": request})

        @self.__router.post("/register")
        async def register_user(
            request: Request, 
            username: str = Form(...), 
            email: str = Form(...), 
            password: str = Form(...),
            confirmpassword: str = Form(...)):

            hash_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            hash_confirm = hashlib.sha256(confirmpassword.encode('utf-8')).hexdigest()
            if hash_password == hash_confirm:
                success = self.__database.insert_user(username, email, hash_password)
                if success:
                    return RedirectResponse(url="/login", status_code=303)  # Redirect on success
                else:
                    return JSONResponse(status_code=400, content={"message": "Registration failed. User might already exist."})
            else:
                return JSONResponse(status_code=400, content={"message": "Passwords do not match. Please try again."})

    def get_router(self):
        return self.__router

class Setting_page:
    def __init__(self):
        self.__router = APIRouter()
        self.__templates = Jinja2Templates(directory="templates")
        self.__database = Database()
        self.setup_routes()

    def setup_routes(self):
        @self.__router.get("/setting", response_class=HTMLResponse)
        async def showSetting_page(request: Request):
            user_id = request.cookies.get("user_id")
            if not user_id:
                return RedirectResponse(url="/login")
            user = self.__database.getUserInfo(user_id)
            return self.__templates.TemplateResponse("setting.html", {"request": request, "user": user.get_username()})

    def get_router(self):
        return self.__router

class Profile_page:
    def __init__(self):
        self.__router = APIRouter()
        self.__templates = Jinja2Templates(directory="templates")
        self.__database = Database()
        self.setup_routes()

    def setup_routes(self):
        import hashlib
        @self.__router.get("/profile", response_class=HTMLResponse)
        async def showProfile_page(request: Request):
            user_id = request.cookies.get("user_id")
            if not user_id:
                return RedirectResponse(url="/login")
            user = self.__database.getUserInfo(user_id)
            if (user.get_profile()):
                profile_picture_data = base64.b64encode(user.get_profile()).decode("utf-8")
                profile_picture_url = f"data:image/jpeg;base64,{profile_picture_data}"
            else:
                profile_picture_url = None
            return self.__templates.TemplateResponse("profile.html", {"request": request, "pic":profile_picture_url,"user":user})
        
        @self.__router.post("/profile", response_class=HTMLResponse)
        async def edit_profile(
            request: Request,
            full_name: str = Form(...),
            email: str = Form(...),
            password: str = Form(...),
            phone: str = Form(...),
            fileInput: UploadFile = File(...)
        ):
            if (full_name.split()):
                full_name = full_name.split()
                firstname = full_name[0]
                surname = full_name[1]
            else:
                firstname = None
                surname = None
            user_id = request.cookies.get("user_id")
            if (password):
                hash_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            else:
                hash_password = None
            if (fileInput):
                picture_data = await fileInput.read()
            else:
                picture_data = None
            self.__database.editProfileDB(user_id,email,firstname,surname,hash_password,phone,picture_data)
            return RedirectResponse(url="/profile", status_code=303)

    def get_router(self):
        return self.__router
#Class Booking_List_page
class Booking_List_page:
    def __init__(self):
        self.__router = APIRouter()
        self.__templates = Jinja2Templates(directory="templates")
        self.__timetoday = str(datetime.now()).split()
        self.__history = History()
        self.__database = Database()
        self.setup_routes()

    def setup_routes(self):
        @self.__router.get("/booking_list", response_class=HTMLResponse)
        async def showBookingActive(request: Request):
            user_id = request.cookies.get("user_id")
            if not user_id:
                return RedirectResponse(url="/login")
            listshow = []
            allbooking = self.__history.getAllBooking(user_id)
            for booking in allbooking:
                time1 = datetime.strptime(booking.get_start_time(), "%H:%M:%S").time()
                time2 = datetime.strptime(self.__timetoday[1][:-7], "%H:%M:%S").time()
                time3 = datetime.strptime(booking.get_end_time(), "%H:%M:%S").time()
                result = time1 <= time2 <= time3
                dateb = booking.get_booking_date() == self.__timetoday[0] and result
                listshow.append(dateb)
            self.__database.UpdateBookingALL(self.__timetoday[0],time2)
            return self.__templates.TemplateResponse("Booking_list.html", {"request": request, "allbooking":zip(allbooking,listshow)})
        @self.__router.post("/booking_list/{booking_id}", response_class=HTMLResponse)
        async def EditBookingcancle(request: Request,booking_id: int):
            user_id = request.cookies.get("user_id")
            if not user_id:
                return RedirectResponse(url="/login")
            self.__database.UpdateBooking(booking_id,None,None,None,"canceled")
            return RedirectResponse(url="/booking_list", status_code=303)

        @self.__router.get("/booking/edit/{booking_id}/{station_id}", response_class=HTMLResponse)
        async def EditBooking(request: Request, booking_id: int, station_id: int):
            user_id = request.cookies.get("user_id")
            if not user_id:
                return RedirectResponse(url="/login")
            booking = self.__database.getBooking(booking_id)
            return self.__templates.TemplateResponse("stationedit.html", {"request": request,"today":self.__timetoday[0],"booking":booking})
        
        @self.__router.post("/booking/edit/{booking_id}/{station_id}", response_class=HTMLResponse)
        async def createBooking(request: Request, booking_id: int,
            station_id: int,
            booking_date: str = Form(...),
            booking_time_start: str = Form(...),
            booking_time_end: str = Form(...)
        ):
            user_id = request.cookies.get("user_id")
            booking_same = self.__database.getbooking_same(booking_date,booking_time_start,booking_time_end,station_id)
            booking = self.__database.getBooking(booking_id)
            if (booking_same):
                return self.__templates.TemplateResponse("stationedit.html", {"request": request,"today":self.__timetoday[0],"booking":booking})
            else:
                print(booking_date,booking_time_start,booking_time_end)
                self.__database.UpdateBooking(booking_id,booking_time_start,booking_time_end,booking_date)
                return RedirectResponse(url="/booking_list", status_code=303)
        
    def get_router(self):
        return self.__router

#Class Use_page
class Use_page:
    def __init__(self):
        self.__router = APIRouter()
        self.__templates = Jinja2Templates(directory="templates")
        self.__timetoday = str(datetime.now()).split()
        self.__database = Database()
        self.setup_routes()
    def setup_routes(self):
        @self.__router.get("/use/{booking_id}", response_class=HTMLResponse)
        async def showUse(request: Request,booking_id: int):
            user_id = request.cookies.get("user_id")
            if not user_id:
                return RedirectResponse(url="/login")
            self.__database.UpdateBooking(booking_id,None,None,None,"completed")
            booking = self.__database.getBooking(booking_id)
            time1 = datetime.strptime(booking.get_end_time(), "%H:%M:%S").time()
            time2 = datetime.strptime(self.__timetoday[1][:-7], "%H:%M:%S").time()

            # แปลง time เป็น datetime เพื่อให้สามารถทำการลบกันได้
            time1_dt = datetime.combine(datetime.today(), time1)
            time2_dt = datetime.combine(datetime.today(), time2)

            # คำนวณผลต่างของเวลา
            time_difference = time1_dt - time2_dt

            # แปลงผลต่างเป็นนาที
            timeleft_minutes = time_difference.total_seconds() // 60
            timeleft_sec = time_difference.total_seconds() % 60
            return self.__templates.TemplateResponse("use-case.html", {"request": request, "booking":booking,"timeleft_minutes":timeleft_minutes,"timeleft_sec":timeleft_sec})
    def get_router(self):
        return self.__router

class Result:
    def __init__(self):
        self.__router = APIRouter()
        self.__templates = Jinja2Templates(directory="templates")
        self.setup_routes()

    def setup_routes(self):
        @self.__router.get("/result", response_class=HTMLResponse)
        async def showResult(request: Request):
            user_id = request.cookies.get("user_id")
            if not user_id:
                return RedirectResponse(url="/login")
            return self.__templates.TemplateResponse("result.html", {"request": request})

    def get_router(self):
        return self.__router

m = Main_page()
app = m.get_app()
