from fastapi import FastAPI
import os
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from redis_om import get_redis_connection, HashModel


load_dotenv()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # allow_origins="http://localhost:8000",
    # allow_methods=["*"],
    # allow_headers=["*"],
)

redis = get_redis_connection(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True,
)


class Product(HashModel):
    name: str
    price: float
    description: str
    quantity: int

    class Meta:
        database = redis


class ProductCreate(BaseModel):
    name: str
    price: float
    description: str
    quantity: int


# get all product
@app.get("/")
async def root():
    return [format(pk) for pk in Product.all_pks()]


def format(pk: str):
    product = Product.get(pk)
    return {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "quantity": product.quantity,
    }


# create product
@app.post("/product")
async def create_product(product: ProductCreate):
    new_product = Product(**product.dict())
    new_product.save()
    return new_product


# get single product


@app.get("/product/{id}")
async def get_single_product(id: str):
    return Product.get(id)


@app.delete("/product/{id}")
async def delete_product(id: str):
    return Product.delete(id)
