from fastapi import Body, FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .. import models, schemas, utils, Oauth2
from ..database import get_db, engine

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
## ""OATh2PasswordRequestForm""" is a class provided by FastAPI that represents the form data sent in an OAuth2 password flow request. It contains two fields: username and password. When a client sends a POST request to the /login endpoint with the appropriate form data, FastAPI automatically parses the request and populates an instance of OAuth2PasswordRequestForm with the provided values.
# This line trips everyone up. OAuth2PasswordRequestForm means this endpoint does not accept JSON. It accepts application/x-www-form-urlencoded form data, with exactly two required fields named username and password.
#So testing in Postman: Body → form-data (or x-www-form-urlencoded), not raw JSON. Send JSON here and you get a 422.
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    USER = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not USER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    if not utils.verify(user_credentials.password, USER.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    # Return a token
    access_token = Oauth2.create_access_token(data={"user_id": USER.id})
    return schemas.Token(access_token=access_token, token_type="bearer")