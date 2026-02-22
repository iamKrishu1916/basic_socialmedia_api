from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import vote
from . import models
from .database import engine
from .routers import post, user, auth
from .config import settings

# models.Base.metadata.create_all(bind=engine)
origins = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")  # get: http method,
def root():
    return {
        "message": "Welcomoe to my api!"
    }  # this python dict will automatically gets converted to JSON(main lang. of apis)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
