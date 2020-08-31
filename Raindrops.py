import random
import pytz as pytz

from auth_operations import r
from datetime import datetime
from pymongo import MongoClient

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

collections = {}

client = MongoClient('mongodb://localhost:27017/')
db = client.DigestAppDB


def print_posts():
    posts = db.posts
    posts.insert_one(
        {"title": "Hello world!", "author": "Marta Pancaldi", "created": datetime.now(), "tags": ['test', 'hello']})
    print(posts.find())


def add_collection(collection):
    found = db.raindrops.find_one({"collection_id": collection['_id']})
    new_datetime = to_datetime(collection['lastUpdate'])
    if not found:
        db.raindrops.insert_one({
            "collection_id": collection['_id'],
            "name": collection['title'],
            "created": to_datetime(collection['created']),
            "last_update": new_datetime,
            "count": collection['count'],
            "bookmarks": []
        })
    else:
        existing_last_update = found['last_update']
        if new_datetime > existing_last_update:
            db.raindrops.update_one(
                {"collection_id": found['collection_id']},
                {"$set": {"last_update": new_datetime, "count": collection["count"]}}
            )


def read_collections():
    return db.raindrops.find({})


def add_bookmarks(collection_id, bookmarks):
    db.raindrops.update_one(
        {"collection_id": collection_id},
        {"$set": {
            "bookmarks": format_bookmarks(bookmarks)
        }}
    )


def format_bookmarks(bookmarks):
    result = []
    for b in bookmarks:
        if True:
            # if get_last_update_time() < to_datetime(b['lastUpdate']):
            result.append({
                "id": b['_id'],
                "title": b['title'],
                "link": b['link'],
                "created": to_datetime(b['created'])
            })
            # print("New Raindrop added: {}".format(b['title']))

    return result


def get_random_bookmark():
    _, random_collection = random.choice(list(collections.items()))
    return random.choice(random_collection['bookmarks'])


def update_time():
    r.set('last_update', datetime.now().astimezone(pytz.UTC).strftime(DATETIME_FORMAT))


def get_last_update_time():
    return to_datetime(r.get('last_update'))


def to_datetime(time_string):
    return datetime.strptime(time_string, DATETIME_FORMAT)
