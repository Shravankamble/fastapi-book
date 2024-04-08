from passlib.context import CryptContext

# This function is used hash The password so the password would be more secure
# for hashing we used the passlib module
# only the user knows the password
# we used bcrypt algorithm to hash the password you can use any, there are a lot out there
# for more context visit the passlib Documentation

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pwd(pwd: str) -> str:
    hashing_pwd = pwd_context.hash(pwd)
    return hashing_pwd

def verify(raw_pwd, hashed_pwd):
    return pwd_context.verify(raw_pwd, hashed_pwd)
