from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from typing import List

router = APIRouter(
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
)


@router.get("/stream")
def get_stream_from_camera(camera_id):
    try:
        data = ""
        if data:
            return StreamingResponse(data, media_type="multipart/x-mixed-replace; boundary=frame")
        else:
            return "No data found!"
    except Exception as e:
        return {
            "Error": str(e)
        }