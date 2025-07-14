from fastapi import FastAPI
from . import models
from .database import engine
from .routers import blog, user, authentication


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(authentication.router, prefix="/auth", tags=["authentication"])
app.include_router(blog.router, prefix="/blogs", tags=["blogs"])
app.include_router(user.router, prefix="/users", tags=["users"])

