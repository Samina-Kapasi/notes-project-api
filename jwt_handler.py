from jose import jwt 
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
from database import SessionLocal
from models import Users

load_dotenv()
SECRET_KEY=os.getenv("SECRET_KEY")


ALGORITHM="HS256"

ACCESS_TOKEN_EXPIRE_TIME=30

def create_access_token(data:dict):

    to_encode=data.copy()

    expire=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)

    to_encode.update({
        "exp":expire
    })

    encode_jwt=jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encode_jwt

Oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

def verify_access_token(token:str):

    try:
        payload=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=ALGORITHM
        )
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid Token")
    
def get_current_user(token:str=Depends(Oauth2_scheme)):

    payload=verify_access_token(token)

    email=payload.get("sub")

    db=SessionLocal()

    user=db.query(Users).filter(Users.email==email).first()

    return user