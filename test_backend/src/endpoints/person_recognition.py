from fastapi import FastAPI, Request, APIRouter, HTTPException, Depends, status, BackgroundTasks
from fastapi.responses import JSONResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import UploadFile, File
import shutil
import os
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from bson.objectid import ObjectId
from typing import List
import sys
import cv2
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime, timedelta
import imutils
import time
from imutils.video import FPS
import sys
sys.path.append("/home/reemarani/work/test_poc/test_backend")
from config.config import PathConfig, FaceBlurConfig
from database.track_db import TrackDB
from typing import List

db = TrackDB()

start_time = FaceBlurConfig.start_time
end_time = FaceBlurConfig.end_time
count1 = FaceBlurConfig.count1
count2 = FaceBlurConfig.count2

sys.path.append("/home/reemarani/work/test_poc1/test_backend")
from database.track_db import TrackDB
from src.utils.face_blur import algo
from pydantic import BaseModel
import sys

sys.path.append("/home/reemarani/work/test_poc1/test_poc/test_backend")
from config.config import Database, PersonData
# from database.models import InputCamera
from database.track_db import TrackDB
import datetime

router = APIRouter(
    # prefix="/Admin",
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
)

router.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@router.post("/upload")
async def upload_file(videofile: UploadFile = File(...)):
    # Process the uploaded video file as needed
    # You can save it to a specific location or perform further operations
    # For example, you can save the uploaded file to the "uploads" directory
    file_name = videofile.filename.split("/")[-1]
    saved_dir = PersonData.INPUT_IMG_PATH
    print(f"saved_dir: {saved_dir}")
    print(f"not os.path.isdir(saved_dir): {not os.path.isdir(saved_dir)}")
    if not os.path.isdir(saved_dir):
        os.makedirs(saved_dir)
    test_filename = os.path.join(saved_dir, videofile.filename)
    # file_location = f"uploads/images/{videofile.filename}"
    with open(test_filename, "wb") as file:
        file.write(videofile.file.read())

    db = TrackDB()
    db.add_person(img_path=test_filename, img_name=file_name)
    return JSONResponse(content={"success": True})


@router.post("/persons_upload")
async def upload_image(imgFile: UploadFile = File(...)):
    # Process the uploaded video file as needed
    # You can save it to a specific location or perform further operations
    # For example, you can save the uploaded file to the "uploads" directory
    # file_location = f"uploads/images/{uploadFile.filename}"
    try:
        # if uploadFile.filename:
        file_name = imgFile.filename.split("/")[-1]
        file_name_ext = imgFile.filename.split(".")[-1]
        if file_name_ext in ["jpg", "jpeg", "png"]:
            # saved_dir- directory path where we'll save the uploaded file 
            saved_dir = PersonData.INPUT_IMG_PATH
            print(f"saved_dir: {saved_dir}")
            print(f"not os.path.isdir(saved_dir): {not os.path.isdir(saved_dir)}")
            if not os.path.isdir(saved_dir):
                os.makedirs(saved_dir)
            test_filename = os.path.join(saved_dir, imgFile.filename)
            with open(test_filename, "wb") as file_object:
                file_object.write(imgFile.file.read())
                # shutil.copyfileobj(uploadFile.file, file_object)

            db = TrackDB()
            db.add_person(img_path=test_filename, img_name=file_name)
            response = RedirectResponse(url="/person_recognition", status_code=status.HTTP_303_SEE_OTHER)
            return response
            # return templates.TemplateResponse("person_recognition.html", {"request": {"filename":imgFile.filename,
            # "status":"Success"}}) raise HTTPException(status_code=status.HTTP_200_OK, detail="File Uploaded
            # Successfully!") return {"filename":imgFile.filename,"status":"Success"}
        else:
            return "Invalid Image Format!"

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/cameras/upload")
async def upload_video(videofile: UploadFile = File(...)):
    # Process the uploaded video file as needed
    # You can save it to a specific location or perform further operations
    # For example, you can save the uploaded file to the "uploads" directory
    # camera_id = request.camera_id
    # camera_name = request.camera_name
    # print("camera_id: ",camera_id)
    try:
        if videofile.filename:
            file_name = videofile.filename
            print(f"file_name: {file_name}")
            file_name_ext = file_name.split(".")[-1]
            if file_name_ext in ["mp4", "avi", "webm"]:
                # saved_dir- directory path where we'll save the uploaded file 
                saved_dir = PersonData.INPUT_VIDEO_PATH
                print(f"saved_dir: {saved_dir}")
                print(f"not os.path.isdir(saved_dir): {not os.path.isdir(saved_dir)}")
                if not os.path.isdir(saved_dir):
                    os.makedirs(saved_dir)
                test_filename = os.path.join(saved_dir, file_name)
                print(f"test: {test_filename}")
                with open(test_filename, "wb+") as file_object:
                    # shutil.copyfileobj(file_name, file_object)
                    file_object.write(videofile.file.read())

                db = TrackDB()
                # db.add_person(img_path=saved_dir, img_name=file_name)
                a = db.add_camera(camera_id="1", camera_name="CAM01", camera_path=test_filename)
                print(f"a: {a}")
                # raise HTTPException(status_code=status.HTTP_200_OK, detail="File Uploaded Successfully!")
                return "Camera Details Uploaded Successfully!"

            else:
                return "Invalid Video Format!"

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/persons/get_all")
def get_all_persons():
    db = TrackDB()
    db.get_persons()
    try:
        db = TrackDB()
        data = db.get_persons()
        print(f"data: {data}")
        if data:
            lst = []
            for i in data:
                id = i["id"]
                # img_path = i["img_path"]
                img_name = i["img_name"]
                timestamp = i["timestamp"]

                info = {
                    "id": id,
                    # "img_path": img_path,
                    "img_name": img_name,
                    "timestamp": timestamp
                }

                lst.append(info)

            return lst
        else:
            return "No data found!"

    except Exception as e:
        return {
            "Error": str(e)
        }


