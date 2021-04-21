from typing import List

from beanie import Document
from pydantic.main import BaseModel


class Nutrition(BaseModel):
    energy: float
    fat: float
    protein: float
    carbs: float


class IceCream(Document):
    name: str
    price: float
    summary: str
    description: str
    ingredients: List[str]
    per_100_gr: Nutrition

    class Collection:
        name = "ice-cream"


class IceCreamShort(Document):
    name: str
    price: float
    summary: str

    class Collection:
        name = "ice-cream"
