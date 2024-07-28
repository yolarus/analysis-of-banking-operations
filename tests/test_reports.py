# from unittest.mock import mock_open, patch
#
# import pandas as pd
#
# from src.reports import out_to_json_file, out_to_user_file, spending_by_category
#
#
# def test_spending_by_category(transactions_df: pd.DataFrame,
#                               res_spending_by_category: pd.DataFrame) -> None:
#     assert spending_by_category(transactions_df, "Супермаркеты", "2022.03.01").equals(res_spending_by_category)
#
#
# def test_spending_by_category_without_date(transactions_df: pd.DataFrame,
#                                            res_spending_by_category_without_date: pd.DataFrame) -> None:
#     result = spending_by_category(transactions_df, "Супермаркеты")
#     assert result. equals(res_spending_by_category_without_date)
#
#
# def test_spending_by_category_empty(transactions_df: pd.DataFrame) -> None:
#     result = spending_by_category(transactions_df, "Супермаркеты", "2025.03.01")
#     assert result.empty
