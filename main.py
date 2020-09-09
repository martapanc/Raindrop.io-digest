import requests

from Raindrops import collections, add_collection, add_bookmarks, update_time, get_random_bookmark, read_collections, \
    read_bookmarks_of_last_days, get_random
from auth_operations import get_auth_header
from datetime import datetime, timedelta

auth_header = get_auth_header()


def get_collections():
    url = "https://api.raindrop.io/rest/v1/collections"

    collections_rs = requests.get(url, headers=auth_header).json()
    if collections_rs['items']:
        for coll in collections_rs['items']:
            add_collection(coll)


def get_bookmarks():
    for coll in read_collections():
        coll_id = coll['collection_id']
        url = "https://api.raindrop.io/rest/v1/raindrops/{}".format(coll_id)

        raindrops_rs = requests.get(url, headers=auth_header).json()
        add_bookmarks(coll_id, raindrops_rs['items'])

    update_time()


def build_bookmarks_collection():
    get_collections()
    get_bookmarks()


def get_bookmarks_added_in_last_days(days):
    date_since = datetime.now() - timedelta(days=days)
    for coll_id, collection in collections.items():
        if collection['last_update'] > date_since:
            for bookmark in collection['bookmarks']:
                if bookmark['created'] > date_since:
                    print("Raindrop {} added in collection {}".format(bookmark['title'], collection['name']))


def get_random_bookmarks(number):
    bookmarks = []

    while len(bookmarks) < number:
        random_bookmark = get_random_bookmark()
        if random_bookmark['id'] not in [j['id'] for j in bookmarks]:
            bookmarks.append(random_bookmark)

    return bookmarks


def get_random_bookmarks_in_last_days(number, days):
    bookmarks = []

    recent_bookmarks = [b for b in read_bookmarks_of_last_days(days)]

    if len(recent_bookmarks) <= number or number == 0:
        for b in recent_bookmarks:
            bookmarks.append(b['bookmark'])
    else:
        while len(bookmarks) < number:
            random = get_random(recent_bookmarks)
            if random['bookmark']['id'] not in [k['id'] for k in bookmarks]:
                bookmarks.append(random['bookmark'])

    return bookmarks


if __name__ == '__main__':
    build_bookmarks_collection()
