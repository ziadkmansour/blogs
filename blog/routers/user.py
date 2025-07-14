from fastapi import APIRouter
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, status
from ..controllers import user as user_controller
from ..oauth2 import get_current_user


router = APIRouter(tags=["users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    return user_controller.create_user(user, db)

@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(get_current_user)):
    return user_controller.get_user(user_id, db, current_user.user_id)