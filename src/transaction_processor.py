import re
from typing import List, Dict


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """Функция, которая принимает список словарей с данными о банковских операциях и строку поиска и
    возвращает список словарей, у которых в описании есть данная строка."""

    # Проверка входных данных
    if not data:
        return []

    # Если строка поиска пустая, возвращаем все данные
    if not search:
        return data.copy()

    try:
        # Создаем регулярное выражение для поиска
        # Добавляем флаг re.IGNORECASE для поиска нечувствительному к регистру
        pattern = re.compile(search, re.IGNORECASE)
    except re.error as e:
        # В случае ошибки в регулярном выражении возвращаем пустой список
        # Можно также вывести сообщение об ошибке для отладки
        print(f"Ошибка в регулярном выражении: {e}")
        return []

    # Создаем пустой список для результатов
    result = []

    # Проходим по всем транзакциям в списке
    for transaction in data:
        # Проверяем, есть ли ключ 'description' в текущем словаре
        if "description" in transaction:
            description = transaction["description"]

            # Проверяем, что описание является строкой и не пустое
            if isinstance(description, str) and description.strip():
                # Ищем совпадение с помощью регулярного выражения
                # search() ищет первое совпадение в строке
                if pattern.search(description):
                    # Если найдено совпадение, добавляем транзакцию в результат
                    result.append(transaction)

    # Возвращаем отфильтрованный список
    return result


# Пример использования функции
if __name__ == "__main__":
    # Тестовые данные
    test_data = [
        {
            "id": "650703",
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210,
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
            "description": "Перевод организации",
        },
        {
            "id": "3598919",
            "state": "EXECUTED",
            "date": "2020-12-06T23:00:58Z",
            "amount": 29740,
            "currency_name": "Peso",
            "currency_code": "COP",
            "from": "Discover 3172601889670065",
            "to": "Discover 0720428384694643",
            "description": "Перевод с карты на карту",
        },
        {
            "id": "5380041",
            "state": "CANCELED",
            "date": "2021-02-01T11:54:58Z",
            "amount": 23789,
            "currency_name": "Peso",
            "currency_code": "UYU",
            "from": "",
            "to": "Счет 23294994494356835683",
            "description": "Открытие вклада",
        },
    ]

    # Тест 1: Поиск по обычной строке
    print("Тест 1: Поиск по слову 'перевод'")
    result1 = process_bank_search(test_data, "перевод")
    print(f"Найдено: {len(result1)} транзакций")
    for item in result1:
        print(f"  - {item['description']}")

    # Тест 2: Поиск с использованием регулярного выражения
    print("Тест 2: Поиск по шаблону '.*карты.*'")
    result2 = process_bank_search(test_data, ".*карты.*")
    print(f"Найдено: {len(result2)} транзакций")
    for item in result2:
        print(f"  - {item['description']}")

    # Тест 3: Поиск по точному совпадению
    print("Тест 3: Поиск по точной фразе 'Открытие вклада'")
    result3 = process_bank_search(test_data, "Открытие вклада")
    print(f"Найдено: {len(result3)} транзакций")
    for item in result3:
        print(f"  - {item['description']}")

    # Тест 4: Пустой запрос
    print("Тест 4: Пустой поисковый запрос")
    result4 = process_bank_search(test_data, "")
    print(f"Найдено: {len(result4)} транзакций (должны быть все)")

    # Тест 5: Поиск по несуществующей строке
    print("Тест 5: Поиск несуществующей строки")
    result5 = process_bank_search(test_data, "несуществующий_текст")
    print(f"Найдено: {len(result5)} транзакций")
