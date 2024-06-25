from fastapi import APIRouter

router = APIRouter(
    # prefix="/Admin",
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
)
