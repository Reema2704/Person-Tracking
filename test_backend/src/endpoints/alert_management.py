from fastapi import FastAPI, Request, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

router = APIRouter(
    # prefix="/Admin",
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
)
router.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@router.get("/alert_management")
async def alert_management(request: Request):
    return templates.TemplateResponse("alert_management.html", {"request": request})
