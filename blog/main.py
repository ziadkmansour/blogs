from fastapi import FastAPI, Depends, status, HTTPException
from . import models, schemas
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .utils import PasswordHasher


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)
hasher = PasswordHasher()

app = FastAPI()

@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create_blog(blog: schemas.Blog, db: Session = Depends(get_db)) -> dict:
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"message": "Blog created successfully", "blog": new_blog}

@app.get("/blogs", status_code=status.HTTP_200_OK, response_model=schemas.Blogs)
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return {"blogs": blogs}

@app.get("/blog/{blog_id}", status_code=status.HTTP_200_OK, response_model=schemas.Blog)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found"
        )
    return blog

@app.delete("/blog/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    deleted_count = db.query(models.Blog).filter(models.Blog.id == blog_id).delete(synchronize_session=False)

    if deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found"
        )

    db.commit()

@app.put("/blog/{blog_id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Blog)
def update_blog(blog_id: int, blog: schemas.Blog, db: Session = Depends(get_db)):
    result = db.query(models.Blog).filter(models.Blog.id == blog_id).update(blog.model_dump(), synchronize_session="fetch")

    if result == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found"
        )

    db.commit()

    updated_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    return updated_blog

@app.post("/user", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(**user.model_dump(exclude={"password"}), password=hasher.hash(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user