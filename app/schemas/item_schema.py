from pydantic import BaseModel

class ItemSchema(BaseModel):
    name: str
    description: str
    price: float
    stock: int
