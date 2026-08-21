from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, models, database
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings 

# pull the token from the request header and verify it. If the token is valid, it will return the user_id from the token payload. If the token is invalid or expired, it will raise an HTTPException with a 401 status code.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
#SECERT_KEY
#ALGORITHM
#Expiration time

SECERT_KEY = settings.secret_key
ALGORITHM = settings.algorithm
access_token_expire_minutes = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    # Add expiration time to the token
    expire = datetime.utcnow() + timedelta(minutes=access_token_expire_minutes)
# Add the expiration time to the payload of the token. The "exp" claim is a standard claim in JWT that indicates the expiration time of the token. It is used to determine if the token is still valid or has expired.
# if you change "exp" to "expires" it will not work because the JWT standard expects the claim to be named "exp". If you change it to "expires", the JWT library will not recognize it as a valid expiration claim, and the token will not be considered expired when it should be.
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECERT_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str , credentials_exception):

    try:
        payload =jwt.decode(token, SECERT_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = id
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token).first()
    return user 