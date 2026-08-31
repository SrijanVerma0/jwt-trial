from fastapi import APIRouter,Depends,HTTPException
from sqlmodel import Session
from sqlalchemy import select

from db import User,get_session,hash_password,verify_password,create_access_token

router = APIRouter()

class LoginRequest:
    def __init__(self,username:str,password:str):
        self.username = username
        self.password = password
        
@router.post("/signup")
def sign_up(username:str,password:str,session:Session = Depends(get_session)):
    existing_user = session.execute(select(User).where(User.username == username)).scalars().first()
    if existing_user:
        raise HTTPException(status_code = 400,detail = "Username already exists")
    
    hashed_password = hash_password(password)
    new_user = User(username = username ,hashed_password = hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message":"User created successfully"}

@router.post("/login")

def login(username:str,password:str,session:Session = Depends(get_session)):
    user = session.execute(select(User).where(User.username == username)).scalars().first()
    if not user:
        raise HTTPException(status_code=400,detail = "incorrect username or password")
    if not verify_password(password,user.hashed_password):
        raise HTTPException(status_code = 400,detail = "incorrect username or password")
    access_token = create_access_token(data = {"sub":username})
    return {"access_token" : access_token ,"token_type": "bearer"}

    

    
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from db import SECRET_KEY, ALGORITHM  # SECRET_KEY aur ALGORITHM import karein

    

def verify_token(token: str):
    try:
        # 1 min ke andar decode ho jayega
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        # 1 min baad jwt yahan error throw karega
        raise HTTPException(status_code=401, detail="Token has expired! Please login again.")


# Yeh raha protected route jisse aap check karenge
@router.get("/profile")
def get_profile(current_user: str = Depends(verify_token)):
    return {"message": f"Hello {current_user}, your token is active and valid!"}

   
