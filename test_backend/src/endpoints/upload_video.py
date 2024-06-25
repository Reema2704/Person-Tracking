from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import UploadFile, File


router =APIRouter(
    # prefix="/Admin",
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
)

router.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# @router.post("/upload")
# async def upload_file(request: Request, videoFile: UploadFile = File(...)):
#     # Process the uploaded video file as needed
#     # You can save it to a specific location or perform further operations
#     # For example, you can save the uploaded file to the "uploads" directory
#     file_location = f"uploads/{videoFile.filename}"
#     with open(file_location, "wb") as file:
#         file.write(videoFile.file.read())
    
#     return JSONResponse(content={"success": True})


@router.get("/video_form")
async def video_upload_form(request: Request):
    return templates.TemplateResponse("upload_form.html", {"request": request})



