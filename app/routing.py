""" get Telegram message, processin that one and provide answer to Telegram User """

# python imports
import json

# Pydantic, FastAPI imports
from schemas import InputData
from pydantic import ValidationError

# Telegram imports
from aiogram import types
from aiogram import Router

# import constancts
from constants import NOT_VALID_REQUEST

# import custom fooc, classes
from db_actions import find_mongo_data
from logger import logger

# declare router for processing Telegram messages 
base_router = Router()


@base_router.message()
async def get_user_message(message: types.Message) -> types.Message | None:
    """
    Telegram route for user's message with JSON that must
    contains dt_from, dt_upto, group_type params.
    The route processes the received data and if data is valid
    send answer.
    NOTE: it's not good docstring for route (:
    """
    try:
        json_input_data = json.loads(message.text)
        # convert to lowercase all keys and values if nested dicts
        json_input_data = {k.lower(): v.lower() for k, v in json_input_data.items()}

        input_data = {}
        input_data["dt_from"] = json_input_data.get('dt_from')
        input_data["dt_upto"] = json_input_data.get("dt_upto")
        input_data["group_type"] = json_input_data.get("group_type")

        if not any(
            param in [None, " ", ""] for param in input_data.values()
        ):

            try:
                input_data: dict = dict(InputData(**input_data))
                mongo_data: dict = await find_mongo_data(input_data)
            
                if mongo_data:

                    try:
                        await message.answer(mongo_data)
                    
                    except Exception as ex:

                        if "text is too long" in str(ex):
                            # https://docs.aiogram.dev/en/latest/api/upload_file.html
                            mongo_data: bytes = mongo_data.encode('utf-8')
                            buffered_input_file: types.BufferedInputFile[bytes] = types.BufferedInputFile(mongo_data, filename="data.json")
                            await message.answer_document(buffered_input_file)

                        else:
                            logger.error(
                                "[routing.get_user_message] "
                                "Exception while sending message. "
                                f"Exception text: {ex}. "
                                f"Message object: {message}. "
                            )
                            
            except ValidationError as valid_error:
                await message.answer(NOT_VALID_REQUEST)
                logger.error(
                    "[routing.get_user_message] "
                    f"ValidationError text: {valid_error}. "
                    f"Message object: {message}. "
                )

        else:
            await message.answer(NOT_VALID_REQUEST)

    except Exception as ex:
        await message.answer(NOT_VALID_REQUEST)
        logger.error(
            "[routing.get_user_message] "
            f"Exception text: {ex}. "
            f"Message object: {message}. "
        )
