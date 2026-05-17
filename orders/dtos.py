from pydantic import BaseModel


class OrderCreate(BaseModel):
    name: str
