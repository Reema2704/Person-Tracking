import os

class Database:
    HOST = 'mongodb://localhost'
    PORT = 27017
    DB_NAME = "PersonTracker"
    LOGIN_COL = "login"
    PERSON_COL = "person"
    CAMERA_COL = "camera"
    TRACK_COL = "tracks"
    IMAGES_COL = "images"
    ENCODINGS_COL = "encodings"


class PersonData:
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    INPUT_IMG_PATH = os.path.join(BASE_PATH, "input", "images")
    INPUT_VIDEO_PATH = os.path.join(BASE_PATH, "input", "videos")
    OUTPUT_PATH = os.path.join(BASE_PATH, "output")


class PathConfig:
    BASE_DIR = "/home/reemarani/work/test_poc/test_backend"
    INPUT_DIR = 'input'
    OUT_DIR = 'output'


class FaceBlurConfig:
    start_time = 0
    end_time = 0
    count1 = 0
    count2 = 0
