# from pymongo import MongoClient
#
# from main.config import get_config_by_name
# from main.logger.custom_logging import log
#
#
# def init_database():
#     global mongo_client, mongo_db
#     database_host = get_config_by_name('MONGO_DATABASE_HOST')
#     database_port = get_config_by_name('MONGO_DATABASE_PORT')
#     database_name = get_config_by_name('MONGO_DATABASE_NAME')
#     mongo_client = MongoClient(database_host, database_port)
#     mongo_db = mongo_client[database_name]
#     log(f"Connection to mongodb://{database_host}:{database_port} is successful!")
#
#
# def get_mongo_collection(collection_name):
#     return mongo_db[collection_name]


""" Module that monkey-patches the json module when it's imported so
JSONEncoder.default() automatically checks to see if the object being encoded
is an instance of an Enum type and, if so, returns its name.
"""
from enum import Enum
from json import JSONEncoder

_saved_default = JSONEncoder().default  # Save default method.


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

