from typing import List, Dict, Any, cast
import pytest

from src.bank_operations import process_bank_operations


def test_basic_functionality(test_data: List[Dict[str, Any]], categories: List[str]) -> None:
    """Тестируем основную функциональность - подсчет операций по категориям."""
    result = process_bank_operations(test_data, categories)

    # Проверяем что функция возвращает словарь
    assert isinstance(result, dict)

    # Проверяем правильность подсчета
    assert result["перевод организации"] == 2
    assert result["открытие вклада"] == 2
    assert result["перевод с карты на карту"] == 2
    assert result["перевод со счета на счет"] == 1


def test_case_insensitivity() -> None:
    """Тестируем что поиск категорий регистронезависимый."""
    data = [
        {"description": "ПЕРЕВОД ОРГАНИЗАЦИИ"},  # Все буквы заглавные
        {"description": "Перевод Организации"},  # Смешанный регистр
        {"description": "перевод организации"},  # Все строчные
    ]
    categories = ["перевод организации"]

    result = process_bank_operations(data, categories)

    # Все три записи должны быть найдены
    assert result["перевод организации"] == 3


def test_empty_data_list(categories: List[str]) -> None:
    """Тестируем обработку пустого списка операций."""
    empty_data: List[Dict[str, Any]] = []

    result = process_bank_operations(empty_data, categories)

    # При пустых данных все счетчики должны быть 0
    assert result["перевод организации"] == 0
    assert result["открытие вклада"] == 0
    assert result["перевод с карты на карту"] == 0
    assert result["перевод со счета на счет"] == 0


def test_empty_categories_list(test_data: List[Dict[str, Any]]) -> None:
    """Тестируем обработку пустого списка категорий."""
    empty_categories: List[str] = []

    result = process_bank_operations(test_data, empty_categories)

    # При пустых категориях должен вернуться пустой словарь
    assert result == {}


def test_transaction_without_description() -> None:
    """Тестируем обработку транзакций без поля 'description'."""
    data = [
        {"id": "1"},  # Нет поля description
        {"id": "2", "description": "Перевод организации"},
        {"id": "3", "other": "value"},  # Есть другие поля, но нет description
    ]
    categories = ["перевод организации"]

    result = process_bank_operations(data, categories)

    # Только одна операция с description должна быть учтена
    assert result["перевод организации"] == 1


def test_invalid_description_type() -> None:
    """Тестируем обработку нестроковых значений в поле 'description'."""
    data: List[Dict[str, Any]] = [
        {"description": "Перевод организации"},
        {"description": 123},  # Число вместо строки
        {"description": None},  # None значение
        {"description": ["список"]},  # Список вместо строки
    ]
    categories = ["перевод организации"]

    result = process_bank_operations(data, categories)

    # Только первая валидная строка должна быть учтена
    assert result["перевод организации"] == 1


def test_empty_string_description() -> None:
    """Тестируем обработку пустых строк и строк из пробелов."""
    data = [
        {"description": ""},  # Пустая строка
        {"description": "   "},  # Только пробелы
        {"description": "Перевод организации"},
    ]
    categories = ["перевод организации"]

    result = process_bank_operations(data, categories)

    # Только последняя непустая строка должна быть учтена
    assert result["перевод организации"] == 1


def test_type_error_for_invalid_data() -> None:
    """Тестируем что функция выбрасывает TypeError при неправильном типе данных."""
    invalid_data = cast(List[Dict[str, Any]], "не список")  # Строка вместо списка
    categories = ["категория"]

    # Ожидаем исключение TypeError
    with pytest.raises(TypeError) as exc_info:
        process_bank_operations(invalid_data, categories)

    # Проверяем текст ошибки
    assert "Параметр 'data' должен быть списком" in str(exc_info.value)


def test_type_error_for_invalid_categories() -> None:
    """Тестируем что функция выбрасывает TypeError при неправильном типе категорий."""
    data = [{"description": "операция"}]
    invalid_categories = cast(List[str], "не список")  # Строка вместо списка

    # Ожидаем исключение TypeError
    with pytest.raises(TypeError) as exc_info:
        process_bank_operations(data, invalid_categories)

    # Проверяем текст ошибки
    assert "Параметр 'categories' должен быть списком" in str(exc_info.value)


def test_partial_category_match() -> None:
    """Тестируем что категория ищется как подстрока в описании."""
    data = [
        {"description": "Срочный перевод организации клиенту"},
        {"description": "перевод"},  # Не содержит полное название категории
    ]
    categories = ["перевод организации"]

    result = process_bank_operations(data, categories)

    # Только первая запись содержит полную категорию
    assert result["перевод организации"] == 1


def test_multiple_categories_in_one_description() -> None:
    """Тестируем когда в одном описании встречается несколько категорий."""
    data = [
        {"description": "Перевод организации и открытие вклада одновременно"},
    ]
    categories = ["перевод организации", "открытие вклада"]

    result = process_bank_operations(data, categories)

    # Обе категории должны быть найдены в одной записи
    assert result["перевод организации"] == 1
    assert result["открытие вклада"] == 1


def test_no_matching_categories() -> None:
    """Тестируем когда ни одна категория не совпадает с описаниями."""
    data = [
        {"description": "Оплата услуг"},
        {"description": "Покупка товаров"},
    ]
    categories = ["перевод организации", "открытие вклада"]

    result = process_bank_operations(data, categories)

    # Все счетчики должны быть 0
    assert result["перевод организации"] == 0
    assert result["открытие вклада"] == 0
