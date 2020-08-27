import requests

from Raindrops import collections, add_collection, add_bookmarks
from auth_operations import get_auth_header

auth_header = get_auth_header()


def get_collections():
    url = "https://api.raindrop.io/rest/v1/collections"

    collections_rs = requests.get(url, headers=auth_header).json()
    if collections_rs['items']:
        for coll in collections_rs['items']:
            add_collection(coll)


def get_bookmarks():
    for coll_id, coll in collections.items():
        url = "https://api.raindrop.io/rest/v1/raindrops/{}".format(coll_id)

        raindrops_rs = requests.get(url, headers=auth_header).json()
        add_bookmarks(coll_id, raindrops_rs['items'])


if __name__ == '__main__':
    get_collections()
    get_bookmarks()