@router.get("/cameras/get_all")
def get_all_cameras():
    db = TrackDB()
    db.get_cameras()
    try:
        db = TrackDB()
        data = db.get_cameras()
        if data:
            lst = []
            for i in data:
                id = i["id"]
                camera_name = i["camera_name"]
                camera_path = i["camera_path"]
                timestamp = i["timestamp"]

                info = {
                    "id": id,
                    "camera_name": camera_name,
                    "camera_path": camera_path,
                    "timestamp": timestamp
                }

                lst.append(info)

            return lst
        else:
            return "No data found!"

    except Exception as e:
        return {
            "Error": str(e)
        }


@router.delete("/persons/delete_one/{image_name}")
def delete_one(image_name: str):
    try:
        db = TrackDB()
        data = db.delete_one_person(image_name=image_name)
        print(f"data: {data}")
        return {
            "delete_status": f"{image_name} deleted successfully"
        }

    except Exception as e:
        return {
            "delete_status": str(e)
        }


@router.delete("/persons/delete_all")
def delete_all():
    try:
        db = TrackDB()
        data = db.delete_all_persons()
        print(f"data: {data}")
        return {
            "delete_status": "Jobs deleted successfully"
        }

    except Exception as e:
        return {
            "delete_status": str(e)
        }


@router.delete("/cameras/delete_all")
def delete_all():
    try:
        db = TrackDB()
        data = db.delete_all_cameras()
        print(f"data: {data}")
        return {
            "delete_status": "Jobs deleted successfully"
        }

    except Exception as e:
        return {
            "delete_status": str(e)
        }


@router.get("/person_recognition")
async def person_recognition(request: Request):
    return templates.TemplateResponse("person_recognition.html", {"request": request})


@router.get("/high_chart")
async def high_chart(request: Request):
    return templates.TemplateResponse("high_chart.html", {"request": request})


@router.get("/tracks/alert_management")
def get_all_alerts():
    db = TrackDB()
    try:
        db = TrackDB()
        data = db.get_tracks()
        print(f"data: {data}")
        if data:
            lst = []
            for item in data:
                person_id = item["person_id"]
                camera_id = item["camera_id"]
                timestamp = item["timestamp"]
                print(f"timestamp: {timestamp}")
                dt_object = datetime.datetime.fromtimestamp(timestamp)
                print("dt_object:", dt_object)
                info = {
                    "person_id": person_id,
                    "camera_id": camera_id,
                    "timestamp": dt_object
                }
                lst.append(info)
            print("list of alerts", lst)
            return lst
    except Exception as e:
        error = str(e)
        return {
            "Error": error
        }


