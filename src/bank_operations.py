from collections import Counter
from typing import List, Dict, Any


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """Функция, которая принимает список словарей с данными о банковских операциях и список категорий
    операций, а возвращает словарь, в котором ключи — это названия категорий, а значения — это
    количество операций в каждой категории. Категории операций хранятся в поле description."""

    # Проверка типов входных параметров
    if not isinstance(data, list):
        raise TypeError(f"Параметр 'data' должен быть списком, получен {type(data).__name__}")

    if not isinstance(categories, list):
        raise TypeError(f"Параметр 'categories' должен быть списком, получен {type(categories).__name__}")

    # Инициализируем счетчик для категорий
    category_counts = {category: 0 for category in categories}

    if not data or not categories:
        return category_counts

    # Создаем множество категорий в нижнем регистре для быстрого доступа
    # Используем dict для сохранения связи с оригинальными категориями
    categories_lower = {cat.lower(): cat for cat in categories}

    # Используем Counter для подсчета вхождений каждой категории
    counter: Counter[str] = Counter()

    # Проходим по всем транзакциям
    for transaction in data:
        if 'description' not in transaction:
            # Если нет поля description, пропускаем транзакцию
            continue

        description = transaction['description']

        # Проверяем, что описание является строкой и не пустое
        if not isinstance(description, str) or not description.strip():
            continue

        # Приводим описание к нижнему регистру для регистронезависимого поиска
        description_lower = description.lower()

        # Проверяем каждую категорию в нижнем регистре
        for cat_lower, cat_original in categories_lower.items():
            if cat_lower in description_lower:
                # Увеличиваем счетчик для данной категории
                counter[cat_original] += 1

    # Обновляем результат значениями из Counter
    category_counts.update(counter)

    return category_counts


# Пример использования функции
if __name__ == '__main__':
    # Создаем тестовые данные
    test_data = [
        {"id": "1", "description": "Перевод организации"},
        {"id": "2", "description": "Перевод с карты на карту"},
        {"id": "3", "description": "Открытие вклада"},
        {"id": "4", "description": "Перевод со счета на счет"},
        {"id": "5", "description": "Перевод организации"},
        {"id": "5", "description": "Открытие вклада"},
        {"id": "2", "description": "Перевод с карты на карту"},
    ]

    # Категории для поиска
    categories = ["перевод организации", "открытие вклада", "перевод с карты на карту", "перевод со счета на счет"]

    # Вызываем функцию
    result = process_bank_operations(test_data, categories)

    # Выводим результат
    print("Результат работы функции:")
    for category, count in result.items():
        print(f"{category}: {count}")
