from typing import Any, Dict, List


def filter_by_state(operations: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Функция, которая фильтрует список словарей по значению ключа 'state' и возвращает новый
    список словарей, у которых ключ 'state' соответствует указанному значению"""

    # Создаем пустой новый список для отфильтрованных операций
    filtered_operations = []

    # Проходим по каждой операции в исходном списке
    for operation in operations:
        # Сравниваем значение статуса операции с заданным значением 'state'
        if operation.get("state") == state:
            # Если статус операции совпадает, добавляем операцию в новый список
            filtered_operations.append(operation)

    # Возвращаем отфильтрованный список
    return filtered_operations


# Тестирование функции
if __name__ == "__main__":
    test_examples = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    # Выход функции со статусом по умолчанию 'EXECUTED'
    executed_operations = filter_by_state(test_examples)
    print(executed_operations)

    # Выход функции, если вторым аргументом передано 'CANCELED'
    canceled_operations = filter_by_state(test_examples, "CANCELED")
    print(canceled_operations)


def sort_by_date(operations: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """Функция, которая принимает список словарей с операциями и возвращает новый список,
    отсортированный по ключу 'date'. Сортировка выполняется по умолчанию в порядке убывания."""

    # Сортируем новый список по ключу 'date'
    sorted_list = sorted(operations, key=lambda x: x["date"], reverse=reverse)

    # Возвращаем новый список словарей, отсортированный по дате
    return sorted_list


# Тестирование функции
if __name__ == "__main__":
    test_examples = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    # Выход функции (сортировка по убыванию, т. е. сначала самые последние операции)
    sort_descending = sort_by_date(test_examples)
    print("Сортировка по убыванию: ")
    for operation in sort_descending:
        print(f"ID: {operation['id']}, State: {operation['state']}, Date: {operation['date']}")

    # Выход функции (сортировка по возрастанию, т. е. сначала самые первые операции)
    sort_ascending = sort_by_date(test_examples, reverse=False)
    print("\nСортировка по возрастанию: ")
    for operation in sort_ascending:
        print(f"ID: {operation['id']}, State: {operation['state']}, Date: {operation['date']}")


