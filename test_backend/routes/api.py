from fastapi import APIRouter
from src.endpoints import face_detection , upload_video, \
auth, person_recognition,\
alert_management, gait_recognition,\
predict_persons, stream_video

router = APIRouter()

router.include_router(face_detection.router)
router.include_router(auth.router)
router.include_router(upload_video.router)
router.include_router(person_recognition.router)
router.include_router(alert_management.router)
router.include_router(gait_recognition.router)
router.include_router(predict_persons.router)
router.include_router(stream_video.router)
