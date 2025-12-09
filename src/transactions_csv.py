import pandas as pd
import os
from typing import List, Dict, Any, cast


def read_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из CSV-файла и возвращает список словарей с транзакциями."""

    # Проверяем существование файла
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден")

    # Чтение CSV-файла с разделителем ';'
    df = pd.read_csv(file_path, sep=";")

    # Замена NaN на None для корректной обработки пустых значений
    df = df.replace({pd.NA: None, float("nan"): None})

    # Преобразование DataFrame в список словарей
    transactions = cast(List[Dict[str, Any]], df.to_dict("records"))

    return transactions


# Пример использования:
if __name__ == "__main__":
    absolute_path = r"C:\Users\mburs\PycharmProjects\Project1-Skypro\data\transactions.csv"

    transactions = read_transactions_from_csv(absolute_path)
    for transaction in transactions:
        print(transaction)
