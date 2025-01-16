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
        "https://nosu-o6l1.vercel.app",
        "https://nosu-cyber-sec.vercel.app",
        "http://localhost:3000",
    ],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Specify methods
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,  # Cache preflight requests for 10 minutes
)

# Create database tables
models.Base.metadata.create_all(bind=engine)


# Dependency for database session


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(course.router, prefix="/course", tags=["course"])
