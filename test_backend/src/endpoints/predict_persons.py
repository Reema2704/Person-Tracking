from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import UploadFile, File
from fastapi.responses import StreamingResponse
# from utils.face_blur.algo import track_person_in_video
from database.track_db import TrackDB
from typing import List


router =APIRouter(
    # prefix="/Admin",
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
)


router.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@router.post("/upload_images")
async def upload_file(request: Request, videoFile: UploadFile = File(...)):
    # Process the uploaded video file as needed
    # You can save it to a specific location or perform further operations
    
    # For example, you can save the uploaded file to the "uploads" directory
    file_location = f"uploads/{videoFile.filename}"
    with open(file_location, "wb") as file:
        file.write(videoFile.file.read())
    
    return JSONResponse(content={"success": True})

@router.get("/predict_persons")
async def person_recognition(request: Request):
    return templates.TemplateResponse("predict_persons.html", {"request": request})


@router.get('/video_feed')
def video_feed(person_ids: List[str]):
    db = TrackDB()
        # Get the list of CCTV video details from MongoDB
        # videos = collection.find()
    videos = db.get_cameras()
        # Process videos in parallel using ThreadPoolExecutor
        # Schedule the video processing tasks
    for video in videos:
        video_id = str(video["camera_id"])
        video_path = video["camera_path"]
        print(f"video_id: {video_id}")  
        print(f"video_path: {video_path}")
        print(f"person: {person_ids}")
        
    # return StreamingResponse(track_person_in_video(video_id=video_id, video_path=video_path, person_ids=person_ids), media_type='multipart/x-mixed-replace; boundary=frame')
