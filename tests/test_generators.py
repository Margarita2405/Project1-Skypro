from typing import Any, Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


def test_filter_usd_transactions(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест фильтрации транзакций в USD. Проверяет, что функция корректно находит все
    транзакции в указанной валюте."""

    result = list(filter_by_currency(sample_transactions, "USD"))

    assert len(result) == 3
    assert all(transaction["operationAmount"]["currency"]["code"] == "USD" for transaction in result)
    assert result[0]["id"] == 939719570
    assert result[1]["id"] == 142264268
    assert result[2]["id"] == 895315941


def test_filter_rub_transactions(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест фильтрации транзакций в RUB. Проверяет, что функция корректно находит все
    транзакции в рублях."""

    result = list(filter_by_currency(sample_transactions, "RUB"))

    assert len(result) == 2
    assert all(transaction["operationAmount"]["currency"]["code"] == "RUB" for transaction in result)
    assert result[0]["id"] == 873106923
    assert result[1]["id"] == 594226727


def test_filter_nonexistent_currency(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест фильтрации по несуществующей валюте. Проверяет, что функция возвращает пустой
    результат при отсутствии транзакций в запрашиваемой валюте."""

    result = list(filter_by_currency(sample_transactions, "EUR"))

    assert len(result) == 0
    assert result == []


def test_empty_transactions_list(empty_transactions: List[Dict[str, Any]]) -> None:
    """Тест обработки пустого списка транзакций. Проверяет, что функция корректно
    обрабатывает пустой список и возвращает пустой итератор."""

    result = list(filter_by_currency(empty_transactions, "USD"))

    assert len(result) == 0
    assert result == []


def test_transactions_with_invalid_structure(transactions_with_invalid_structure: List[Dict[str, Any]]) -> None:
    """Тест обработки транзакций с некорректной структурой. Проверяет, что функция корректно
    пропускает транзакции с отсутствующими или некорректными полями."""

    result = list(filter_by_currency(transactions_with_invalid_structure, "USD"))

    assert len(result) == 0
    assert result == []


def test_transaction_descriptions_with_sample_data(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тестирует функцию с корректными данными транзакций."""

    result = list(transaction_descriptions(sample_transactions))

    expected_descriptions = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]

    assert len(result) == 5
    assert result == expected_descriptions


def test_transaction_descriptions_empty_list() -> None:
    """Тестирует функцию с пустым списком транзакций."""

    result = list(transaction_descriptions([]))

    assert len(result) == 0
    assert result == []


def test_transaction_descriptions_with_missing_fields(transactions_with_missing_fields: List[Dict[str, Any]]) -> None:
    """Тестирует функцию с транзакциями, содержащими отсутствующие или некорректные поля."""

    result = list(transaction_descriptions(transactions_with_missing_fields))

    assert len(result) == 1
    assert result == ["Перевод со счета на счет"]


@pytest.mark.parametrize(
    "transactions_count,expected_count",
    [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
    ],
)
def test_transaction_descriptions_different_sizes(
    sample_transactions: List[Dict[str, Any]], transactions_count: int, expected_count: int
) -> None:
    """Параметризованный тест для проверки работы с разным количеством транзакций."""

    test_transactions = sample_transactions[:transactions_count]
    result = list(transaction_descriptions(test_transactions))

    assert len(result) == expected_count


@pytest.mark.parametrize(
    "transaction_data,expected_description",
    [
        ([{"description": "Тестовое описание"}], ["Тестовое описание"]),
        ([{"id": 1, "description": "Описание 1"}], ["Описание 1"]),
        ([{"description": "Первое"}, {"description": "Второе"}], ["Первое", "Второе"]),
    ],
)
def test_transaction_descriptions_various_formats(
    transaction_data: List[Dict[str, Any]], expected_description: List[str]
) -> None:
    """Параметризованный тест для проверки различных форматов транзакций."""

    result = list(transaction_descriptions(transaction_data))

    assert result == expected_description


def test_card_number_generator_basic_functionality(small_range: List[int]) -> None:
    """Тестирует базовую функциональность генератора с малым диапазоном."""

    start, stop = small_range
    result = list(card_number_generator(start, stop))

    expected = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]

    assert len(result) == 5
    assert result == expected


def test_card_number_generator_format_correctness(medium_range: List[int]) -> None:
    """Тестирует корректность форматирования номеров карт."""

    start, stop = medium_range
    result = list(card_number_generator(start, stop))

    # Проверяем формат каждой карты
    for card_number in result:
        # Должно быть 16 цифр + 3 пробела = 19 символов
        assert len(card_number) == 19
        # Должно содержать 3 пробела
        assert card_number.count(" ") == 3
        # Все группы должны состоять из 4 цифр
        groups = card_number.split(" ")
        assert len(groups) == 4
        for group in groups:
            assert len(group) == 4
            assert group.isdigit()


def test_card_number_generator_min_and_max_separately() -> None:
    """Тестирует минимальное и максимальное значения отдельно."""
    # Тестируем минимальное значение
    min_result = list(card_number_generator(0, 0))
    assert len(min_result) == 1
    assert min_result[0] == "0000 0000 0000 0000"

    # Тестируем максимальное значение
    max_result = list(card_number_generator(9999999999999999, 9999999999999999))
    assert len(max_result) == 1
    assert max_result[0] == "9999 9999 9999 9999"


def test_card_number_generator_edge_values_small(small_edge_range: List[int]) -> None:
    """Тестирует обработку крайних значений диапазона с небольшим количеством элементов."""

    start, stop = small_edge_range
    result = list(card_number_generator(start, stop))

    # Проверяем первое значение
    assert result[0] == "9999 9999 9999 9998"

    # Проверяем последнее значение
    assert result[-1] == "9999 9999 9999 9999"

    # Проверяем количество элементов
    assert len(result) == 2


def test_card_number_generator_single_number(single_number_range: List[int]) -> None:
    """Тестирует генератор с диапазоном из одного числа."""
    start, stop = single_number_range
    result = list(card_number_generator(start, stop))

    assert len(result) == 1
    assert result[0] == "0000 0000 0000 0042"


def test_card_number_generator_empty_range() -> None:
    """Тестирует генератор с некорректным диапазоном (start > stop)."""
    result = list(card_number_generator(20, 7))

    assert len(result) == 0
    assert result == []


@pytest.mark.parametrize(
    "number, expected_format",
    [
        (0, "0000 0000 0000 0000"),
        (1, "0000 0000 0000 0001"),
        (9999, "0000 0000 0000 9999"),
        (10000, "0000 0000 0001 0000"),
        (1234567890123456, "1234 5678 9012 3456"),
        (9999999999999999, "9999 9999 9999 9999"),
    ],
)
def test_card_number_generator_specific_numbers(number: int, expected_format: str) -> None:
    """Тестирует форматирование конкретных номеров карт."""

    result = list(card_number_generator(number, number))

    assert len(result) == 1
    assert result[0] == expected_format


def test_card_number_generator_generator_behavior(small_range: List[int]) -> None:
    """Тестирует поведение генератора (поочередная выдача значений)."""

    start, stop = small_range
    generator = card_number_generator(start, stop)

    # Проверяем поочередное получение значений
    assert next(generator) == "0000 0000 0000 0001"
    assert next(generator) == "0000 0000 0000 0002"
    assert next(generator) == "0000 0000 0000 0003"
    assert next(generator) == "0000 0000 0000 0004"
    assert next(generator) == "0000 0000 0000 0005"

    # Проверяем, что генератор завершился
    with pytest.raises(StopIteration):
        next(generator)
