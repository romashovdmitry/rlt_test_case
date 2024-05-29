# Python imports
from enum import Enum
from datetime import datetime

# Pydantic imports
from pydantic import BaseModel, model_validator
from pydantic import Extra

# additional libs for processing datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta

# import constants
from constants import MONGO_ARGS

# import custom foos, classes
from logger import logger


def timedelta_diff_helper(
        date_from: datetime,
        date_to: datetime,
        group_type: str
) -> bool:
    """
    Help to define difference between date_from param
        and date_to: if difference less than group_type-period
        than return False and call ValueError by next step.
    Parameters:
        date_from: date_from param's value that sent user
        date_to: date_to param's value that sent user
        group_type: group_type-period param's value that sent user
    Returns:
        bool: True if group_type-period greater than differnce
            between date_to and date_from. Otherwise, return False
    """
    if group_type == "month":
        delta_date_from = date_to - relativedelta(months=1)

        if delta_date_from < date_from:

            return False
    
        return True

    return (date_from - date_to) < MONGO_ARGS[group_type]["timedelta"]


# https://stackoverflow.com/a/73827031
class GroupType(str, Enum):
    hour = "hour"
    day = "day"
    month = "month"


class InputData(BaseModel):
    dt_from: datetime = None
    dt_upto: datetime = None
    group_type: GroupType

    # https://stackoverflow.com/a/67202142
    class Config:
        extra = Extra.allow

    @model_validator(mode="before")
    def validate_all_fields(cls, values: dict) -> dict | ValueError:
        """
        1. Validate all fields in type of data.
        2. Validate period that user sent.
        3. Add additional field formatted_periods
            for more info about this field look
            constants.py, services.py
        Parameters:
            cls: class InputData
            values: json-dict that sent to user
        Returns:
            dict | ValueError: validated dict with additional field
                or ValueError if data is not validated by method
        """
        # https://stackoverflow.com/a/3908349/24040439
        dt_from = parser.parse(values["dt_from"])
        dt_upto = parser.parse(values["dt_upto"])
        group_type = values["group_type"]

        if dt_upto < dt_from:
            raise ValueError()

        if not timedelta_diff_helper(
            date_from=dt_from,
            date_to=dt_upto,
            group_type=group_type
        ):
            raise ValueError()

        # call foo from services.py, look constants.py MONGO_ARGS
        formatted_periods: list[str] | None = MONGO_ARGS[group_type]["time_interval"](
            dt_from=dt_from,
            dt_upto=dt_upto
        )

        if formatted_periods:

            return {
                "dt_from": dt_from,
                "dt_upto": dt_upto,
                "group_type": group_type,
                "formatted_periods": formatted_periods
            }

        else:
            ValueError()