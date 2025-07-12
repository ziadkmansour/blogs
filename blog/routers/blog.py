from fastapi import APIRouter
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from typing import List
from ..controllers import blog as blog_controller

router = APIRouter(tags=["blogs"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.BlogOut)
def create_blog(blog: schemas.Blog, db: Session = Depends(get_db)):
    return blog_controller.create_blog(blog, db)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.BlogOut])
def get_blogs(db: Session = Depends(get_db)):
    return blog_controller.get_blogs(db)

@router.get("/{blog_id}", status_code=status.HTTP_200_OK, response_model=schemas.BlogOut)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    return blog_controller.get_blog(blog_id, db)

@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    blog_controller.delete_blog(blog_id, db)

@router.put("/{blog_id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.BlogOut)
def update_blog(blog_id: int, blog: schemas.BlogOut, db: Session = Depends(get_db)):
    return blog_controller.update_blog(blog_id, blog)