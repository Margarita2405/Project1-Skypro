import pytest
from unittest.mock import patch
import pandas as pd
from src.transactions_csv import read_transactions_from_csv


def test_file_not_found() -> None:
    """Тест на случай, когда файл не существует. Проверяет, что функция корректно
    выбрасывает FileNotFoundError при попытке чтения несуществующего файла"""

    # Мокируем os.path.exists чтобы возвращать False (файл не существует)
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = False

        # Проверяем, что функция выбрасывает FileNotFoundError
        with pytest.raises(FileNotFoundError):
            read_transactions_from_csv("nonexistent_file.csv")


def test_successful_read() -> None:
    """Тест успешного чтения CSV-файла"""

    # Создаем тестовые данные, имитирующие реальные транзакции
    mock_data = pd.DataFrame(
        {
            "id": [650703, 3598919],
            "state": ["EXECUTED", "CANCELED"],
            "date": ["2023-09-05T11:30:32Z", "2020-12-06T23:00:58Z"],
            "amount": [16210, 29740],
            "currency_name": ["Sol", "Peso"],
            "currency_code": ["PEN", "COP"],
            "from": ["Счет 58803664561298323391", None],
            "to": ["Счет 39745660563456619397", "Discover 0720428384694643"],
            "description": ["Перевод организации", "Перевод с карты на карту"],
        }
    )

    # Мокируем проверку существования файла и чтение CSV
    with patch("os.path.exists") as mock_exists, patch("pandas.read_csv") as mock_read_csv:
        # Настраиваем моки
        mock_exists.return_value = True  # Файл существует
        mock_read_csv.return_value = mock_data  # Возвращаем тестовые данные

        # Вызываем тестируемую функцию
        result = read_transactions_from_csv("test.csv")

        # Проверяем результаты
        assert len(result) == 2
        assert result[0]["id"] == 650703
        assert result[0]["state"] == "EXECUTED"
        assert result[1]["state"] == "CANCELED"
        assert result[1]["from"] is None  # Проверяем обработку None


def test_empty_file() -> None:
    """Тест на пустой CSV-файл"""
    with patch("os.path.exists") as mock_exists, patch("pandas.read_csv") as mock_read_csv:
        mock_exists.return_value = True
        mock_read_csv.return_value = pd.DataFrame()  # Пустой DataFrame

        # Вызываем функцию с пустым файлом
        result = read_transactions_from_csv("empty.csv")
        # Должен вернуться пустой список
        assert result == []


def test_nan_values_replaced() -> None:
    """Тест замены NaN значений на None. Проверяет, что функция корректно обрабатывает
    различные типы пустых значений (NaN, None) и заменяет их на None"""

    # Создаем DataFrame с NaN значениями
    mock_data = pd.DataFrame(
        {"id": [1, 2], "state": ["EXECUTED", None], "amount": [100, float("nan")]}  # Явный None  # NaN значение
    )

    with patch("os.path.exists") as mock_exists, patch("pandas.read_csv") as mock_read_csv:
        mock_exists.return_value = True
        mock_read_csv.return_value = mock_data

        # Получаем результат обработки
        result = read_transactions_from_csv("test.csv")

        # Проверяем, что NaN заменен на None
        assert result[1]["amount"] is None, "NaN значения должны быть заменены на None"
        assert result[1]["state"] is None, "Существующие None должны сохраниться"


def test_csv_reading_parameters() -> None:
    """Тест корректности параметров чтения CSV."""
    with patch("os.path.exists") as mock_exists, patch("pandas.read_csv") as mock_read_csv:
        mock_exists.return_value = True
        mock_read_csv.return_value = pd.DataFrame({"id": [1]})

        # Вызываем тестируемую функцию
        read_transactions_from_csv("test.csv")

        # Проверяем, что read_csv вызван с правильными параметрами
        mock_read_csv.assert_called_once_with("test.csv", sep=";")
