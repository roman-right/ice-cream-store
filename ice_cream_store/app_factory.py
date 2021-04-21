import motor
from beanie import init_beanie
from fastapi import FastAPI
from pydantic import BaseSettings

from models import IceCream, IceCreamShort
from routes import ice_cream_router

app = FastAPI()


class Settings(BaseSettings):
    mongo_host: str = "localhost"
    mongo_user: str = "beanie"
    mongo_pass: str = "beanie"
    mongo_db: str = "beanie_db"

    @property
    def mongo_dsn(self):
        return f"mongodb://{self.mongo_user}:{self.mongo_pass}@{self.mongo_host}:27017/{self.mongo_db}"


@app.on_event("startup")
async def app_init():
    # CREATE MOTOR CLIENT
    client = motor.motor_asyncio.AsyncIOMotorClient(
        Settings().mongo_dsn
    )

    # INIT BEANIE
    await init_beanie(client.beanie_db,
                      document_models=[IceCream, IceCreamShort])

    # ADD ROUTES
    app.include_router(ice_cream_router, prefix="/ice_cream",
                       tags=["ice_cream"])
