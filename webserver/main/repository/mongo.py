import pymongo

from main.constant import ID
from main.logger.custom_logging import log, log_error


def collection_insert_one(mongo_collection, entry):
    try:
        log(f"Inserting entry to collection {mongo_collection.name}")
        mongo_collection.insert_one(entry)
        log(f"Entry inserted to collection {mongo_collection.name} successfully!")
        return True
    except:
        log_error(f"Entry insertion to collection {mongo_collection.name} failed!")
        return False


def collection_insert_many(mongo_collection, entries):
    try:
        log(f"Inserting entries to collection {mongo_collection.name}")
        mongo_collection.insert_many(entries)
        log(f"Entries inserted to collection {mongo_collection.name} successfully!")
        return True
    except:
        log_error(f"Entries insertion to collection {mongo_collection.name} failed!")
        return False


def collection_find_all(mongo_collection, query_object):
    try:
        log(f"Getting entries from collection {mongo_collection.name}")
        catalogue_objects = mongo_collection.find(query_object)
        catalogues = [dict(c) for c in catalogue_objects]
        for c in catalogues:
            c.pop('_id')
        log(f"Got entries from collection {mongo_collection.name} successfully")
        return catalogues
    except:
        log_error(f"Getting Entries for collection {mongo_collection.name} failed!")
        return None


def collection_find_one(mongo_collection, query_object):
    catalog = mongo_collection.find_one(query_object)
    catalog.pop('_id')
    return catalog

