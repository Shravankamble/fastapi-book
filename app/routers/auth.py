from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi_cache.decorator import cache
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post("/auth/login", status_code=status.HTTP_201_CREATED, response_model=schemas.Token)
@cache(expire=120)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    # this HTTPException raises when the user does not exist or not found in the database  
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    """verifying if the password is correct or not |
    when creating a new user the password is hashed for security reasons so we verify the password
    by getting password from the user who is trying to login and check if it does exists or not
    so the problem is you can't just verify the password in simple string and an hashed string stored in the DataBase
    so we take the password from the user who is trying to login and hash his given password and then compare it with 
    the one in the DataBase if it matches then we let the user through or if it doesn't then we raise the below http exception"""
    
    verification = utils.verify(user_credentials.password, user.password)

    if not verification:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = oauth2.create_access_token(data = {"user_id": user.user_id}) 

    return {"access_token": access_token}
    
