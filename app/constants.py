""" static texts, logic blocks in form of dicts (like MONGO_ARGS) """

# Python improts
from datetime import timedelta
from dateutil.relativedelta import relativedelta

# import custom classes, foos
from services import (
    create_day_delta_period,
    create_hour_delta_period,
    create_month_delta_period
)

MONGO_ARGS = {
    "hour": {
        "mango_args": {
            "year": {"$year": "$dt"},
            "month": {"$month": "$dt"},
            "day": {"$dayOfMonth": "$dt"},
            "hour": {"$hour": "$dt"}
        },
        "time_interval": create_hour_delta_period,
        "timedelta": timedelta(hours=1)
    },
    "day": {
        "mango_args": {
            "year": {"$year": "$dt"},
            "month": {"$month": "$dt"},
            "day": {"$dayOfMonth": "$dt"}
        },
        "time_interval": create_day_delta_period,
        "timedelta": timedelta(days=1)
    },
    "month": {
        "mango_args": {
        "year": {"$year": "$dt"},
        "month": {"$month": "$dt"}
        },
        "time_interval": create_month_delta_period,
        "timedelta": relativedelta(months=1)
    }
}

NOT_VALID_REQUEST = (
    "Невалидный запос. Пример запроса: \n"
    '{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}'
)