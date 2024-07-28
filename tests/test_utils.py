from src.utils import (get_data_filter_by_date, get_cards_info, get_top_transactions,
                       get_exchange_rates, get_stock_rates, open_user_settings)
from unittest.mock import patch, mock_open
import pandas as pd
import datetime
from typing import Any
import requests

@patch("pandas.read_excel")
def test_get_data_filter_by_date(mock_df: Any, transactions_df: pd.DataFrame,
                                 res_get_data_filter_by_date: pd.DataFrame) -> None:
    date = datetime.datetime.strptime("31.12.2021 16:44:00", "%d.%m.%Y %H:%M:%S")
    mock_df.return_value = transactions_df
    assert get_data_filter_by_date("operations.xlsx", date).equals(res_get_data_filter_by_date)


def test_get_cards_info(transactions_df: pd.DataFrame) -> None:
    result = get_cards_info(transactions_df)
    assert result == [{"last_digits": "1111", "total_spent": 3, "cashback": 30},
                      {"last_digits": "2222", "total_spent": 7, "cashback": 30},
                      {"last_digits": "3333", "total_spent": 11, "cashback": 90}]


def test_get_top_transactions(transactions_df: pd.DataFrame, top_transactions_df: list[dict]) -> None:
    result = get_top_transactions(transactions_df)
    assert result == top_transactions_df


@patch("requests.get")
def test_get_exchange_rates(mock_get: Any):
    mock_get.return_value.json.return_value = {"result": 100}
    assert get_exchange_rates(["USER"]) == [{'currency': 'USER', 'rate': 100}]
    mock_get.assert_called_once()


@patch("requests.get")
def test_get_stock_rates(mock_get: Any):
    mock_get.return_value.json.return_value = [{"symbol": "USER", "price": 100}]
    assert get_stock_rates(["USER"]) == [{'stock': 'USER', 'price': 100}]
    mock_get.assert_called_once()


def test_open_user_settings():
    data = """{"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}"""
    with patch("builtins.open", mock_open(read_data=data)) as mock_file:
        assert open_user_settings() == {"user_currencies": ["USD", "EUR"],
                                        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}