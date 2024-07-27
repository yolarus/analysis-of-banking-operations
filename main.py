import pandas as pd

from src.views import main
from src.services import increase_cashback
from src.reports import spending_by_category

if __name__ == "__main__":
    # print(main("2021-12-31 16:44:00"))

    data = pd.read_excel("data/operations.xlsx")
    print(increase_cashback(data, 2021, 11))

    print(spending_by_category(data, "Супермаркеты", "2022.03.01"))
