from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


fake_items_db = [{"item_name": "Foo"}, {
    "item_name": "Bar"}, {"item_name": "Baz"}]


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id):
    return {"user_id": user_id}


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    response = {"item_id": item_id}
    if q:
        response["q"] = q
    if not short:
        response["description"] = "This is an amazing item that has a long description"
    return response


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    message_default = "Have some residuals"
    message_map = {
        ModelName.alexnet: "Deep Learning FTW!",
        ModelName.lenet: "LeCnn all the images",
    }

    message = message_map.get(model_name, message_default)

    return {"model_name": model_name, "message": message}


@app.post("/items/")
async def create_item(item=Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.price.update({"price_with_tax": price_with_tax})


@app.put("/item/{item_id}")
async def create_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


@app.options("/")
async def options():
    return {"allowed-methods": ["GET", "OPTIONS"]}
