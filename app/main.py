from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)
# this command told sqlalchemy to generate all the tables which we dont need since we have alembic

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware, #middleware is basically a function taht runs before every request
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router) #grabbing the router object from the separate files to use the functions
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "hello, world"}






