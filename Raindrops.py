from datetime import datetime

import pytz as pytz

from auth_operations import r

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

collections = {}


def add_collection(collection):
    collections[collection['_id']] = {
        "id": collection['_id'],
        "name": collection['title'],
        "created": to_datetime(collection['created']),
        "last_update": to_datetime(collection['lastUpdate']),
        "count": collection['count'],
        "bookmarks": []
    }


def add_bookmarks(collection_id, bookmarks):
    collections[collection_id]['bookmarks'] = format_bookmarks(bookmarks)


def format_bookmarks(bookmarks):
    result = []
    for b in bookmarks:
        if get_last_update_time() < to_datetime(b['lastUpdate']):
            result.append({
                "id": b['_id'],
                "title": b['title'],
                "link": b['link'],
                "created": to_datetime(b['created'])
            })
            print("New Raindrop added: {}".format(b['title']))

    return result


def update_time():
    r.set('last_update', datetime.now().astimezone(pytz.UTC).strftime(DATETIME_FORMAT))


def get_last_update_time():
    return to_datetime(r.get('last_update'))


def to_datetime(time_string):
    return datetime.strptime(time_string, DATETIME_FORMAT)
