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


def get_cards_info(operations: pd.DataFrame) -> list[dict]:
    """
    Получение информации по картам (последние 4 цифры, общая сумма расходов, кешбэк)
    """
    expenses = operations[operations["Сумма операции"] < 0]
    expenses_group_cards = expenses.groupby("Номер карты").agg({"Сумма операции": "sum", "Кэшбэк": "sum"})

    fieldnames = ["last_digits", "total_spent", "cashback"]
    card_numbers = expenses_group_cards.index.tolist()
    cards_list = []
    for row in expenses_group_cards.iterrows():
        card_dict = {"last_digits": card_num[-4:] for card_num in card_numbers}
        for i, element in enumerate(row[1], 1):
            card_dict[fieldnames[i]] = element
        cards_list.append(card_dict)

    for card in cards_list:
        card["total_spent"] *= -1
        card["total_spent"] = round(card["total_spent"], 2)
    return cards_list