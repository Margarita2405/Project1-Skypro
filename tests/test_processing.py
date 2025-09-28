from typing import Any, Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date


# 1. Тестирование фильтрации по умолчанию (EXECUTED)
def test_filter_by_default_state(sample_operations: List[Dict[str, Any]]) -> None:
    """Тестирование фильтрации списка словарей по статусу по умолчанию (EXECUTED)"""
    result: List[Dict[str, Any]] = filter_by_state(sample_operations)

    # Проверяем что все операции в результате имеют статус EXECUTED
    assert all(operations["state"] == "EXECUTED" for operations in result)

    # Проверяем количество найденных операций
    assert len(result) == 2

    # Проверяем что возвращаются правильные ID
    result_ids = [operations["id"] for operations in result]
    expected_ids = [41428829, 939719570]
    assert result_ids == expected_ids


# 2. Параметризованные тесты для различных статусов
@pytest.mark.parametrize(
    "state,expected_count,expected_ids",
    [
        ("EXECUTED", 2, [41428829, 939719570]),
        ("CANCELED", 2, [594226727, 615064591]),
        ("PENDING", 0, []),  # статус которого нет в данных
    ],
)
def test_filter_by_various_states(
    sample_operations: List[Dict[str, Any]], state: str, expected_count: int, expected_ids: List[int]
) -> None:
    """Параметризация тестов для различных возможных значений статуса state"""
    result: List[Dict[str, Any]] = filter_by_state(sample_operations, state)

    # Проверяем количество операций
    assert len(result) == expected_count

    # Проверяем что все операции имеют указанный статус
    assert all(op["state"] == state for op in result)

    # Проверяем ID операций
    result_ids = [op["id"] for op in result]
    assert result_ids == expected_ids


# 3. Тестирование при отсутствии словарей с указанным статусом
def test_filter_empty_result(sample_operations: List[Dict[str, Any]]) -> None:
    """Проверка работы функции при отсутствии словарей с указанным статусом"""
    result: List[Dict[str, Any]] = filter_by_state(sample_operations, "UNKNOWN_STATE")

    # Проверяем что возвращается пустой список
    assert result == []
    assert len(result) == 0


# 4. Тестирование с пустым списком операций
def test_filter_empty_list() -> None:
    """Тестирование функции с пустым списком операций"""
    empty_list: List[Dict[str, Any]] = []
    result: List[Dict[str, Any]] = filter_by_state(empty_list, "EXECUTED")

    assert result == []
    assert len(result) == 0


# 5. Тестирование операций без ключа 'state'
def test_operations_without_state_key() -> None:
    """Тестирование операций, у которых отсутствует ключ 'state'"""
    operations_without_state: List[Dict[str, Any]] = [
        {"id": 1, "date": "2019-01-01T00:00:00.000000"},  # нет ключа state
        {"id": 2, "state": "EXECUTED", "date": "2019-01-02T00:00:00.000000"},
        {"id": 3, "date": "2019-01-03T00:00:00.000000"},  # нет ключа state
    ]

    result: List[Dict[str, Any]] = filter_by_state(operations_without_state, "EXECUTED")

    # Должна вернуться только одна операция с ключом state
    assert len(result) == 1
    assert result[0]["id"] == 2


# 1. Тестирование сортировки по убыванию (по умолчанию)
def test_sort_descending(sample_operations: List[Dict[str, Any]]) -> None:
    """Тестирование сортировки списка словарей по датам в порядке убывания"""
    result: List[Dict[str, Any]] = sort_by_date(sample_operations)

    # Проверяем порядок дат (должны идти от самой новой к самой старой)
    dates = [op["date"] for op in result]

    # Получаем даты из sample_operations и сортируем их вручную для сравнения
    original_dates = [op["date"] for op in sample_operations]
    expected_dates = sorted(original_dates, reverse=True)

    assert dates == expected_dates
    # Проверяем что первая операция имеет самую позднюю дату
    assert result[0]["date"] == expected_dates[0]
    # Проверяем что последняя операция имеет самую раннюю дату
    assert result[-1]["date"] == expected_dates[-1]


