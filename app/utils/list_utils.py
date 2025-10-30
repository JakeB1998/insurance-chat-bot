def remove_item(collection: list, item, safe_remove: bool = True):
    if collection is None:
        raise TypeError("collection cannot be None")

    try:
        collection.remove(item)
    except ValueError:
        if not safe_remove:
            raise e