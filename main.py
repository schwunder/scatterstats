from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from scat import scatter_vis

origins = [
    "*",
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    a: str
    b: str
    c: int


@app.get("/items/{item}")
def read_item(item):
    return item

#def str_from_item():



@app.post("/items/")
async def create_item(item: Item):
    result_dir = "results/"
    #if not in /results calculate
    f = scatter_vis(item.a, item.b, item.c)
    filename = str(item.a.split("/")[-1]) + "-" + str(item.b.split("/")[-1]) + "-" + str(item.c)
    loc = result_dir + filename + ".html"
    open(loc, 'wb').write(f.encode('utf-8'))
    return loc

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.post("/items/")
# async def create_item(item: Item):
#     g = get_page_lists(item.a, item.b)
#     return g
