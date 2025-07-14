from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import status, HTTPException


def get_blogs(db: Session, user_id: int):
    blogs = db.query(models.Blog).filter(models.Blog.user_id == user_id).all()
    return blogs

def create_blog(blog: schemas.Blog, db: Session, user_id: int):
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def delete_blog(blog_id: int, db: Session, user_id: int):
    deleted_count = db.query(models.Blog).filter(models.Blog.id == blog_id, models.Blog.user_id == user_id).delete(synchronize_session=False)

    if deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found"
        )

    db.commit()

def get_blog(blog_id: int, db: Session, user_id: int):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id, models.Blog.user_id == user_id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found"
        )
    return blog

def update_blog(blog_id: int, blog: schemas.BlogOut, db: Session, user_id: int):
    result = db.query(models.Blog).filter(models.Blog.id == blog_id, models.Blog.user_id == user_id).update(blog.model_dump(), synchronize_session="fetch")

    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found"
        )

    db.commit()

    updated_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    return updated_blog