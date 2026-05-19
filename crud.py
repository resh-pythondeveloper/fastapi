from fastapi import FastAPI
from db2 import Base,sessionLocal,engine,metadata
from pydantic import BaseModel
from model2 import Item

app=FastAPI()

Base.metadata.create_all(bind=engine)

class Itemschema(BaseModel):
    name:str
    price:float
    quantity:int

@app.post('/items/')
def create_item(item:Itemschema):
    db=sessionLocal()
    db_item=Item(name=item.name,quantity=item.quantity,price=item.price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    db.close()
    return db_item

@app.get('/items/{item_id}')
def get_item(item_id:int):
    db=sessionLocal()
    item=db.query(Item).filter(Item.id==item_id).first()
    db.close()
    if not item:
        return {"error":"Item not found"}
    return item

@app.put('/items/{item_id}')
def update_item(item_id:int,item:Itemschema):
    db=sessionLocal()
    db_item=db.query(Item).filter(Item.id==item_id).first()
    if not db_item:
        db.close()
        return {"error":"Item not found"}
    db_item.name=item.name
    db_item.price=item.price
    db_item.quantity=item.quantity
    db.commit()
    db.refresh(db_item)
    db.close()
    return db_item

@app.delete('/items/{item_id}')
def delete_item(item_id:int):
    db=sessionLocal()
    db_item=db.query(Item).filter(Item.id==item_id).first()
    if not db_item:
        db.close()
        return {"error":"Item not found"}
    db.delete(db_item)
    db.commit()
    db.close()
    return {"message":"Item deleted successfully"}
