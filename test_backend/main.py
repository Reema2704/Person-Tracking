import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,requests
from routes.api import router as api_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os


app = FastAPI()
script_dir = os.path.dirname((os.path.abspath(__file__)))
st_abs_file_path = os.path.join(script_dir, "static/")
app.mount("/static", StaticFiles(directory=st_abs_file_path), name="static")

# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")


origins = "*"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


# os.system("python3 src/utils/scheduled_job.py")

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, workers=1)
