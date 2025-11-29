import pandas as pd
import os
from typing import List, Dict, Any, cast


def read_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из Excel-файла и возвращает список словарей."""

    # Проверяем существование файла
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден")

    # Чтение Excel-файла
    df = pd.read_excel(file_path, engine="openpyxl")

    # Замена NaN на None для корректной обработки пустых значений
    df = df.replace({pd.NA: None})

    # Преобразование DataFrame в список словарей
    transactions = cast(List[Dict[str, Any]], df.to_dict("records"))

    return transactions


# Пример использования:
if __name__ == "__main__":
    absolute_path = r"C:\Users\mburs\PycharmProjects\Project1-Skypro\data\transactions_excel.xlsx"

    transactions = read_transactions_from_excel(absolute_path)
    for transaction in transactions:
        print(transaction)
