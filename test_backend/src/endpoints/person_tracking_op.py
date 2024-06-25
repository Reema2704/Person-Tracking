from fastapi import FastAPI, File, UploadFile
from typing import List
import cv2
import asyncio
import base64
 
app = FastAPI()
 
async def process_video(video_file):
  # Read video frames
  cap = cv2.VideoCapture(video_file.filename)
  frames = []
  while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
      break
    # Apply OpenCV processing (replace with your logic)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frames.append(gray)
  cap.release()
  return frames
 
@app.post("/process_videos")
async def upload_and_process(files: List[UploadFile] = File(...)):
  processed_videos = []
  tasks = [asyncio.create_task(process_video(f)) for f in files]
  for task in tasks:
    processed_videos.append(await task)
  return processed_videos
 
def encode_frame(frame):
  _, buffer = cv2.imencode('.jpg', frame)
  return base64.b64encode(buffer.tobytes()).decode('utf-8')
 
# Example endpoint to serve a single processed video (modify for all)
@app.get("/video/{video_id}")
async def get_video(video_id: int):
  if video_id >= len(processed_videos):
    return {"error": "Invalid video ID"}
  frames = processed_videos[video_id]
  return [encode_frame(frame) for frame in frames]