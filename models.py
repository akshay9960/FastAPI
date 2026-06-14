from pydantic import BaseModel



class My_Product(BaseModel):
    id:int
    name:str
    description:str
    price:float
    quantity:int