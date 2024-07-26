import datetime
import json
import pandas as pd
import math
import requests
import os
from dotenv import load_dotenv

load_dotenv(".env")


def get_data_filter_by_date(file_name: str, end_date: datetime.datetime) -> pd.DataFrame:
    """
    Считывание данных и фильтрация по дате
    """
    start_date = end_date.replace(day=1, hour=0, minute=0, second=0)
    operations = pd.read_excel(os.path.join("data/", file_name))
    df_date = pd.to_datetime(operations["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    operations = operations[(start_date <= df_date) & (df_date <= end_date)]
    return operations
