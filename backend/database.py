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
        if 'recognition_results' in video:
            del video['recognition_results']
        videos.append(video)
    return videos


async def get_video_card_data(_id):
    card = await videos_collection.find_one({'_id': ObjectId(_id)})
    if card is not None:
        card['_id'] = str(card['_id'])
    if 'recognition_results' in card:
        class2name = {
            'crane': "Подъемный кран",
            'truck': 'Грузовой автомобиль',
            'tractor': 'Трактор',
            'digger': 'Экскаватор'
        }
        line_data = {}
        for rec in card['recognition_results']['data']:
            for det in rec['detections']:
                line_data.setdefault(f'{det["tracking_id"]} {class2name[det["class_name"]]}', {}).setdefault('Активность', []).append(det['activity'])
        # line_data = {
        #     'Грузовик': {'Активность':[0]*100 + [1]*50 + [0]*100},
        #     'Трактор': {'Активность':[0]*100 + [1]*50 + [0]*100}
        # }
        card['line_data'] = line_data
    return card


async def get_analytics_data(filter_type: str=None, group:str=None):
    if filter_type == '':
        filter_type = None
    if group == '':
        group = None

    if filter_type is None and group is None:
        data = {}
        sdata = {}
        async for video in videos_collection.find():
            if video['status'] != StatusEnum.ready:
                continue
            used_id = set()
            if video['date'] not in data:
                data[video['date']] = 0
            if video['date'] not in sdata:
                sdata[video['date']] = 0
            for rec in video['json_res']:
                if rec['id'] not in used_id and rec['type'] != 'простой':
                    used_id.add(rec['id'])
                    data[video['date']] += 1
                if rec['type'] != 'простой':
                    sdata[video['date']] += 1
        line_data = {
            'Количество используемой техники': [data[i] for i in sorted(data)],
            'Количество простоев': [sdata[i] for i in sorted(sdata)],
        }
        return line_data

    elif filter_type is not None and group is None: 
        data = {}
        sdata = {}
        async for video in videos_collection.find({'construction_object': filter_type}):
            if video['status'] != StatusEnum.ready:
                continue
            used_id = set()
            if video['date'] not in data:
                data[video['date']] = 0
            if video['date'] not in sdata:
                sdata[video['date']] = 0
            for rec in video['json_res']:
                if rec['id'] not in used_id:
                    used_id.add(rec['id'])
                    data[video['date']] += 1
                if rec['type'] == 'простой':
                    sdata[video['date']] += 1
        line_data = {
            'Количество используемой техники': [data[i] for i in sorted(data)],
            'Количество простоев': [sdata[i] for i in sorted(sdata)],
        }
        return line_data  
     
    elif filter_type is None and group is not None:
        data = {}
        sdata = {}
        async for video in videos_collection.find():
            if video['status'] != StatusEnum.ready:
                continue
            used_id = set()
            if video['date'] not in data:
                data[video['date']] = 0
            if video['date'] not in sdata:
                sdata[video['date']] = 0
            for rec in video['json_res']:
                if rec['id'] not in used_id and rec['class'] == group:
                    used_id.add(rec['id'])
                    data[video['date']] += 1
                if rec['type'] == 'простой' and rec['class'] == group:
                    sdata[video['date']] += 1
        line_data = {
            'Количество используемой техники': [data[i] for i in sorted(data)],
            'Количество простоев': [sdata[i] for i in sorted(sdata)],
        }
        return line_data
    
    else:
        data = {}
        sdata = {}
        async for video in videos_collection.find({'construction_object': filter_type}):
            if video['status'] != StatusEnum.ready:
                continue
            used_id = set()
            if video['date'] not in data:
                data[video['date']] = 0
            if video['date'] not in sdata:
                sdata[video['date']] = 0
            for rec in video['json_res']:
                if rec['id'] not in used_id and rec['class'] == group:
                    used_id.add(rec['id'])
                    data[video['date']] += 1
                if rec['type'] == 'простой' and rec['class'] == group:
                    sdata[video['date']] += 1
        line_data = {
            'Количество используемой техники': [data[i] for i in sorted(data)],
            'Количество простоев': [sdata[i] for i in sorted(sdata)],
        }
        return line_data
