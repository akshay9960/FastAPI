from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from models import My_Product
from database import session,engine
import database_model
from sqlalchemy.orm import Session

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
database_model.Base.metadata.create_all(bind=engine)





@app.get("/")
def greet():
    return "Welcome Akshay to FastAPI"

Products=[
My_Product(id=1,name="pen",description="blue pen",price=10.0,quantity=50),
My_Product(id=2,name="ball",description="football",price=40.0,quantity=100)
]

def get_db():
    db=session()
    try:
        yield db
    finally:    
        db.close()


def int_db():
    db=session()
    count =db.query(database_model.My_Product).count()
    if count==0:
        for product in Products:
            db.add(database_model.My_Product(**product.model_dump()))
        db.commit()

int_db()    

@app.get("/products")
def get_all_products(db:Session=Depends(get_db)):
    db_products=db.query(database_model.My_Product).all()
    return db_products

@app.get("/products/{id}")
def get_product_by_id(id:int,db:Session=Depends(get_db)):
   db_product=db.query(database_model.My_Product).filter(database_model.My_Product.id==id).first()
   if db_product:
        return db_product
        
   return "product not found by id"       

@app.post("/products")
def add_product(product:My_Product,db:Session=Depends(get_db)):
    db.add(database_model.My_Product(**product.model_dump()))
    db.commit()
    return product
 
@app.put("/products/{id}")
def update_product(id:int,product:My_Product,db:Session=Depends(get_db)):
    db_product=db.query(database_model.My_Product).filter(database_model.My_Product.id==id).first()

    if db_product:
            db_product.name=product.name
            db_product.description=product.description
            db_product.price=product.price
            db_product.quantity=product.quantity
            db.commit()
            return "product updated successfully"
    else:
        return "product not found"

@app.delete("/products/{id}")
def delete_product(id:int,db:Session=Depends(get_db)):
    db_product=db.query(database_model.My_Product).filter(database_model.My_Product.id==id).first()

    if db_product:
          db.delete(db_product)
          db.commit()
          return "product deleted successfully"
    else:
        return "product not found"
        
