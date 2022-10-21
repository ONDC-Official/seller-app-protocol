from pymongo import MongoClient

from main.config import get_config_by_name
from main.logger.custom_logging import log


def init_database():
    global mongo_client, mongo_db
    database_host = get_config_by_name('MONGO_DATABASE_HOST')
    database_port = get_config_by_name('MONGO_DATABASE_PORT')
    database_name = get_config_by_name('MONGO_DATABASE_NAME')
    mongo_client = MongoClient(database_host, database_port)
    mongo_db = mongo_client[database_name]
    log(f"Connection to mongodb://{database_host}:{database_port} is successful!")


def get_mongo_collection(collection_name):
    return mongo_db[collection_name]
