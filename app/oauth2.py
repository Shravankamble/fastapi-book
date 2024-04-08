from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from . import schemas, database, models
from sqlalchemy.orm import Session
from .config import settings as stg

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

# SECRET KEY
"""this is just a random string, you can put any string you like
   if you want to generate a random secret key you can use this cmd (openssl rand -hex 32) to generate one.
   you can use this secret key for learning purposes
   but never create or show your secret key like this in the codebase
   always use enviroment variables for confidential information and also for best practices
   rand hash : 09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
"""
SECRET_KEY = stg.secret_key

# ALGORITHM
"""you can provide which algorithm you're gonna use, in our case we are gonna use HS256 algorithm
   if you want to know more about HS256 algorithm check (https://www.youtube.com/watch?v=iSStmRn05nA)
   or blog (https://auth0.com/blog/rs256-vs-hs256-whats-the-difference/)
   and also learn what is the difference between HS256 and RS256
"""
ALGORITHM = stg.algorithm

# ACCESS TOKEN EXPIRE TIME
# this is the Expiration time of the token, after 45 minutes the JWT token will get expired 
# check (https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) to get more information.
ACCESS_TOKEN_EXPIRE_TIME = stg.access_token_expire_time

def create_access_token(data: dict):
   to_encode = data.copy()

   current_time = datetime.utcnow()
   expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME) 
   to_encode.update({"iat": current_time})
   to_encode.update({"exp": expire})

   encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

   return encoded_jwt

def verify_access_token(token: str, credentials_exception):
   try:
      decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      id = decoded.get("user_id")

      if id is None:
         raise credentials_exception

      token_data = schemas.TokenData(user_id=id)
   except JWTError:
      raise credentials_exception

   return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
   credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials", headers={"WWWW-Authenticate": "Bearer"})
   token = verify_access_token(token, credentials_exception)

   user = db.query(models.User).filter(models.User.user_id == token.user_id).first()

   return user
