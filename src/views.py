import datetime
import json
import pandas as pd
import math
import requests
import os
from dotenv import load_dotenv

load_dotenv(".env")


def main(user_date: str) -> str:
    """
    Функция принимает строку с датой  и временем в формате YYYY-MM-DD HH:MM:SS и возвращает JSON-ответ
    """
    end_date = datetime.datetime.strptime(user_date, "%Y-%m-%d %H:%M:%S")

    # Определяем время суток
    if 0 <= end_date.hour < 6:
        greeting = "Доброй ночи"
    elif 6 <= end_date.hour < 12:
        greeting = "Доброе утро"
    elif 12 <= end_date.hour < 18:
        greeting = "Добрый день"
    else:
        greeting = "Добрый вечер"

    operations = get_data_filter_by_date("operations.xlsx", end_date)

    cards_list = get_cards_info(operations)

    top_operations_list = get_top_transactions(operations)

    currencies_list = get_exchange_rates(["USD", "EUR"])

    stock_prices = get_stock_rates(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])

    result_dict = {"greeting": greeting,
                   "cards": cards_list,
                   "top_transactions": top_operations_list,
                   "currency_rates": currencies_list,
                   "stock_prices": stock_prices}

    return json.dumps(result_dict, ensure_ascii=False)


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


def get_top_transactions(operations: pd.DataFrame) -> list[dict]:
    """
    Топ 5 по сумме платежа
    """
    operations_with_fabs = operations
    operations_with_fabs["Сумма операции по модулю"] = operations["Сумма операции"].apply(math.fabs)
    sorted_operations_by_amount = operations_with_fabs.sort_values(by="Сумма операции по модулю", ascending=False)
    fieldnames = ["date", "amount", "category", "description"]
    top_operations_list = []
    counter = 0
    for row in sorted_operations_by_amount.loc[:, ["Дата операции",
                                                   "Сумма операции",
                                                   "Категория",
                                                   "Описание"]].iterrows():
        operation_dict = {}
        for i, element in enumerate(row[1]):
            operation_dict[fieldnames[i]] = element
        top_operations_list.append(operation_dict)
        counter += 1
        if counter == 5:
            return top_operations_list


def get_exchange_rates(currencies: list[str]) -> list[dict]:
    """
    Получение курсов валют по списку кодов
    """
    api_key_exchange_rates_data = os.getenv("API_KEY_EXCHANGE_RATES_DATA")
    headers = {"apikey": api_key_exchange_rates_data}
    currencies_list = []
    for currency in currencies:
        currency_dict = {}
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={'RUB'}&from={currency}&amount={1}"
        response = requests.get(url, headers=headers)
        currency_dict["currency"] = currency
        currency_dict["rate"] = round(response.json()["result"], 2)
        currencies_list.append(currency_dict)
    return currencies_list


def get_stock_rates(stock_list: list[str]) -> list[dict]:
    """
    Получение цен акций по списку кодов
    """
    api_key_financial_modeling_prep = os.getenv("API_KEY_FINANCIAL_MODELING_PREP")
    url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={api_key_financial_modeling_prep}"
    response = requests.get(url)
    stock_prices = []
    for share in response.json():
        stock_dict = {}
        if share["symbol"] in stock_list:
            stock_dict["stock"] = share["symbol"]
            stock_dict["price"] = round(share["price"], 2)
            stock_prices.append(stock_dict)
    return stock_prices
