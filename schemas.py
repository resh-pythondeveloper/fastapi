from pydantic import BaseModel

class Usercreate(BaseModel):
    username:str
    password:str

class UserLogin(BaseModel):
    username:str
    password:str