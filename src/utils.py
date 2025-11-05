import json
import os
from typing import List, Dict, Any


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает данные о финансовых транзакциях из JSON-файла."""

    # Определяем путь к файлу относительно корня проекта
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "operations.json")

    print(f"Ищем файл по пути: {file_path}")  # Для отладки

    # Проверяем существование файла
    if os.path.exists(file_path):
        print(f"Файл найден по пути: {os.path.abspath(file_path)}")
    else:
        print(f"Файл НЕ найден по пути: {os.path.abspath(file_path)}")
        return []

    # Проверяем, что это файл, а не директория
    if not os.path.isfile(file_path):
        print(f"{file_path} не является файлом")
        return []

    # Проверяем, что файл не пустой
    if os.path.getsize(file_path) == 0:
        print(f"Файл {file_path} пустой")
        return []

    try:
        # Открываем и читаем файл
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Проверяем, что данные являются списком
        if isinstance(data, list):
            print(f"Успешно загружено {len(data)} транзакций")
            return data
        else:
            print(f"Данные не являются списком, тип: {type(data)}")
            return []

    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON-данных в файле {file_path}")
        return []
    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден")
        return []


# Пример использования
if __name__ == "__main__":
    # Загрузка транзакций из файла
    transactions = load_transactions("data/operations.json")

    # Вывод результата
    print(f"Загружено {len(transactions)} транзакций")
    for transaction in transactions:
        print(transaction)
