import os

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection


class MongoConnector:
    _URL = os.getenv("MONGO_URL")

    def __init__(self):
        client = AsyncIOMotorClient(self._URL)
        db = client.db
        self._collection: AsyncIOMotorCollection = db.quiz

    async def create_quiz(self, chat_id: int, message_id: int, name: str):
        await self._collection.insert_one({
            "chat_id": chat_id,
            "message_id": message_id,
            "name": name,
            "options": []
        })

    async def create_quiz_option(self, chat_id: int, quiz_message_id: int, option: str, option_message_id) -> bool:
        result = await self._collection.update_one(
            {"chat_id": chat_id,
             "message_id": quiz_message_id},
            {"$addToSet": {"options": {"name": option, "value": 0, "message_id": option_message_id}}}
        )
        return result.modified_count == 1

    async def cast_vote(self, chat_id: int, quiz_message_id: int, option_message_id: int) -> bool:
        result = await self._collection.update_one(
            {"chat_id": chat_id, "message_id": quiz_message_id},
            {"$inc": {"options.$[elem].value": 1}},
            array_filters=[{"elem.message_id": option_message_id}]
        )
        return result.modified_count == 1

    async def retract_vote(self, chat_id: int, quiz_message_id: int, option_message_id: int) -> bool:
        result = await self._collection.update_one(
            {"chat_id": chat_id, "message_id": quiz_message_id},
            {"$inc": {"options.$[elem].value": -1}},
            upsert=True,
            array_filters=[{"elem.message_id": option_message_id}]
        )
        return result.modified_count == 1

    async def get_quiz_by_quiz_message_id(self, chat_id: int, quiz_message_id: int) -> dict:
        result = await self._collection.find_one({
            "chat_id": chat_id,
            "message_id": quiz_message_id
        })
        return result

    async def get_quiz_by_answer_message_id(self, chat_id: int, answer_message_id: int) -> dict:
        result = await self._collection.find_one({
            "chat_id": chat_id,
            "options": {"$elemMatch": {"message_id": answer_message_id}}
        })
        return result

    async def is_option_exists(self, chat_id: int, quiz_message_id: int, option_name: str) -> bool:
        result = await self._collection.find_one({
            "chat_id": chat_id,
            "message_id": quiz_message_id,
            "options": {"$elemMatch": {"name": option_name}}
        })
        return result is not None
