from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, like
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Backend system design"
)

# The Real CRUD application starts from here the other ones are only for getting the idea of how the routes are gonna be,
# and how to exchange data from one location to another.

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(like.router)


@app.get("/")
async def root():
    return {"message": "hello world!"}

