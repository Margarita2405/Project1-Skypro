from typing import List, Dict, Any

from src.transaction_processor import process_bank_search


def test_search_by_word(basic_transactions: List[Dict[str, Any]]) -> None:
    """Тестирует поиск транзакций по обычному слову."""

    result = process_bank_search(basic_transactions, "перевод")

    # Проверяем количество найденных транзакций
    assert len(result) == 3, f"Ожидалось 3 транзакции с 'перевод', найдено {len(result)}"

    # Проверяем ID найденных транзакций
    found_ids = {t["id"] for t in result}
    expected_ids = {"650703", "3598919", "5294458"}
    assert found_ids == expected_ids, f"Найдены ID: {found_ids}, ожидались: {expected_ids}"

    # Проверяем, что все найденные транзакции содержат слово "перевод"
    for transaction in result:
        assert "перевод" in transaction["description"].lower()


def test_search_case_insensitive(basic_transactions: List[Dict[str, Any]]) -> None:
    """Тестирует поиск без учета регистра."""

    result_lower = process_bank_search(basic_transactions, "перевод")
    result_upper = process_bank_search(basic_transactions, "ПЕРЕВОД")
    result_mixed = process_bank_search(basic_transactions, "ПеРеВоД")

    # Все варианты должны давать одинаковый результат
    assert len(result_lower) == len(result_upper) == len(result_mixed)

    # Проверяем, что ID транзакций одинаковые
    ids_lower = {t["id"] for t in result_lower}
    ids_upper = {t["id"] for t in result_upper}
    ids_mixed = {t["id"] for t in result_mixed}

    assert ids_lower == ids_upper == ids_mixed


def test_search_by_phrase(basic_transactions: List[Dict[str, Any]]) -> None:
    """Тестирует поиск по точной фразе."""

    result = process_bank_search(basic_transactions, "Открытие вклада")

    # Проверяем количество найденных транзакций
    assert len(result) == 2, f"Ожидалось 2 транзакции, найдено {len(result)}"

    # Проверяем ID найденных транзакций
    found_ids = {t["id"] for t in result}
    expected_ids = {"5380041", "3107343"}
    assert found_ids == expected_ids, f"Найдены ID: {found_ids}, ожидались: {expected_ids}"

    # Проверяем точное совпадение описания
    for transaction in result:
        assert transaction["description"] == "Открытие вклада"


def test_empty_search_string(basic_transactions: List[Dict[str, Any]]) -> None:
    """Тестирует поиск с пустой строкой."""

    result = process_bank_search(basic_transactions, "")

    # При пустой строке должны вернуться все транзакции (копия)
    assert len(result) == len(basic_transactions)
    assert result is not basic_transactions  # Должна быть копия

    # Проверяем, что все транзакции присутствуют
    original_ids = {t["id"] for t in basic_transactions}
    result_ids = {t["id"] for t in result}
    assert original_ids == result_ids


def test_no_matching_transactions(basic_transactions: List[Dict[str, Any]]) -> None:
    """Тестирует поиск несуществующей строки."""
    result = process_bank_search(basic_transactions, "несуществующий текст")

    # Должен вернуться пустой список
    assert result == []
    assert len(result) == 0


def test_empty_input_data(empty_transactions: List[Dict[str, Any]]) -> None:
    """Тестирует обработку пустого списка транзакций."""

    # С пустым запросом
    result1 = process_bank_search(empty_transactions, "")
    assert result1 == []

    # С непустым запросом
    result2 = process_bank_search(empty_transactions, "перевод")
    assert result2 == []


def test_transactions_without_description(transactions_without_description: List[Dict[str, Any]]) -> None:
    """Тестирует обработку транзакций без поля 'description'."""

    result = process_bank_search(transactions_without_description, "перевод")

    # Должны найтись только транзакции с описанием, содержащим "перевод"
    assert len(result) == 2
    found_ids = {t["id"] for t in result}
    assert found_ids == {"1", "3"}


def test_transactions_with_empty_description(transactions_with_empty_description: List[Dict[str, Any]]) -> None:
    """Тестирует обработку транзакций с пустым описанием."""

    result = process_bank_search(transactions_with_empty_description, "перевод")

    # Должны найтись только транзакции с непустым описанием, содержащим "перевод"
    assert len(result) == 2
    found_ids = {t["id"] for t in result}
    assert found_ids == {"1", "4"}


def test_regular_expression_search(basic_transactions: List[Dict[str, Any]]) -> None:
    """Тестирует поиск с использованием регулярных выражений."""

    # Поиск по шаблону
    result1 = process_bank_search(basic_transactions, ".*карты.*")
    assert len(result1) == 2

    # Поиск с альтернацией
    result2 = process_bank_search(basic_transactions, "перевод|вклад")
    assert len(result2) == 5

    # Поиск с начала строки
    result3 = process_bank_search(basic_transactions, "^Перевод")
    assert len(result3) == 3

    # Поиск с конца строки
    result4 = process_bank_search(basic_transactions, "вклада$")
    assert len(result4) == 2


def test_invalid_regular_expression(basic_transactions: List[Dict[str, Any]]) -> None:
    """Тестирует обработку невалидного регулярного выражения."""

    # Невалидное регулярное выражение
    result = process_bank_search(basic_transactions, "[a-z")

    # Должен вернуться пустой список
    assert result == []


def test_mixed_case_search(transactions_mixed_case: List[Dict[str, Any]]) -> None:
    """Тестирует поиск в данных с разным регистром."""

    # Поиск должен находить транзакции независимо от регистра
    result = process_bank_search(transactions_mixed_case, "перевод")
    assert len(result) == 3

    # Проверяем ID найденных транзакций
    found_ids = {t["id"] for t in result}
    assert found_ids == {"1", "2", "4"}
