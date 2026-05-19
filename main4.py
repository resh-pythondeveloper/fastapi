DATABASE_URL="postgresql://postgres:django@localhost:5432/fastapi"


from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel,Field,create_engine,Session,select
from typing import Optional,List

class Item(SQLModel,table=True):
    id:Optional[int]=Field(default=None,primary_key=True)
    name:str
    price:float

engine=create_engine(DATABASE_URL,echo=True)

def create_db_and_table():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_and_table()
    yield

app=FastAPI(lifespan=lifespan)

@app.post("/items/")
def create_item(item:Item):
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item
    
@app.get("/items/",response_model=List[Item])
def get_item():
    with Session(engine) as session:
        items=session.exec(select(Item)).all()
        return items
