from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, models, JWToken
from ..database import get_db
from ..utils import passwordHasher

router = APIRouter(tags=["authentication"])

@router.post("/login", status_code=200, response_model=schemas.Token)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not passwordHasher.verify(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = JWToken.create_access_token(data={"sub": user.username, "user_id": user.id})
    return schemas.Token(access_token=access_token, token_type="bearer")