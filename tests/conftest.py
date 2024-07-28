import pytest

import pandas as pd


@pytest.fixture
def transactions_df() -> pd.DataFrame:
    data = pd.DataFrame({"Категория": ["Супермаркеты",
                                       "Одежда",
                                       "Рестораны",
                                       "Супермаркеты",
                                       "Супермаркеты",
                                       "Супермаркеты"],
                         "Дата операции": ["31.12.2021 16:44:00",
                                           "30.12.2021 16:44:00",
                                           "30.12.2021 16:44:00",
                                           "30.12.2021 16:44:00",
                                           "29.11.2021 16:44:00",
                                           "27.07.2024 16:44:00"],
                         "Сумма операции": [-1,
                                            -2,
                                            -3,
                                            -4,
                                            -5,
                                            -6],
                         "Кэшбэк": [10, 20, 0, 30, 40, 50]},
                        index=[0, 1, 2, 3, 4, 5])

    return data


@pytest.fixture
def res_spending_by_category() -> pd.DataFrame:
    data = pd.DataFrame({"Категория": ["Супермаркеты", "Супермаркеты"],
                         "Дата операции": ["31.12.2021 16:44:00", "30.12.2021 16:44:00"],
                         "Сумма операции": [-1, -4],
                         "Кэшбэк": [10, 30]},
                        index=[0, 3])
    return data


@pytest.fixture
def res_spending_by_category_without_date() -> pd.DataFrame:
    data = pd.DataFrame({"Категория": ["Супермаркеты"],
                         "Дата операции": ["27.07.2024 16:44:00"],
                         "Сумма операции": [-6],
                         "Кэшбэк": [50]},
                        index=[5])
    return data


@pytest.fixture
def res_spending_by_category_empty() -> pd.DataFrame:
    data = pd.DataFrame({"Категория": [],
                         "Дата операции": [],
                         "Сумма операции": [],
                         "Кэшбэк": []},
                        index=[])
    return data


@pytest.fixture()
def cashback_12() -> str:
    data = """{"Супермаркеты": 40, "Одежда": 20}"""
    return data
