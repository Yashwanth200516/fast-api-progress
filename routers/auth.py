from pydantic import BaseModel
from fastapi import APIRouter,HTTPException
from database import user_collection
from utils.security import hash_password,verify_password
from utils.jwt_handler import create_access_token
from models import User

router=APIRouter()

@router.post('/register')
def register_user(user:User):
    existing_username=user_collection.find_one({'username':user.username})
    if existing_username:
        raise HTTPException(
            status_code=400,
            detail='use different username'
        )
    user.password=hash_password(user.password).decode()
    user_collection.insert_one(user.model_dump())
    return {"detail":"user registered successfully"}

@router.post('/login')
def login_user(user:User):
    existing_user=user_collection.find_one({'username':user.username})
    if existing_user:
        stored_hash=existing_user["password"]
        if verify_password(user.password,stored_hash.encode()):
            token=create_access_token(
                {
                    "username":user.username,
                    "role":existing_user["role"]
                }
            )

            return {'access_token':token}
    
    raise HTTPException(
        status_code=401,
        detail='invalid name or password'
    )