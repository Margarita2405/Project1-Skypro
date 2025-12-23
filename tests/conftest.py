from typing import Any, Dict, List, Tuple

import pytest


# Фикстура для для создания входных данных для тестов
@pytest.fixture
def standard_card_numbers() -> Dict[str, str]:
    """Фикстура со стандартными номерами банковских карт для тестирования"""
    return {
        "standard": "5946823031801656",
        "visa_16": "3111111111111116",
        "mastercard_16": "4275342222228016",
        "amex_15": "533333333333315",
        "diners_14": "61111111111114",
        "old_visa_13": "7111111111113",
        "union_pay_19": "8111111111111111119",
    }


@pytest.fixture
def edge_case_card_numbers() -> Dict[str, str]:
    """Фикстура с граничными случаями для тестирования"""
    return {
        "min_length_12": "123456789012",
        "short_10": "1234567890",
        "zeros": "0000000000000000",
        "repeating_digits": "1111111111111111",
    }


# Фикстура с тестовыми номерами счетов
@pytest.fixture
def account_samples() -> Dict[str, str]:
    """Фикстура с номерами счетов для тестирования"""
    return {
        "standard_20": "40817810207005367456",
        "short_10": "1234567890",
        "long_25": "1234567890123456789012345",
        "minimal_4": "1234",
        "zeros": "00000000000000000000",
        "repeating_digits": "11111111111111111111",
    }


# Фикстуры для тестовых данных
@pytest.fixture
def valid_card_examples() -> List[str]:
    """Фикстура с валидными примерами карт разных типов"""
    return [
        "Visa Platinum 7000792289606361",
        "Maestro 1596837868705199",
        "MasterCard 7158300734726758",
        "Visa Classic 6831982476737658",
        "Visa Platinum 8990922113665229",
        "Visa Gold 5999414228426353",
    ]


@pytest.fixture
def valid_account_examples() -> List[str]:
    """Фикстура с валидными примерами счетов"""
    return ["Счет 73654108430135874305", "Счет 64686473678894779589", "Счет 35383033474447895560"]


@pytest.fixture
def invalid_input_examples() -> List[Tuple[str, str]]:
    """Фикстура с некорректными входными данными и ожидаемыми ошибками"""
    return [
        # (input_data, expected_error_message)
        ("VisaPlatinum7000792289606361", "Некорректный формат строки"),
        ("", "Некорректный формат строки"),
        ("Счет", "Некорректный формат строки"),
        ("Visa Platinum 7000abc89606361", "Некорректный ввод, номер должен состоять только из цифр"),
        ("Счет 7365410843abc5874305", "Некорректный ввод, номер должен состоять только из цифр"),
        ("Счет 1234567890123456789", "Некорректный ввод, номер счета слишком короткий"),  # 19 цифр
        ("Visa Platinum 123456789012345", "Некорректный ввод, номер карты слишком короткий"),  # 15 цифр
    ]


@pytest.fixture
def sample_dates() -> List[Tuple[str, str]]:
    """Фикстура с примерами дат для тестирования"""
    return [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2025-07-23T10:45:34.256130", "23.07.2025"),
        ("2000-01-01T00:00:00.000000", "01.01.2000"),
    ]


@pytest.fixture
def sample_operations() -> List[Dict[str, Any]]:
    """Фикстура с примерами операций для тестирования"""
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


# Фикстура с тестовыми данными
@pytest.fixture
def samples_operations() -> List[Dict[str, Any]]:
    """Фикстура с примерами операций для тестирования"""
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


