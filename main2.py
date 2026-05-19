from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()

class Item(BaseModel):
    name:str
    price:float
    password:str

class ItemResponse(BaseModel):
    name:str
    price:float

@app.post("/items1/",response_model=ItemResponse)
def create_item(item:Item):
    return item