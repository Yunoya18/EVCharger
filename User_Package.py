from fastapi import FastAPI, Request, APIRouter, Form, Depends, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import HTTPException
from DatabaseConnection import Database
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import RedirectResponse
import base64


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

        #set page
        self.__booking_station_list_page = Booking_Station_list_page()
        self.__login_page = Login_Page(self)
        self.__register_page = Register_Page()
        self.__setting_page = Setting_page()
        self.__profile_page = Profile_page()
        self.__bookinglist_page = Booking_List_page()
        self.__result_page = Result()
        self.__booking_station_page = Booking_Station_page()

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
            if user_id:
                user = self.__database.getUserInfo(user_id)
                return self.__templates.TemplateResponse("Customer-main.html", {"request": request, "user": user.get_username()})
            else:
                return self.__templates.TemplateResponse("Customer-main.html", {"request": request, "user":None})


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
            return self.__templates.TemplateResponse("station-list.html", {"request": request, "all_station":self.__all_station.get_station_list()})

    def get_router(self):
        return self.__router

# Class Booking_Station_page
class Booking_Station_page:
    def __init__(self):
        self.__router = APIRouter()
        self.__templates = Jinja2Templates(directory="templates")
        self.setup_routes()

    def setup_routes(self):
        @self.__router.get("/booking/station/{station_id}", response_class=HTMLResponse)
        async def toBooking_Station_page(request: Request, station_id: int):
            return self.__templates.TemplateResponse("station.html", {"request": request, "station_id": station_id})

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
                return {"message": "Invalid username or password."}  # Handle login failure

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
                    return {"message": "Registration failed. User might already exist."}  # Handle error
            else:
                return {"message": "Password mai thong gan a pai sai ma mai naaaaa"}

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
            user = self.__database.getUserInfo(user_id)
            profile_picture_data = base64.b64encode(user.get_profile()).decode("utf-8")
            profile_picture_url = f"data:image/jpeg;base64,{profile_picture_data}"
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
            full_name = full_name.split()
            firstname = full_name[0]
            surname = full_name[1]
            user_id = request.cookies.get("user_id")
            hash_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            picture_data = await fileInput.read()
            self.__database.editProfileDB(user_id,email,firstname,surname,hash_password,phone,picture_data)
            return RedirectResponse(url="/profile", status_code=303)

    def get_router(self):
        return self.__router
    
class Booking_List_page:
    def __init__(self):
        self.__router = APIRouter()
        self.__templates = Jinja2Templates(directory="templates")
        self.setup_routes()

    def setup_routes(self):
        @self.__router.get("/booking_list", response_class=HTMLResponse)
        async def showBookingActive(request: Request):
            return self.__templates.TemplateResponse("Booking_list.html", {"request": request})

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
            return self.__templates.TemplateResponse("result.html", {"request": request})

    def get_router(self):
        return self.__router

m = Main_page()
app = m.get_app()
