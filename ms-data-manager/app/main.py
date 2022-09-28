from fastapi import FastAPI, Path
from fastapi_utils.tasks import repeat_every
from app.db import mongodb
from datetime import datetime


app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/routers_history/{router_id}")
async def routers_history(router_id):

    routers = mongodb.collection_routers_history.find(
        {'router_id': router_id})
    total = []

    for router in routers:
        router.pop('_id')
        total.append(router)

    return total


@app.get("/routers/{router_id}")
async def routers_id(router_id):

    router = mongodb.collection_routers.find_one(
        {'router_id': router_id})

    router.pop('_id')

    return router


@app.get("/routers/")
async def routers():

    routers = mongodb.collection_routers.find(
        {})
    total = []

    for router in routers:
        router.pop('_id')
        total.append(router)

    return total


@app.get("/routers_state/{router_id}")
async def routers_state_id(router_id):

    router = mongodb.collection_routers_state.find_one(
        {'router_id': router_id})

    router.pop('_id')

    return router


@app.get("/routers_state/")
async def routers_state():

    routers = mongodb.collection_routers_state.find(
        {})
    total = []

    for router in routers:
        router.pop('_id')
        total.append(router)

    return total
