from fastapi import Request, FastAPI, status, Depends, HTTPException
import time
from app.config.database import users_collection, admin_collection
from app.models.model import UserLogin, UserRegistration
from app.routes.user_route import user_router, verify_password
from app.routes.question_route import quiz_router
from app.routes.admin_route import admin_router

# from app.routes.answer_route import answer_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from app.config.database import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from passlib.context import CryptContext

app = FastAPI(title="Quiz App API", docs_url="/api")


@app.get("/")
async def root():
    return {"message": "Welcome to the Quiz App API"}


@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    print(
        f"\nTime Log of request ==== {request.method} {request.url} took {duration:.2f}s\n"
    )
    return response


@app.post("/token", response_model=dict)
def authentication_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_data = users_collection.find_one({"email": form_data.username})
    if user_data and verify_password(form_data.password, user_data["password"]):
        role = "user"
    else:
        user_data = admin_collection.find_one({"email": form_data.username})
        if user_data and verify_password(form_data.password, user_data["password"]):
            role = "admin"
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user_data["_id"]), "role": role},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer", "role": role}


app.include_router(user_router, tags=["User Operations"])
app.include_router(quiz_router, tags=["Question"])
app.include_router(admin_router, tags=["Admin Operations"])
# app.include_router(answer_router, tags=["Answer "])