@router.get("/tracks/get_all")
def get_all_tracks():
    db = TrackDB()
    try:
        db = TrackDB()
        data = db.get_tracks()
        print(f"data: {data}")
        result = {}

        if data:
            lst = []
            for item in data:
                person_id = item["person_id"]
                camera_id = item["camera_id"]
                timestamp = item["timestamp"]
                # person_id, timestamp, camera_id = item

                if person_id not in result:
                    result[person_id] = []

                result[person_id].append([timestamp, camera_id])
                # id = i["id"]
                # person_id = i["person_id"]
                # camera_id = i["camera_id"]
                # timestamp = i["timestamp"]
                # date = i["date"]
                # time = i["time"]
                # info = {
                # "id": id,
                # "person_id": person_id,
                # "camera_id": camera_id,
                # "timestamp": timestamp
                # # "date": date,
                # # "time": time
                # }

                # lst.append(info)
            # obj_of_person = {}
            # for item in lst:
            #     obj_of_person[item["person_id"]]= [*filter(lambda x: x["person_id"]==item["person_id"],lst)]
            # print(f"obj_of_person: {obj_of_person}")
            return JSONResponse(content=result)

            # return {
            #     "xaxis":obj_of_person.keys(),
            #     "yaxis":obj_of_person.values()
            # }
        else:
            return "No data found!"
    except Exception as e:
        return {
            "Error": str(e)
        }


# def process_video(video_path):
#     with executor:
#         result = executor.submit(recognize_person, video_path)
#         return result.result()


# @router.post("/process-multiple-videos")
# async def process_multiple_videos(videos: List[UploadFile] = File(...)):
def process_multiple_videos(person_ids: List[str]):
    try:
        # Read the person's image from local storage (assuming the same image for all videos)
        # person_image_filename = "person_image.jpg" # Replace with the actual filename
        # person_image = cv2.imread(person_image_filename)
        db = TrackDB()
        # Get the list of CCTV video details from MongoDB
        # videos = collection.find()
        videos = db.get_cameras()
        # Process videos in parallel using ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            # Schedule the video processing tasks
            for video in videos:
                video_id = str(video["camera_id"])
                video_path = video["camera_path"]
                print(f"video_id: {video_id}")
                print(f"video_path: {video_path}")
                print(f"person: {person_ids}")
                futures = [executor.submit(algo.track_person_in_video, video_id, video_path, person_ids)]
            # future = executor.submit(algo.track_person_in_video, video_id, video_path, person_ids)
            # futures = []
            # for video in videos:
            #     video_id = str(video["camera_id"])
            #     video_path = video["camera_path"]
            #     print(f"video_id: {video_id}")
            #     print(f"video_path: {video_path}")
            #     print(f"person: {person_ids}")
            #     future = executor.submit(algo.track_person_in_video, video_id, video_path, person_ids)
            # futures.append(future)
            print(f"future: {futures}")
            # Wait for all tasks to complete
            concurrent.futures.wait(futures)
        return {"message": "All videos processed successfully"}
    except Exception as e:
        error = str(e)
        return {
            "error": error
        }


@router.post("/process-multiple-videos")
async def test(person_ids: List[str]):
    try:
        return Response(process_multiple_videos(person_ids=person_ids), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        error = str(e)
        return {
            "error": error
        }


@router.get("/tracks/person")
def get_person_tracks(person_id):
    try:
        db = TrackDB()
        data = db.get_tracks_for_person(person_id=person_id)
        print(f"data: {data}")
        if data:
            return data
        else:
            return "No data found!"
    except Exception as e:
        return {
            "Error": str(e)
        }


@router.get("/tracks/camera")
def get_camera_tracks(camera_id):
    try:
        db = TrackDB()
        data = db.get_tracks_for_camera(camera_id=camera_id)
        print(f"data: {data}")
        if data:
            return data
        else:
            return "No data found!"
    except Exception as e:
        return {
            "Error": str(e)
        }
    