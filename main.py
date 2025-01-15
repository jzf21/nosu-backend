from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session

from typing import List, Optional, Annotated
from enum import Enum
import database.models as models
import database.schemas as schemas

from database.database import SessionLocal, engine
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from api import auth,course
from dependencies import get_current_user
from dotenv import load_dotenv
load_dotenv()  

from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(title="Bucket List API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://nosu-cyber-sec.vercel.app",
        "http://localhost:3000"
    ],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
models.Base.metadata.create_all(bind=engine)


# Dependency for database session


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(course.router, prefix="/course", tags=["course"])
