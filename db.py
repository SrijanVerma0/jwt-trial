from sqlmodel import SQLModel,create_engine,Field
from sqlalchemy.orm import Session
from typing import Optional

sqlite_file_name = "tasks.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"


engine = create_engine(
    sqlite_url
)

def create_db_and_table():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

class Task(SQLModel,table = True):

    id: Optional[int] = Field(default = None,primary_key = True)
    title : str = Field(description = "title")
    done : bool = Field(description="done or not")

    

class TaskCreate(SQLModel):
    title: str = Field(description="title")
    done: bool = Field(description="done or not")



#####################################
##########   Authentication  ########
#####################################


from passlib.context import CryptContext
from datetime import datetime,timedelta
from jose import JWTError, jwt


pwd_context = CryptContext(schemes = ["bcrypt"],deprecated = "auto")
SECRET_KEY="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 1


class User(SQLModel,table = True):
    id : Optional[int] = Field(default = None,primary_key = True)
    username : str = Field(index = True,description = "username")
    hashed_password : str = Field(description = "hashed_password")  


def hash_password(password : str):
    return pwd_context.hash(password)
    
def verify_password(plain_password:str,hashed_passwrord:str)->bool:
    return pwd_context.verify(plain_password,hashed_passwrord)

def create_access_token(data:dict,expires_delta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=1)

    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm = ALGORITHM)
    return encoded_jwt


def create_refresh_token(data:dict,expires_delta:Optional[timedelta]=  None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days = 7)
    
    to_encode.update({"exp":expire,"type":"refresh"})
    return jwt.encode(to_encode,SECRET_KEY,algorithm = ALGORITHM)

