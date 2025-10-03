from fastapi import APIRouter, HTTPException, status
from app.config.database import admin_collection
from app.models.model import AdminLogin, AdminRegistration
from datetime import datetime, UTC
from passlib.context import CryptContext
import bcrypt

admin_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    # Convert to bytes and handle length limit
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]

    # Generate salt and hash using bcrypt directly
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode("utf-8")
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]

    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)


@admin_router.post("/admin-register", status_code=status.HTTP_201_CREATED)
async def register_admin(admin: AdminRegistration):
    if admin_collection.find_one({"email": admin.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    admin_dict = admin.model_dump()
    admin_dict["password"] = hash_password(admin.password)
    admin_dict["created_at"] = datetime.now(UTC)
    admin_collection.insert_one(admin_dict)

    return {
        "message": "Admin registered successfully",
        "admin_id": str(admin_dict["_id"]),
    }


@admin_router.post("/admin-login")
async def login_admin(admin: AdminLogin):
    db_admin = admin_collection.find_one({"email": admin.email})
    if not db_admin or not verify_password(admin.password, db_admin["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return {"message": "Login successful"}
