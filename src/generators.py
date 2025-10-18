from typing import Any, Dict, Generator, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """Фильтрует транзакции по заданной валюте. Функция принимает список транзакций и возвращает
    итератор, который поочередно выдает транзакции, где валюта операции соответствует заданной."""

    for transaction in transactions:
        try:
            # Получаем код валюты из вложенной структуры transaction
            transaction_currency = transaction["operationAmount"]["currency"]["code"]
            if transaction_currency == currency:
                yield transaction
        except (KeyError, TypeError):
            # Пропускаем транзакции с некорректной структурой
            continue


# Пример использования
if __name__ == "__main__":
    transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
    ]

    # Использование функции
    usd_transactions = filter_by_currency(transactions, "USD")
    for _ in range(2):
        print(next(usd_transactions))


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """Генератор, который возвращает описание каждой транзакции по очереди. Функция принимает
    список транзакций и возвращает итератор, который поочередно выдает строки с описанием операций."""

    for transaction in transactions:
        try:
            # Извлекаем описание из транзакции
            description = transaction["description"]
            yield description
        except (KeyError, TypeError):
            # Если описание отсутствует или структура некорректна, пропускаем
            continue


# Пример использования
if __name__ == "__main__":
    # Тестовые данные
    transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]

    # Использование генератора
    descriptions = transaction_descriptions(transactions)
    for _ in range(5):
        print(next(descriptions))


def card_number_generator(start: int, stop: int) -> Generator[str]:
    """Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.Генерирует номера карт
    в заданном диапазоне, начиная с начального значения и заканчивая конечным значением
    включительно. Каждый номер карты форматируется как четыре группы по четыре цифры,
    разделенные пробелами."""

    for number in range(start, stop + 1):
        # Преобразуем число в строку и дополняем ведущими нулями до 16 цифр
        card_str = f"{number:016d}"

        # Форматируем в виде XXXX XXXX XXXX XXXX
        formatted_card = " ".join([card_str[0:4], card_str[4:8], card_str[8:12], card_str[12:16]])

        yield formatted_card


# Пример использования
if __name__ == "__main__":
    for card_number in card_number_generator(1, 5):
        print(card_number)
