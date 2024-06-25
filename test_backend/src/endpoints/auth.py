import cv2
from fastapi import FastAPI, Request, UploadFile, File, APIRouter, status
from starlette.responses import FileResponse
import uuid
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

router = APIRouter(
    # prefix="/Admin",
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
)

# app = FastAPI()
router.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(request: Request):
    form = await request.form()
    print(form)
    username = form.get("username")
    password = form.get("password")
    print(username)
    print(password)
    # Perform login validation here
    # You can compare the entered username and password with a stored set of credentials

    if username == "admin" and password == "1234":
        # return {"message": "Login successful"}
        response = RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)
        return response
        # return templates.TemplateResponse("home.html", {"request": request})
        # return response
    else:
        return templates.TemplateResponse("login.html", {"request": request})
        # return {"message": "Invalid username or password"}


@router.get("/home")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
