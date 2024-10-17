from schema.schemas import Token,UserOut,UserCreate
from utils import password_utils,token_utils
from database.get_db import get_db
from database.models import models
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


user_router = APIRouter(
    prefix="/users",
    tags=['Users'] # Giving title and grouping in the documentation
)


@user_router.post("/login", response_model=Token)
# def login(user_credential: schemas.UserLogin, db: Session = Depends(database.get_db)):
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # user = db.query(models.User).filter(models.User.email == user_credential.email).first()

    # when retreaving user credential from OAuth2PasswordRequestForm the email is stored in field called username
    # and it only return 2 thing {"username": "abcd", "password": "abcd"}
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credential")

    if not password_utils.verify_pwd(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credential")

    # Create a token
    # return token
    access_token = token_utils.create_access_token(data={"user_id": user.id})  # the data is the payload, you can add what you want

    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id}

@user_router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)): # see schemas.py to see the key
    # get the email from db to ensure the email does not exist
    user_query = db.query(models.User).filter(models.User.email == user.email).first()
    
    if not user_query:
        if user.password != "":
            # hash the password
            hashed_password = password_utils.hash_pwd(user.password)
            user.password = hashed_password

            new_user = models.User(**user.dict()) # this will unpack the post dict to be formatted like above
            db.add(new_user)
            db.commit()
            db.refresh(new_user) 
            return new_user
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="请输入密码！")
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="邮箱已经被注册!")
    

@user_router.get('/{id}', response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id}, does not exist!")
    
    return user

