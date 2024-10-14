from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from DatabaseConnection import Database

class Announcement:
    def __init__(self, announcement_id, announcement_text, created_time):
        self.__announcement_id = announcement_id
        self.__announcement_text = announcement_text
        self.__created_time = created_time

    #getter
    def get_announcement_id(self):
        return self.__announcement_id

    def get_announcement_text(self):
        return self.__announcement_text

    def get_created_time(self):
        return self.__created_time

    #setter
    def set_announcement_id(self, announcement_id):
        self.__announcement_id = announcement_id

    def set_announcement_text(self, announcement_text):
        self.__announcement_text = announcement_text

    def set_created_time(self, created_time):
        self.__created_time = created_time

#รอดึงข้อมูลขึ้น
class Admin_main_page:
    def __init__(self):
        from User_Package import History, All_User
        self.__router = APIRouter()
        self.__templates= Jinja2Templates(directory="Admin")
        self.__in_active_user = None #รอดึงข้อมูล
        self.__total_customer = All_User().get_total_user()
        self.__total_booking = History().get_total_booking()
        self.setup_routes()

    def setup_routes(self):
        @self.__router.get("/admin", response_class=HTMLResponse)
        async def show_iframe_admin_page(request: Request):
            return self.__templates.TemplateResponse("admin-main.html", {"request": request, "in_active_user": self.__in_active_user, "total_customer": self.__total_customer, "total_booking": self.__total_booking})
        @self.__router.get("/main_admin", response_class=HTMLResponse)
        async def show_admin_main_page(request: Request):
            return self.__templates.TemplateResponse("main.html", {"request": request, "in_active_user": self.__in_active_user, "total_customer": self.__total_customer, "total_booking": self.__total_booking})

    def get_router(self):
        return self.__router

#อาจจะไม่ทำ
class Announcement_page:
    def __init__(self):
        self.__router = APIRouter()
        self.__templates= Jinja2Templates(directory="Admin")
        self.setup_routes()

    def setup_routes(self):
        @self.__router.get("/announcement", response_class=HTMLResponse)
        async def show_annoucement_page(request: Request):
            return self.__templates.TemplateResponse("Announcement.html", {"request": request})
        @self.__router.post("/announcement", response_class=HTMLResponse)
        async def create_announcement(request: Request):
            pass

    def get_router(self):
        return self.__router

#ดึงข้อมูล customer แล้วแสดง
class Customer_page:
    def __init__(self):
        from User_Package import All_User
        self.__router = APIRouter()
        self.__templates= Jinja2Templates(directory="Admin")
        self.__all_customer = All_User().get_user_list()
        self.setup_routes()

    def setup_routes(self):
        @self.__router.get("/customer", response_class=HTMLResponse)
        async def show_customer(request: Request):
            return self.__templates.TemplateResponse("Admin-Customer.html", {"request": request, "all_customer": self.__all_customer})

    def get_router(self):
        return self.__router

#เหลือแสดงข้อมูลตามที่อยากได้ใน html page
class History_page:
    def __init__(self):
        from User_Package import History
        self.__router = APIRouter()
        self.__templates= Jinja2Templates(directory="Admin")
        self.__all_history = History().get_booking_list()
        self.setup_routes()

    def setup_routes(self):
        @self.__router.get("/history", response_class=HTMLResponse)
        async def show_history(request: Request):
            return self.__templates.TemplateResponse("History.html", {"request": request, "all_history": self.__all_history})

    def get_router(self):
        return self.__router

class Station_edit_page:
    def __init__(self):
        from User_Package import All_Station
        self.__router = APIRouter()
        self.__templates = Jinja2Templates(directory="Admin")
        self.__all_station = All_Station().get_station_list()
        self.__db = Database()
        self.setup_routes()

    def setup_routes(self):
        @self.__router.get("/edit_station", response_class=HTMLResponse)
        async def edit_station(request: Request):
            return self.__templates.TemplateResponse("station_edit.html", {"request": request, "all_station": self.__all_station})
        @self.__router.post("/update_station/{station_id}")
        async def update_station(station_id: int):
            return self.__db.updateStaionStatus(station_id) #ติด foreign key

    def get_router(self):
        return self.__router