import os.path

import pandas as pd
import datetime
import json
from functools import wraps

from typing import Optional, Callable


def out_to_json_file(func: Callable) -> Callable:
    """
    Запись датафрейма в файл records.json в JSON формате
    """
    @wraps(func)
    def wrapper(*args: list, **kwargs: list) -> pd.DataFrame:
        result = func(*args, **kwargs)
        wrapper_result = result.to_dict("records")
        wrapper_result = json.dumps(wrapper_result, indent=4, ensure_ascii=False)
        with open("reports/report.json", "w") as file:
            file.write(wrapper_result)
        return result
    return wrapper


def out_to_user_file(file_name: str) -> Callable:
    """
    Запись датафрейма в пользовательский файл в CSV формате
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: list, **kwargs: list) -> pd.DataFrame:
            result = func(*args, **kwargs)
            with open(os.path.join("reports/", file_name), "w") as file:
                file.write(result.to_csv())
            return result

        return wrapper
    return decorator


@out_to_user_file(file_name="spending_by_category.txt")
@out_to_json_file
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """ Опицонально принимает дату в формате ГГГГ.ММ.ДД"""

    if date:
        end_date = datetime.datetime.strptime(date, "%Y.%m.%d")
    else:
        end_date = datetime.datetime.now()

    if end_date.month <= 3:
        start_date = end_date.replace(year=end_date.year - 1, month=end_date.month + 12 - 3)
    else:
        start_date = end_date.replace(month=end_date.month - 3)

    df_date = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    transactions = transactions[(start_date <= df_date) & (df_date <= end_date)]
    transactions = transactions[transactions["Категория"] == category]
    expenses = transactions[transactions["Сумма операции"] < 0]
    return expenses
