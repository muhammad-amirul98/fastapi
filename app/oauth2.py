from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") #endpoint url
#secret key, algorithm, expiration time of token to dictate how long user is logged in 
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy() #dont want to change the data itself
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) #not datetime.now()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM]) #Algorithm does not work if not list
        id = str(payload.get("user_id"))
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentials_exception
    return token_data #basically only the id but we are using a schema such that in the future if we want to include more details itll be easier

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)): #once the verify access token returns the token_data which is the id, the get current user fetches user from db so we can attach the user to any path operation and perform any necessary logic
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    
    token = verify_access_token(token, credentials_exception=credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user