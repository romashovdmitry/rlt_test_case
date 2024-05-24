""" Module for Mongo actions: get, delete, update, create DB data """

# Python imports
from os import getenv

# Mongo imports
from motor.motor_asyncio import AsyncIOMotorClient

# import constants
from constants import MONGO_ARGS

# import custom foos, clases
from logger import logger


# Mongo connection setup
username = getenv("MONGO_INITDB_ROOT_USERNAME")
password = getenv("MONGO_INITDB_ROOT_PASSWORD")
url = f"mongodb://{username}:{password}@rlt_mongo:27017/"
client = AsyncIOMotorClient(url)
db = client[getenv("MONGO_DB_NAME")]
collection = db[getenv("MONGO_COLLECTION_NAME")]


async def find_mongo_data(input_data: dict) -> dict[str, list] | None:
    """
    Get data from Mongo DB and return formatted dict
    for answer to Telegram user.

    Parameters (inside input_data):
        input_data["dt_from"]: isodata with start of period for
            query
        input_data["dt_upto"]: isodata with start of period for
            query
        input_data["group_type"]: string 'month', 'day' or 'hour'
            for 'group by' in query
        input_data["formatted_periods"]: periods between dt_from,
            dt_upto that grouped by hour, day ot month
    Returns:
        dict[str, list] | None: dict with final formatted
            data that would be returned to Telegram user
            or None if unsuccesfull query result
    """

    pipeline = [
        {
            "$match": {
                "dt": {
                    "$gte": input_data["dt_from"],
                    "$lte": input_data["dt_upto"]
                }
            }
        },
        {
            "$addFields": {
                "formatted_date": {
                    "$dateToString": {
                        "format": "%Y-%m-%dT%H:%M:%S",
                        "date": "$dt"
                    }
                }
            }
        },
        {
            "$group": {
                "_id": {
                    "$dateFromParts": MONGO_ARGS[input_data["group_type"]]["mango_args"]
                },
                "total_value": {"$sum": "$value"}
            }
        },
        {
            "$sort": {
                "_id": 1
            }
        }
    ]

    return_ = {
        "dataset": [0 for x in range(len(input_data["formatted_periods"]))],
        "labels": input_data["formatted_periods"]
    }

    # NOTE: 100% it's better to do by pipeline,
    # but i didn't find way to do that
    # by pipeline
    try:
        # https://pymongo.readthedocs.io/en/stable/examples/aggregation.html
        async for document in collection.aggregate(pipeline):
            label = document["_id"].strftime("%Y-%m-%dT%H:%M:%S")
            return_["dataset"][return_["labels"].index(label)] = document["total_value"]

    except Exception as ex:
        logger.debug(
            "[db_actions.find_mongo_data] Exceptions while "
            "processing data from database. "
            f'Exception text: {ex}'
        )

    return str(return_)
