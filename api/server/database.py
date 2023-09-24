from typing import List, Optional

import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb+srv://nickolayb11:x7GJAZb7uFY8YwpE@mirea.lnyb0c7.mongodb.net/?retryWrites=true&w=majority"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.api_testing

contact_collection = database.get_collection("contacts")


def contact_helper(contact) -> dict:
    return {
        "id": str(contact["_id"]),
        "username": contact["username"],
        "email": contact["email"],
        "mobile telephone": contact["tel_mobile"],
        "home telephone": contact["tel_home"]
    }


# Извлечь все контакты из БД
async def retrieve_contacts() -> List[dict]:
    contacts = []
    async for contact in contact_collection.find():
        contacts.append(contact_helper(contact))
    return contacts


# Добавить новый контакт
async def add_contact(contact_data: dict) -> dict:
    contact = await contact_collection.insert_one(contact_data)
    new_contact = await contact_collection.find_one({"_id": contact.inserted_id})
    return contact_helper(new_contact)


# Извлечь контакт по id
async def retrieve_contact(contact_id: str) -> Optional[dict]:
    contact = await contact_collection.find_one({"_id": ObjectId(contact_id)})
    if contact:
        return contact_helper(contact)


# Обновить контакт по id
async def update_contact(contact_id: str, data: dict) -> bool:
    if not data:
        return False
    contact = await contact_collection.find_one({"_id": ObjectId(contact_id)})
    if contact:
        updated_contact = await contact_collection.update_one({"_id": ObjectId(contact_id)}, {"$set": data})
        return True if updated_contact else False


# Удалить контакт
async def delete_contact(contact_id: str) -> bool:
    contact = await contact_collection.find_one({"_id": ObjectId(contact_id)})
    if contact:
        await contact_collection.delete_one({"_id": ObjectId(contact_id)})
        return True
    return False
