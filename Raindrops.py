collections = {}


def add_collection(collection):
    collections[collection['_id']] = {
        "id": collection['_id'],
        "name": collection['title'],
        "created": collection['created'],
        "last_update": collection['lastUpdate'],
        "count": collection['count'],
        "bookmarks": []
    }


def add_bookmarks(collection_id, bookmarks):
    collections[collection_id]['bookmarks'] = format_bookmarks(bookmarks)


def format_bookmarks(bookmarks):
    result = []
    for b in bookmarks:
        result.append({
            "id": b['_id'],
            "title": b['title'],
            "link": b['link'],
            "created": b['created']
        })
    return result
