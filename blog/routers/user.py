from fastapi import APIRouter
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from ..utils import PasswordHasher


hasher = PasswordHasher()

router = APIRouter(tags=["users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(**user.model_dump(exclude={"password"}), password=hasher.hash(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user