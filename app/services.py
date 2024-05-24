""" Module for classes, foos, that processing data """

# time imports
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from datetime import datetime # for typing

# import custom foos, classes
from logger import logger


def create_day_delta_period(
        dt_from: datetime,
        dt_upto: datetime
) -> list[str] | None:
    """
    Create list of datetime all days beetween
    dt_from and dt_upto.
    Parameters:
        date_from: date_from param's value that sent user
        date_to: date_to param's value that sent user
    Returns:
        list[str] | None: return list of datetime days objects
            that contains between dt_from and dt_upto or None object
            if there is exception.
    """
    try:
        periods = [dt_from + timedelta(days=i) for i in range((dt_upto - dt_from).days + 1)]

        return [period.strftime("%Y-%m-%dT%H:%M:%S") for period in periods]

    except Exception as ex:
        logger.error(
            "[services.create_day_delta_period] "
            f"Exception: {ex}. "
            f"dt_from: {dt_from}. "
            f"dt_upto: {dt_upto}. "
        )

        return None


def create_month_delta_period(
        dt_from: datetime,
        dt_upto: datetime
) -> list[str] | None:
    """
    Create list of datetime all monthes beetween
    dt_from and dt_upto.
    Parameters:
        date_from: date_from param's value that sent user
        date_to: date_to param's value that sent user
    Returns:
        list[str] | None: return list of datetime month objects
            that contains between dt_from and dt_upto or None object
            if there is exception.
    """
    try:

        months = []
        current_month = dt_from.replace(day=1)

        while current_month <= dt_upto.replace(day=1):
            months.append(current_month)
            current_month += relativedelta(months=1)

        return [month.strftime("%Y-%m-%dT%H:%M:%S") for month in months]

    except Exception as ex:
        logger.error(
            "[services.create_month_delta_period] "
            f"Exception: {ex}. "
            f"dt_from: {dt_from}. "
            f"dt_upto: {dt_upto}. "
        )

        return None


def create_hour_delta_period(
        dt_from: datetime,
        dt_upto: datetime
) -> list[str] | None:
    """
    Create list of datetime all hours beetween
    dt_from and dt_upto.
    Parameters:
        date_from: date_from param's value that sent user
        date_to: date_to param's value that sent user
    Returns:
        list[str] | None: return list of datetime hour objects
            that contains between dt_from and dt_upto or None object
            if there is exception.
    """
    try:
        hours = [dt_from + timedelta(hours=i) for i in range(int((dt_upto - dt_from).total_seconds() / 3600) + 1)]
        return [hour.strftime("%Y-%m-%dT%H:%M:%S") for hour in hours]
    
    except Exception as ex:
        logger.error(
            "[services.create_hour_delta_period] "
            f"Exception: {ex}. "
            f"dt_from: {dt_from}. "
            f"dt_upto: {dt_upto}. "
        )

        return None