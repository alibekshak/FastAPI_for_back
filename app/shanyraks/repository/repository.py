from typing import Optional, List
from datetime import datetime
from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import DeleteResult, UpdateResult


class ShanyrakRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, user_id: str, shanyrak: dict):
        payload = {
            "user_id": user_id,
            "type": shanyrak["type"],
            "price": shanyrak["price"],
            "address": shanyrak["address"],
            "area": shanyrak["area"],
            "rooms_count": shanyrak["rooms_count"],
            "description": shanyrak["description"],
            "created_at": datetime.utcnow(),
        }

        data = self.database["shanyraks"].insert_one(payload)
        return str(data.inserted_id)

    def get_shanyrak_by_id(self, shanyrak_id: str, user_id: str) -> Optional[dict]:
        shanyrak = self.database["shanyraks"].find_one(
            {"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)}
        )
        return shanyrak

    def get_shanyraks(self, user_id: str) -> dict | None:
        shanyraks = self.database["shanyraks"].find_one({"user_id": ObjectId(user_id)})
        return shanyraks
    
    def update_shanyrak_by_id(self, shanyrak_id: str, user_id: str, data: dict) -> UpdateResult:
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id),
                    "user_id": ObjectId(user_id)},
            update={
                "$set": data,
            },
        )

    def delete_shanyrak_by_id(self, shanyrak_id: str, user_id: str) -> DeleteResult:
        return self.database["shanyraks"].delete_one(
            {"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)}
        )
