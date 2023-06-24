import os
from enum import Enum
import motor.motor_asyncio
from bson.objectid import ObjectId

mongo_host = os.environ["MONGO_HOST"]
MONGO_DETAILS = f"mongodb://admin:admin@{mongo_host}:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.data

videos_collection = database.get_collection("videos")


class StatusEnum(str, Enum):
    uploaded = "uploaded"
    processing = "processing"
    ready = "ready"
    error = "error"


async def add_video_data(video):
    video['status'] = StatusEnum.uploaded
    await videos_collection.insert_one(video)


async def get_video_list_data():
    videos = []
    async for video in videos_collection.find():
        video['_id'] = str(video['_id'])
        if 'bar_data' in video:
            del video['bar_data']
        if 'line_data' in video:
            del video['line_data']
        videos.append(video)
    return videos


async def get_video_card_data(_id):
    card = await videos_collection.find_one({'_id': ObjectId(_id)})
    if card is not None:
        card['_id'] = str(card['_id'])
    line_data = {
        'Грузовик': {'Активность':[0]*100 + [1]*50 + [0]*100},
        'Трактор': {'Активность':[0]*100 + [1]*50 + [0]*100}
    }
    card['line_data'] = line_data
    return card


async def get_analytics_data(filter_type: str=None, filter_value: str=None, group:str=None):
    return []