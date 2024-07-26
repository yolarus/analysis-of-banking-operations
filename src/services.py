import datetime
import json

import pandas as pd


def increase_cashback(data: pd.DataFrame, year: int, month: int) -> str:
    """
    Функция анализирует наиболее выгодные категории кэшбэка в переданном датафрэйме
    """
    start_date = datetime.datetime(year=year, month=month, day=1)
    if month == 12:
        end_date = start_date.replace(year=year + 1, month=1) - datetime.timedelta(seconds=1)
    else:
        end_date = start_date.replace(month=month + 1) - datetime.timedelta(seconds=1)

    df_date = pd.to_datetime(data["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    data = data[(start_date <= df_date) & (df_date <= end_date)]
    cashback = data[data["Кэшбэк"] > 0]

    data_group_category = cashback.groupby("Категория").agg({"Кэшбэк": "sum"})
    data_group_category.sort_values(by="Кэшбэк", ascending=False, inplace=True)

    result_dict = data_group_category.to_dict(orient="dict")
    result = json.dumps(result_dict["Кэшбэк"], ensure_ascii=False)
    return result
