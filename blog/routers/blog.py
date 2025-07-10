from fastapi import APIRouter
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from typing import List

router = APIRouter(tags=["blogs"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.BlogOut)
def create_blog(blog: schemas.Blog, db: Session = Depends(get_db)) -> dict:
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.BlogOut])
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.get("/{blog_id}", status_code=status.HTTP_200_OK, response_model=schemas.BlogOut)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found"
        )
    return blog

@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    deleted_count = db.query(models.Blog).filter(models.Blog.id == blog_id).delete(synchronize_session=False)

    if deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found"
        )

    db.commit()

@router.put("/{blog_id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.BlogOut)
def update_blog(blog_id: int, blog: schemas.BlogOut, db: Session = Depends(get_db)):
    result = db.query(models.Blog).filter(models.Blog.id == blog_id).update(blog.model_dump(), synchronize_session="fetch")

    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found"
        )

    db.commit()

    updated_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    return updated_blog