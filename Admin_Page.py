from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

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

class Admin_main_page:
    def __init__(self):
        self.__router = APIRouter()
        self.__templates= Jinja2Templates(directory="Admin")
        self.setup_routes()

    def setup_routes(self):
        @self.__router.get("/admin", response_class=HTMLResponse)
        async def show_admin_main_page(request: Request):
            return self.__templates.TemplateResponse("admin-main.html", {"request": request})

    def get_router(self):
        return self.__router


class Announcement_page:
    def __init__(self):
        self.__router = APIRouter()
        self.__templates= Jinja2Templates(directory="Admin")
        self.setup_routes()

    def setup_routes(self):
        @self.__router.get("/announcement", response_class=HTMLResponse)
        async def create_annoucement(request: Request):
            return self.__templates.TemplateResponse("Announcement.html", {"request": request})

    def get_router(self):
        return self.__router

class Customer_page:
    def __init__(self):
        self.__router = APIRouter()
        self.__templates= Jinja2Templates(directory="Admin")
        self.setup_routes()

    def setup_routes(self):
        @self.__router.get("/customer", response_class=HTMLResponse)
        async def show_customer(request: Request):
            return self.__templates.TemplateResponse("customer.html", {"request": request})

    def get_router(self):
        return self.__router

class History_page:
    def __init__(self):
        self.__router = APIRouter()
        self.__templates= Jinja2Templates(directory="Admin")
        self.setup_routes()

    def setup_routes(self):
        @self.__router.get("/history", response_class=HTMLResponse)
        async def show_history(request: Request):
            return self.__templates.TemplateResponse("History.html", {"request": request})

    def get_router(self):
        return self.__router

class Station_edit_page:
    def __init__(self):
        self.__router = APIRouter()
        self.__templates= Jinja2Templates(directory="Admin")
        self.setup_routes()

    def setup_routes(self):
        @self.__router.get("/edit_station", response_class=HTMLResponse)
        async def edit_station(request: Request):
            return self.__templates.TemplateResponse("station_edit.html", {"request": request})

    def get_router(self):
        return self.__router