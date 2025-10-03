from pymongo import MongoClient
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from typing import Optional
import jwt
from datetime import timedelta, datetime, UTC, timezone
from bson import ObjectId

load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client.quiz_app
users_collection = db.users
quizzes_collection = db.quizzes
results_collection = db.results
answers_collection = db.answers
questions_collection = db.questions
admin_collection = db.admins

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "mysecretkey999"  # Use a strong secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 720  ## 12 hours


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    user_id = payload.get("sub")  # sub = user id
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid user ID format")

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def get_current_admin(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    admin_id = payload.get("sub")
    if not admin_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    try:
        admin = admin_collection.find_one({"_id": ObjectId(admin_id)})
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid admin ID format")

    if admin is None:
        raise HTTPException(status_code=401, detail="Admin not found")
    return admin
