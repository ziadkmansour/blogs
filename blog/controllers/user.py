from .. import models, schemas
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from ..utils import passwordHasher

def create_user(user: schemas.User, db: Session):
    new_user = models.User(**user.model_dump(exclude={"password"}), password=passwordHasher.hash(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(user_id: int, db: Session, current_user_id: int):
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user"
        )
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user