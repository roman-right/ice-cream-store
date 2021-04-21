from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException

from models import IceCream, IceCreamShort

ice_cream_router = APIRouter()


@ice_cream_router.post("/", response_model=IceCream)
async def new(ice_cream: IceCream):
    await ice_cream.create()
    return ice_cream


@ice_cream_router.get("/{ice_cream_id}", response_model=IceCream)
async def get(ice_cream_id: PydanticObjectId):
    ice_cream = await IceCream.get(ice_cream_id)
    if ice_cream is None:
        raise HTTPException(status_code=404, detail="Ice cream not found")
    return ice_cream


@ice_cream_router.get("/", response_model=List[IceCreamShort])
async def get_list():
    print(await IceCreamShort.find_all().to_list())
    return await IceCreamShort.find_all().to_list()
