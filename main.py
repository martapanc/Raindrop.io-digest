import requests

from Raindrops import collections, add_collection, add_bookmarks, update_time, get_random_bookmark, read_collections
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
    for _i in range(1, number):
        print(get_random_bookmark())


if __name__ == '__main__':
    # print_posts()
    build_bookmarks_collection()
    # get_bookmarks_added_in_last_days(7)
    # get_random_bookmarks(10)
