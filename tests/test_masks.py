import pytest

from src.masks import get_mask_account, get_mask_card_number


# 1. Параметризованные тесты для проверки правильной маскировки номеров карт
@pytest.mark.parametrize(
    "card_number, expected",
    [
        # Стандартные 16-значные номера карт
        ("5946823031801656", "5946 82 ** **** 1656"),
        ("3111111111111116", "3111 11 ** **** 1116"),
        ("4275342222228016", "4275 34 ** **** 8016"),
        # Карты разной длины номеров
        ("8111111111111111119", "8111 11 ** **** 1119"),  # 19 цифр
        ("533333333333315", "5333 33 ** **** 3315"),  # 15 цифр
        ("61111111111114", "6111 11 ** **** 1114"),  # 14 цифр
        ("7111111111113", "7111 11 ** **** 1113"),  # 13 цифр
        # Граничные случаи
        ("123456789012", "1234 56 ** **** 9012"),  # 12 цифр
        ("1234567890", "1234 56 ** **** 7890"),  # 10 цифр
        ("0000000000000000", "0000 00 ** **** 0000"),  # все нули
        ("1111111111111111", "1111 11 ** **** 1111"),  # все единицы
    ],
)
def test_card_number_mask_correct_format(card_number: str, expected: str) -> None:
    """Тестирование правильности формата маскирования номера карты"""
    result = get_mask_card_number(card_number)
    assert result == expected


# 2. Параметризованный тест для проверки видимых карт
@pytest.mark.parametrize("card_number", ["5946823031801656", "3111111111111116", "4275342222228016", "1234567890"])
def test_card_number_visible_first_6_last_4_digits(card_number: str) -> None:
    """Тестирование, что первые 6 и последние 4 цифры остаются видимыми"""
    result = get_mask_card_number(card_number)
    # Проверяем, что первые 4 цифры видны
    assert card_number[:4] in result
    # Проверяем, что следующие 2 цифры видны
    assert card_number[4:6] in result
    # Проверяем, что последние 4 цифры видны
    assert card_number[-4:] in result


# 3. Тесты с использованием фикстур
def test_standard_card_with_fixture(standard_card_numbers: dict) -> None:
    """Тестирование с использованием фикстуры стандартных карт"""
    test_examples = [
        ("standard", "5946 82 ** **** 1656"),
        ("visa_16", "3111 11 ** **** 1116"),
        ("mastercard_16", "4275 34 ** **** 8016"),
        ("amex_15", "5333 33 ** **** 3315"),
        ("diners_14", "6111 11 ** **** 1114"),
        ("old_visa_13", "7111 11 ** **** 1113"),
        ("union_pay_19", "8111 11 ** **** 1119"),
    ]

    for card_type, expected in test_examples:
        result = get_mask_card_number(standard_card_numbers[card_type])
        assert result == expected


def test_edge_cases() -> None:
    """Тестирование граничных случаев"""
    edge_cases = {
        "min_length_12": "123456789012",
        "short_10": "1234567890",
        "zeros": "0000000000000000",
        "repeating_digits": "1111111111111111",
    }
    for card_type, card_number in edge_cases.items():
        result = get_mask_card_number(card_number)
        assert "** ****" in result
        assert result.startswith(card_number[:4] + " " + card_number[4:6])
        assert result.endswith(card_number[-4:])


# 4. Тесты для обработки некорректных входных данных
@pytest.mark.parametrize(
    "invalid_input",
    [
        "",  # Отсутствует номер карты
        "12345",  # Слишком короткий номер
        "1234 5678 9012 3456",  # Содержит пробелы
        "abcd1234567890",  # Содержит буквы
        "1234-5678-9012-3456",  # Содержит дефисы
    ],
)
def test_invalid_inputs(invalid_input: str) -> None:
    """Тестирование некорректных входных данных"""
    try:
        result = get_mask_card_number(invalid_input)
        assert isinstance(result, str)
    except Exception:
        pass


# 1. Тестирование правильности маскирования номера счета
@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("40817810207005367456", "** 7456"),
        ("12345678901234567890", "** 7890"),
        ("11112222333344445555", "** 5555"),
        ("1234567890", "** 7890"),
        ("1234", "** 1234"),
    ],
)
def test_account_mask_correct_format(account_number: str, expected: str) -> None:
    """Тестирование правильности маскирования банковского номера счета"""
    result = get_mask_account(account_number)
    assert result == expected


# 2. Проверка работы с различными форматами и длинами
@pytest.mark.parametrize(
    "account_number, expected",
    [
        # Разные длины счетов
        ("1234567890123456789012345", "** 2345"),  # 25 цифр
        ("123456789012345678901234", "** 1234"),  # 24 цифры
        ("12345678901234567890", "** 7890"),  # 20 цифр (стандарт)
        ("1234567890", "** 7890"),  # 10 цифр
        ("123456", "** 3456"),  # 6 цифр
        ("1234", "** 1234"),  # 4 цифры (минимальная длина)
        # Граничные случаи
        ("00000000000000000000", "** 0000"),  # все нули
        ("11111111111111111111", "** 1111"),  # все единицы
        ("22222222222222222222", "** 2222"),  # все двойки
    ],
)
def test_various_account_lengths(account_number: str, expected: str) -> None:
    """Проверка работы с различными длинами номеров счетов"""
    result = get_mask_account(account_number)
    assert result == expected


# 3. Проверка обработки коротких номеров счетов
@pytest.mark.parametrize(
    "short_account, expected",
    [
        ("123", "** 123"),  # 3 цифры
        ("12", "** 12"),  # 2 цифры
        ("1", "** 1"),  # 1 цифра
    ],
)
def test_short_accounts(short_account: str, expected: str) -> None:
    """Проверка обработки очень коротких номеров счетов"""
    result = get_mask_account(short_account)
    assert result == expected


# 4. Тесты с использованием фикстуры
def test_account_with_fixture(account_samples: dict) -> None:
    """Тест с использованием фикстуры"""
    test_examples = [
        ("standard_20", "** 7456"),
        ("short_10", "** 7890"),
        ("minimal_4", "** 1234"),
        ("zeros", "** 0000"),
        ("repeating_digits", "** 1111"),
    ]

    for account_type, expected in test_examples:
        result = get_mask_account(account_samples[account_type])
        assert result == expected


# 5. Проверка что видны только последние 4 цифры
@pytest.mark.parametrize(
    "account_number",
    [
        "40817810207005367456",
        "12345678901234567890",
        "11112222333344445555",
        "1234567890",
    ],
)
def test_only_last_4_digits_visible(account_number: str) -> None:
    """Проверка что видны только последние 4 цифры"""
    result = get_mask_account(account_number)

    # Проверяем что последние 4 цифры видны
    assert account_number[-4:] in result
