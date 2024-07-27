import datetime
import json

from src.utils import (open_user_settings, get_data_filter_by_date, get_cards_info,
                   get_top_transactions, get_stock_rates, get_exchange_rates)


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
    user_settings = open_user_settings()
    currencies_list = get_exchange_rates(user_settings["user_currencies"])
    stock_prices = get_stock_rates(user_settings["user_stocks"])

    result_dict = {"greeting": greeting,
                   "cards": cards_list,
                   "top_transactions": top_operations_list,
                   "currency_rates": currencies_list,
                   "stock_prices": stock_prices}

    return json.dumps(result_dict, ensure_ascii=False)
