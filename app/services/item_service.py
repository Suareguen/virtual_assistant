from app.db.mongodb import db
from app.models.item_model import item_serializer
from bson import ObjectId

async def create_item(item_data: dict):
    new_item = await db["mycollection"].insert_one(item_data)
    item = await db["mycollection"].find_one({"_id": new_item.inserted_id})
    return item_serializer(item)

async def get_all_items():
    items = []
    async for item in db["mycollection"].find():
        items.append(item_serializer(item))
    return items

async def get_item(item_id: str):
    item = await db["mycollection"].find_one({"_id": ObjectId(item_id)})
    return item_serializer(item) if item else None

async def update_item(item_id: str, item_data: dict):
    await db["mycollection"].update_one({"_id": ObjectId(item_id)}, {"$set": item_data})
    item = await db["mycollection"].find_one({"_id": ObjectId(item_id)})
    return item_serializer(item) if item else None

async def delete_item(item_id: str):
    item = await db["mycollection"].find_one_and_delete({"_id": ObjectId(item_id)})
    return item_serializer(item) if item else None
