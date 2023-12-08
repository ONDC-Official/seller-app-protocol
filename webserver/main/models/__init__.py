""" Module that monkey-patches the json module when it's imported so
JSONEncoder.default() automatically checks to see if the object being encoded
is an instance of an Enum type and, if so, returns its name.
"""
from enum import Enum
from json import JSONEncoder

from pymongo import MongoClient

from main.config import get_config_by_name
from main.logger.custom_logging import log

_saved_default = JSONEncoder().default  # Save default method.
mongo_client = None
mongo_db = None


def json_decoder_default(self, obj):
    if isinstance(obj, bool) or isinstance(obj, int) or isinstance(obj, float) or isinstance(obj, list) or isinstance(
            obj, dict):
        return _saved_default  # Default
    elif isinstance(obj, Enum):
        return obj.value  # Could also be obj.value
    else:
        return str(obj)  # Stringify remaining types


JSONEncoder.default = json_decoder_default  # Set new default method.


class BaseModel:
    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            column_value = getattr(self, column.name)
            d[column.name] = column_value

        return d


def init_database():
    global mongo_client, mongo_db
    if mongo_client is not None and mongo_db is not None:
        return
    database_host = get_config_by_name('MONGO_DATABASE_HOST')
    database_port = get_config_by_name('MONGO_DATABASE_PORT')
    database_name = get_config_by_name('MONGO_DATABASE_NAME')
    mongo_client = MongoClient(database_host, database_port, maxPoolSize=10)
    mongo_db = mongo_client[database_name]
    log(f"Connection to mongodb://{database_host}:{database_port} is successful!")
    create_all_ttl_indexes()
    log(f"Created indexes if not already present!")


def create_all_ttl_indexes():
    collection_names = ['search', 'select', 'init', 'confirm', 'cancel', 'status', 'support', 'track', 'update',
                        'rating', 'issue', 'issue_status', 'on_search', 'on_select', 'on_init', 'on_confirm',
                        'on_cancel', 'on_status', 'on_support', 'on_track', 'on_update', 'on_rating', 'on_issue',
                        'on_issue_status']
    [create_ttl_index(c) for c in collection_names]


def create_ttl_index(collection_name):
    # check if index already exists
    if "created_at_ttl" in get_mongo_collection(collection_name).index_information():
        return
    ttl_in_seconds = get_config_by_name('TTL_IN_SECONDS')
    get_mongo_collection(collection_name).create_index("created_at", name="created_at_ttl",
                                                       expireAfterSeconds=ttl_in_seconds)


def get_mongo_collection(collection_name):
    # check if database is initialized
    global mongo_client, mongo_db
    if mongo_client is None or mongo_db is None:
        init_database()
    return mongo_db[collection_name]
