from fastapi import FastAPI
import os
from dotenv import load_dotenv
from redis_om import get_redis_connection, HashModel


load_dotenv()
app = FastAPI()

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


@app.get("/")
async def root():
    return {"message": "hello world"}
