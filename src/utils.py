import json
import os
from typing import List, Dict, Any


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает данные о финансовых транзакциях из JSON-файла."""

    # Проверяем существование файла
    if not os.path.exists(file_path):
        return []

    # Проверяем, что это файл, а не директория
    if not os.path.isfile(file_path):
        return []

    # Проверяем, что файл не пустой
    if os.path.getsize(file_path) == 0:
        return []

    try:
        # Открываем и читаем файл
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Проверяем, что данные являются списком
        if isinstance(data, list):
            return data
        else:
            return []

    except json.JSONDecodeError:
        return []
    except FileNotFoundError:
        return []
    except Exception:
        return []


# Пример использования
if __name__ == "__main__":
    # Формируем путь к файлу
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(current_dir, "data", "operations.json")

    # Загрузка транзакций из файла
    transactions = load_transactions(file_path)

    # Вывод результата
    print(f"Загружено {len(transactions)} транзакций")
    for transaction in transactions:
        print(transaction)