# Фикстура с операциями с одинаковыми датами
@pytest.fixture
def operations_with_same_dates() -> List[Dict[str, Any]]:
    """Фикстура с операциями, содержащими одинаковые даты"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-15T10:30:00.000000"},
        {"id": 2, "state": "CANCELED", "date": "2023-01-15T10:30:00.000000"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-15T10:30:00.000000"},
        {"id": 4, "state": "PENDING", "date": "2022-05-20T14:25:00.000000"},
    ]


# Фикстуры для тестовых данных функции filter_by_currency
@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с примером транзакций с разными валютами и состояниями для тестирования."""
    return [
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


@pytest.fixture
def transactions_with_invalid_structure() -> List[Dict[str, Any]]:
    """Фикстура с транзакциями, имеющими некорректную структуру с отсутствующими полями."""
    return [
        {"id": 1, "state": "EXECUTED"},  # Нет operationAmount
        {"id": 2, "operationAmount": {"amount": "500.00"}},  # Нет currency
        {"id": 3, "operationAmount": {"currency": {"name": "руб."}}},  # Нет code
        {"id": 4, "operationAmount": {"amount": "300.00", "currency": {}}},  # Пустой currency
    ]


@pytest.fixture
def empty_transactions() -> List[Dict[str, Any]]:
    """Фикстура с пустым списком транзакций."""
    return []


# Фикстура для тестовых данных генератора transaction_descriptions
@pytest.fixture
def transactions_with_missing_fields() -> List[Dict[str, Any]]:
    """Фикстура предоставляет транзакции с отсутствующими или некорректными полями."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            # Отсутствует поле description
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


# Фикстуры для тестовых данных генератора card_number_generator
@pytest.fixture
def small_range() -> List[int]:
    """Фикстура предоставляет малый диапазон для тестирования."""
    return [1, 5]


@pytest.fixture
def medium_range() -> List[int]:
    """Фикстура предоставляет средний диапазон для тестирования."""
    return [1000, 1005]


@pytest.fixture
def edge_range() -> List[int]:
    """Фикстура предоставляет крайние значения для тестирования."""
    return [0, 9999999999999999]


@pytest.fixture
def small_edge_range() -> List[int]:
    """Фикстура предоставляет небольшой диапазон для тестирования крайних случаев."""
    return [9999999999999998, 9999999999999999]


@pytest.fixture
def single_number_range() -> List[int]:
    """Фикстура предоставляет диапазон из одного числа."""
    return [42, 42]


@pytest.fixture
def basic_transactions() -> List[Dict[str, Any]]:
    """Фикстура с базовыми тестовыми транзакциями."""
    return [
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
        {
            "id": "5294458",
            "state": "EXECUTED",
            "date": "2022-06-20T18:08:20Z",
            "amount": 16836,
            "currency_name": "Yuan Renminbi",
            "currency_code": "CNY",
            "from": "Visa 2759011965877198",
            "to": "Счет 38287443300766991082",
            "description": "Перевод с карты на карту",
        },
        {
            "id": "3107343",
            "state": "EXECUTED",
            "date": "2023-01-25T13:33:00Z",
            "amount": 33639,
            "currency_name": "Krona",
            "currency_code": "SEK",
            "from": "",
            "to": "Счет 35662766798195077538",
            "description": "Открытие вклада",
        },
    ]


@pytest.fixture
def transactions_without_description() -> List[Dict[str, Any]]:
    """Фикстура с транзакциями, у некоторых из которых отсутствует описание."""
    return [
        {
            "id": "1",
            "state": "EXECUTED",
            "description": "Перевод организации",
            "amount": 1000,
        },
        {
            "id": "2",
            "state": "EXECUTED",
            "amount": 2000,
            # Отсутствует поле 'description'
        },
        {
            "id": "3",
            "state": "CANCELED",
            "description": "Перевод с карты на карту",
            "amount": 3000,
        },
        {
            "id": "4",
            "state": "EXECUTED",
            "amount": 4000,
            # Отсутствует поле 'description'
        },
    ]


@pytest.fixture
def transactions_with_empty_description() -> List[Dict[str, Any]]:
    """Фикстура с транзакциями с пустым или состоящим из пробелов описанием."""
    return [
        {
            "id": "1",
            "state": "EXECUTED",
            "description": "Перевод организации",
            "amount": 1000,
        },
        {
            "id": "2",
            "state": "EXECUTED",
            "description": "",  # Пустая строка
            "amount": 2000,
        },
        {
            "id": "3",
            "state": "CANCELED",
            "description": "   ",  # Только пробелы
            "amount": 3000,
        },
        {
            "id": "4",
            "state": "EXECUTED",
            "description": "Перевод с карты на карту",
            "amount": 4000,
        },
    ]


@pytest.fixture
def transactions_mixed_case() -> List[Dict[str, Any]]:
    """Фикстура с транзакциями с разным регистром в описании."""
    return [
        {
            "id": "1",
            "state": "EXECUTED",
            "description": "Перевод Организации",
            "amount": 1000,
        },
        {
            "id": "2",
            "state": "EXECUTED",
            "description": "ПЕРЕВОД С КАРТЫ НА КАРТУ",
            "amount": 2000,
        },
        {
            "id": "3",
            "state": "CANCELED",
            "description": "открытие вклада",
            "amount": 3000,
        },
        {
            "id": "4",
            "state": "EXECUTED",
            "description": "ПереВод Другу",
            "amount": 4000,
        },
    ]


# Фикстура для тестовых данных в модуле test_bank_operations
@pytest.fixture
def test_data() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми данными о банковских операциях."""
    return [
        {"id": "1", "description": "Перевод организации"},
        {"id": "2", "description": "Перевод с карты на карту"},
        {"id": "3", "description": "Открытие вклада"},
        {"id": "4", "description": "Перевод со счета на счет"},
        {"id": "5", "description": "Перевод организации"},
        {"id": "6", "description": "Открытие вклада"},
        {"id": "7", "description": "Перевод с карты на карту"},
    ]


# Фикстура для категорий в модуле test_bank_operations
@pytest.fixture
def categories() -> List[str]:
    """Фикстура с категориями для поиска."""
    return [
        "перевод организации",
        "открытие вклада",
        "перевод с карты на карту",
        "перевод со счета на счет"
    ]
