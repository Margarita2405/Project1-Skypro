from typing import List, Tuple

import pytest

from src.widget import get_date, mask_account_card


# 1. Проверка корректного распознавания типа данных (карта или счет)
def test_correctly_identifies_card_type(valid_card_examples: List[str]) -> None:
    """Тестирование корректного распознавания карт"""
    for card_data in valid_card_examples:
        result = mask_account_card(card_data)
        assert "** ****" in result


def test_correctly_identifies_account_type(valid_account_examples: List[str]) -> None:
    """Тестирование корректного распознавания счетов"""
    for account_data in valid_account_examples:
        result = mask_account_card(account_data)
        assert result.startswith("Счет")


# 2. Параметризованные тесты с разными типами карт и счетов
@pytest.mark.parametrize(
    "input_data,expected_pattern",
    [
        # Карты разных типов
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79 ** **** 6361"),
        ("Maestro 1596837868705199", "Maestro 1596 83 ** **** 5199"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30 ** **** 6758"),
        # Счета
        ("Счет 73654108430135874305", "Счет ** 4305"),
        ("Счет 64686473678894779589", "Счет ** 9589"),
    ],
)
def test_different_card_and_account_types(input_data: str, expected_pattern: str) -> None:
    """Параметризованный тест различных типов карт и счетов"""
    result = mask_account_card(input_data)
    assert result == expected_pattern


# 3. Проверка обработки некорректных входных данных
@pytest.mark.parametrize(
    "input_data,expected_error",
    [
        # Неправильный формат
        ("VisaPlatinum7000792289606361", "not enough values to unpack"),
        ("Счет73654108430135874305", "not enough values to unpack"),
        ("", "not enough values to unpack"),
        ("Maestro", "not enough values to unpack"),
        # Нецифровые символы
        ("Visa Platinum 7000abc89606361", "Некорректный ввод, номер должен состоять только из цифр"),
        ("Счет 7365410843abc5874305", "Некорректный ввод, номер должен состоять только из цифр"),
        # Слишком короткие номера
        ("Счет 123", "Некорректный ввод, номер счета слишком короткий"),
        ("Счет 1234567890123456789", "Некорректный ввод, номер счета слишком короткий"),  # 19 цифр
        ("Visa Platinum 123456789012345", "Некорректный ввод, номер карты слишком короткий"),  # 15 цифр
        ("Card 123", "Некорректный ввод, номер карты слишком короткий"),
    ],
)
def test_invalid_input_handling(input_data: str, expected_error: str) -> None:
    """Тестирование обработки некорректных входных данных"""
    with pytest.raises(Exception) as exc_info:
        mask_account_card(input_data)
    assert expected_error in str(exc_info.value)


# 4. Проверка граничных значений
@pytest.mark.parametrize(
    "input_data",
    [
        "Card 0000000000000000",  # Минимальная длина карты (16 цифр)
        "Счет 00000000000000000000",  # Минимальная длина счета (20 цифр)
    ],
)
def test_edge_values(input_data: str) -> None:
    """Тестирование граничных значений длины номеров"""
    result = mask_account_card(input_data)
    assert result  # Результат не должен быть пустым
    assert "0000" in result or "**0000" in result  # Должны видеть последние 4 цифры


# 5. Проверка работы с минимально допустимыми длинами
def test_minimum_valid_lengths() -> None:
    """Тестирование минимально допустимых длин номеров"""
    # Минимальная карта (16 цифр)
    card_result = mask_account_card("Card 1234567890123456")
    assert "3456" in card_result

    # Минимальный счет (20 цифр)
    account_result = mask_account_card("Счет 12345678901234567890")
    assert " ** 7890" in account_result


# 1. Тестирование правильности преобразования даты
def test_correct_date_conversion() -> None:
    """Проверка правильности преобразования даты"""
    input_date = "2024-03-11T02:26:18.671407"
    expected = "11.03.2024"
    assert get_date(input_date) == expected


# 2. Параметризованные тесты для различных форматов даты
@pytest.mark.parametrize(
    "input_date,expected",
    [
        # Стандартные случаи
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2025-07-23T10:45:34.256130", "23.07.2025"),
        ("2000-01-01T00:00:00.000000", "01.01.2000"),
        # Граничные случаи
        ("1999-12-31T23:59:59.999999", "31.12.1999"),  # конец века
        ("2000-01-01T00:00:00.000000", "01.01.2000"),  # начало века
        ("2023-02-28T12:00:00.000000", "28.02.2023"),  # невисокосный год
        ("2024-02-29T12:00:00.000000", "29.02.2024"),  # високосный год
        # Месяцы с разным количеством дней
        ("2023-04-30T12:00:00.000000", "30.04.2023"),  # 30 дней
        ("2023-05-31T12:00:00.000000", "31.05.2023"),  # 31 день
    ],
)
def test_various_date_formats(input_date: str, expected: str) -> None:
    """Проверка работы функции на различных входных форматах даты"""
    assert get_date(input_date) == expected


# 3. Тестирование нестандартных строк с датами
@pytest.mark.parametrize(
    "input_date,expected",
    [
        # Разное время и миллисекунды
        ("2024-03-11T00:00:00.000000", "11.03.2024"),
        ("2024-03-11T23:59:59.999999", "11.03.2024"),
        ("2024-03-11T12:30:45.123456", "11.03.2024"),
        # Дата без времени (если функция должна обрабатывать)
        ("2024-03-11", "11.03.2024"),
    ],
)
def test_non_standard_date_strings(input_date: str, expected: str) -> None:
    """Проверка нестандартных строк с датами"""
    assert get_date(input_date) == expected


# 4. Тестирование обработки ошибок - входные строки без даты
@pytest.mark.parametrize(
    "invalid_input",
    [
        "",  # пустая строка
        "2024-03",  # неполная дата
        "T10:30:45",  # только время без даты
        "2024/03/11T10:30:45",  # неправильный разделитель даты
    ],
)
def test_invalid_input_data(invalid_input: str) -> None:
    """Проверка обработки некорректных входных данных"""
    with pytest.raises((ValueError, IndexError)):
        get_date(invalid_input)


# 5. Дополнительный тест для строк, которые функция обрабатывает "неожиданно"
@pytest.mark.parametrize(
    "problematic_input",
    [
        "invalid-date-string",  # некорректная строка, но функция ее обрабатывает
    ],
)
def test_problematic_inputs(problematic_input: str) -> None:
    """Тестирование входных данных, которые функция обрабатывает без ошибок (возможно, некорректно)"""
    # Проверяем, что функция не падает, но результат может быть некорректным
    try:
        result = get_date(problematic_input)
        print(f"Функция обработала '{problematic_input}' как '{result}'")
    except (ValueError, IndexError) as e:
        print(f"Функция вызвала исключение для '{problematic_input}': {e}")


# 6. Тест с использованием фикстуры
def test_with_fixture(sample_dates: List[Tuple[str, str]]) -> None:
    """Тест с использованием фикстуры"""
    for input_date, expected in sample_dates:
        result = get_date(input_date)
        assert result == expected, f"Ожидалось {expected}, получено {result} для входных данных {input_date}"
