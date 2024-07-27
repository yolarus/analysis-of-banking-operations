import pandas as pd
import datetime
import json
from functools import wraps

from typing import Optional, Callable


def out_to_json_file(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: list, **kwargs: list) -> str:
        result = func(*args, **kwargs)
        wrapper_result = result.to_dict("records")
        wrapper_result = json.dumps(wrapper_result, indent=4, ensure_ascii=False)
        with open("reports/spending_by_category.json", "w") as file:
            file.write(wrapper_result)
        return result
    return wrapper


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

    print(start_date)
    print(end_date)

    df_date = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    transactions = transactions[(start_date <= df_date) & (df_date <= end_date)]
    transactions = transactions[transactions["Категория"] == category]
    expenses = transactions[transactions["Сумма операции"] < 0]
    return expenses
