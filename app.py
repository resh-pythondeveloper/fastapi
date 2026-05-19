from fastapi import FastAPI,HTTPException
from passlib.context import CryptContext
from db import database,engine,metadata
from models import users
from schemas import Usercreate,UserLogin

app=FastAPI()
metadata.create_all(engine)

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/register")
async def register(user:Usercreate):
    query=users.select().where(users.c.username==user.username)
    existing_user=await database.fetch_one(query)
    if existing_user:
        return HTTPException(status_code=400,detail="username already exists")
    hashed_password=pwd_context.hash(user.password)
    query=users.insert().values(username=user.username,password=hashed_password)
    await database.execute(query)
    return {"message":"user register successfully"}

@app.post("/login")
async def login(user:UserLogin):
    query=users.select().where(users.c.username==user.username)
    existing_user=await database.fetch_one(query)
    if not existing_user:
        raise HTTPException(status_code=400,detail="username not found")
    if not pwd_context.verify(user.password,existing_user["password"]):
        raise HTTPException(status_code=400,detail="password invalid")
    return {"message":"login successfully"}