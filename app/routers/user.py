from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import engine, sessionLocal, get_db
from typing import List

router = APIRouter(
    # prefix="/users",
    tags=['Users']
)

# users routes from here

@router.get("/users", status_code=status.HTTP_200_OK, response_model=List[schemas.GetUsers])
async def get_users(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    get_all_users = db.query(models.User).all()

    return get_all_users

@router.post("/users", status_code=status.HTTP_201_CREATED ,response_model=schemas.UserResp)
async def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    # checking for user name, if it already exists or not.
    user_name_check = db.query(models.User).filter(models.User.name == user.name).first()
    # checking for user email, if it already exists or not.
    user_email_check = db.query(models.User).filter(models.User.email == user.email).first()
    if user_name_check or user_email_check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=" user already exists! ")
    else:
        # hashing the password / adding security and stored it in variable called hashing_pwd.
        # hashing_pwd = pwd_context.hash(user.password)
        # user.password = hashing_pwd
        hashing_pwd = utils.hash_pwd(user.password)
        user.password = hashing_pwd
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    return new_user

@router.get("/users/userId", status_code=status.HTTP_200_OK, response_model=schemas.UserResp)
async def getUsers(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    get_user_first = db.query(models.User).filter(models.User.user_id == current_user.user_id).first()
    
    if not get_user_first:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {current_user.user_id} doesn't exists")

    return get_user_first

@router.delete("/users/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_from_user(user_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    id_to_delete = db.query(models.User).filter(models.User.user_id == user_id)
    
    if user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"user {current_user.name} your not authorized to perform this task!")

    if id_to_delete.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {user_id} doesn't eixsts")
    
    id_to_delete.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/users/patch/{user_id}")
async def patch_user(user_id: int, data: dict, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if data.get('password'):
        raise HTTPException(detail="Not Allowed Method go to http://127.0.0.1:8000/user/patch/password/{user_id}", status_code=status.HTTP_403_FORBIDDEN)
    user = db.query(models.User).filter(models.User.user_id == user_id)
    user_first = user.first()
    if user_first.name != current_user.name:
        raise HTTPException(detail=f"user {current_user.name} your not authorized to perform this action", status_code=status.HTTP_403_FORBIDDEN)
    if not user_first:
        raise HTTPException(detail=f"user with id {user_id} doesn't exists!")
    user.update(data)
    db.commit()
    return user.first()