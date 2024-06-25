from pydantic import BaseModel, EmailStr
from typing import Optional


class user_sign_up(BaseModel):
    username: str
    password: str
    role: str
    timestamp: str
    email_id: EmailStr


class login(BaseModel):
    username: str
    password: str


class forget_password(BaseModel):
    username: str
    email_id: EmailStr


class AddPerson(BaseModel):
    # name: str
    img_path: str
    img_name: str
    timestamp: str


class AddCamera(BaseModel):
    camera_id: str
    camera_name: str
    camera_path: str
    timestamp: str


# class InputPerson(BaseModel):
#     # id: str
#     # first_name: str
#     # last_name: str
#     name: str
#     # description: str


# class InputCamera(BaseModel):
#     camera_name: str
# ip: str
# port: str


class Track(BaseModel):
    person_id: str
    person_name: str
    camera_id: str
    camera_name: str
    timestamp: str