# 2. Тестирование сортировки по возрастанию
def test_sort_ascending(sample_operations: List[Dict[str, Any]]) -> None:
    """Тестирование сортировки списка словарей по датам в порядке возрастания"""
    result: List[Dict[str, Any]] = sort_by_date(sample_operations, reverse=False)

    # Проверяем порядок дат (должны идти от самой старой к самой новой)
    dates = [op["date"] for op in result]

    # Получаем даты из sample_operations и сортируем их вручную для сравнения
    original_dates = [op["date"] for op in sample_operations]
    expected_dates = sorted(original_dates)

    assert dates == expected_dates
    # Проверяем что первая операция имеет самую раннюю дату
    assert result[0]["date"] == expected_dates[0]
    # Проверяем что последняя операция имеет самую позднюю дату
    assert result[-1]["date"] == expected_dates[-1]


# 3. Тестирование сортировки при одинаковых датах
def test_sort_with_same_dates(operations_with_same_dates: List[Dict[str, Any]]) -> None:
    """Проверка корректности сортировки при одинаковых датах"""
    result: List[Dict[str, Any]] = sort_by_date(operations_with_same_dates)

    # При одинаковых датах порядок должен сохраниться как в исходном списке
    # (так работает стандартная сортировка Python)
    dates = [op["date"] for op in result]

    # Проверяем что даты отсортированы правильно
    assert dates[0] == "2023-01-15T10:30:00.000000"
    assert dates[1] == "2023-01-15T10:30:00.000000"
    assert dates[2] == "2023-01-15T10:30:00.000000"
    assert dates[3] == "2022-05-20T14:25:00.000000"

    # 4. Параметризованные тесты для различных вариантов сортировки
    @pytest.mark.parametrize(
        "reverse,expected_first_date,expected_last_date",
        [
            (True, "2019-07-03T18:35:29.512364", "2018-06-30T02:08:58.425572"),  # по убыванию
            (False, "2018-06-30T02:08:58.425572", "2019-07-03T18:35:29.512364"),  # по возрастанию
        ],
    )
    def test_sort_parameterized(
        sample_operations: List[Dict[str, Any]],
        reverse: bool,
        expected_first_date: str,
        expected_last_date: str,
    ) -> None:
        """Параметризация тестов для различных направлений сортировки"""
        result: List[Dict[str, Any]] = sort_by_date(sample_operations, reverse=reverse)

        assert result[0]["date"] == expected_first_date
        assert result[-1]["date"] == expected_last_date

    # 5. Тестирование с пустым списком
    def test_sort_empty_list() -> None:
        """Тестирование функции с пустым списком операций"""
        empty_list: List[Dict[str, Any]] = []
        result: List[Dict[str, Any]] = sort_by_date(empty_list)

        assert result == []
        assert len(result) == 0

    # 6. Тестирование с некорректными форматами дат
    def test_invalid_date_formats() -> None:
        """Тесты на работу функции с некорректными или нестандартными форматами дат"""
        operations_with_invalid_dates: List[Dict[str, Any]] = [
            {"id": 1, "state": "EXECUTED", "date": "2023-01-15T10:30:00.000000"},  # корректная
            {"id": 2, "state": "EXECUTED", "date": "invalid-date-format"},  # некорректная
            {"id": 3, "state": "EXECUTED", "date": "2023/01/15 10:30:00"},  # нестандартная
            {"id": 4, "state": "EXECUTED", "date": "2023-01-15"},  # неполная
        ]

        # Функция должна отработать без ошибок (сортировка по строковому сравнению)
        result: List[Dict[str, Any]] = sort_by_date(operations_with_invalid_dates)

        # Проверяем что список возвращается (поведение может быть разным)
        assert len(result) == 4
        assert isinstance(result, list)
