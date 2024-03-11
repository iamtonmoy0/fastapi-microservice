from fastapi import FastAPI
import os
import time
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from starlette.requests import Request
from redis_om import get_redis_connection, HashModel
import requests


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


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str

    class Meta:
        database = redis


@app.post("/orders")
async def create_order(request: Request):
    body = await request.json()
    req = requests.get("http://localhost:8000/product/" % body["id"])
    product = req.json()

    order = Order(
        product_id=body["id"],
        price=product["price"],
        fee=product["price"] * 0.2,
        total=1.2 * product["price"],
        quantity=body["quantity"],
        status="pending",
    )
    order.save()
    return order


def order_completed(order: Order):
    time.sleep(5)
    order.status = "completed"
    order.save()
