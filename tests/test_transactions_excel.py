import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from typing import List, Dict, Any
from src.transactions_excel import read_transactions_from_excel


def test_file_not_found() -> None:
    """Тестирует случай, когда файл Excel не существует.Проверяет, что функция корректно
    выбрасывает FileNotFoundError при попытке чтения несуществующего файла."""

    # Мокируем os.path.exists чтобы возвращать False (файл не существует)
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = False

        # Проверяем, что функция выбрасывает FileNotFoundError
        with pytest.raises(FileNotFoundError):
            read_transactions_from_excel("nonexistent.xlsx")


def test_successful_read() -> None:
    """Тестирует успешное чтение и обработку данных из Excel файла."""

    # Создаем тестовые данные, имитирующие реальные транзакции
    mock_data = pd.DataFrame(
        {
            "id": [650703, 3598919],
            "state": ["EXECUTED", "CANCELED"],
            "date": ["2023-09-05T11:30:32Z", "2020-12-06T23:00:58Z"],
            "amount": [16210, 29740],
            "currency_name": ["Sol", "Peso"],
            "currency_code": ["PEN", "COP"],
            "from": ["Счет 58803664561298323391", None],  # Вторая транзакция без отправителя
            "to": ["Счет 39745660563456619397", "Discover 0720428384694643"],
            "description": ["Перевод организации", "Перевод с карты на карту"],
        }
    )

    # Мокируем проверку существования файла и чтение Excel
    with patch("os.path.exists") as mock_exists, patch("pandas.read_excel") as mock_read_excel:
        # Настраиваем моки
        mock_exists.return_value = True  # Файл существует
        mock_read_excel.return_value = mock_data  # Возвращаем тестовые данные

        # Вызываем тестируемую функцию
        result: List[Dict[str, Any]] = read_transactions_from_excel("test.xlsx")

        # Проверяем результаты
        assert len(result) == 2, "Должно быть 2 транзакции"
        assert result[0]["id"] == 650703, "ID первой транзакции должен быть 650703"
        assert result[0]["state"] == "EXECUTED", "Статус первой транзакции должен быть EXECUTED"
        assert result[1]["from"] is None, "Поле 'from' второй транзакции должно быть None"


def test_empty_file() -> None:
    """Тестирует обработку пустого Excel файла.Проверяет, что функция возвращает пустой список
    при чтении файла без данных."""

    with patch("os.path.exists") as mock_exists, patch("pandas.read_excel") as mock_read_excel:
        mock_exists.return_value = True
        mock_read_excel.return_value = pd.DataFrame()  # Пустой DataFrame

        # Вызываем функцию с пустым файлом
        result: List[Dict[str, Any]] = read_transactions_from_excel("empty.xlsx")

        # Должен вернуться пустой список
        assert result == []


def test_excel_reading_parameters() -> None:
    """Тестирует корректность параметров при чтении Excel файла.Проверяет, что функция read_excel
    вызывается с правильными параметрами (путь к файлу и движок openpyxl)."""
    with patch("os.path.exists") as mock_exists, patch("pandas.read_excel") as mock_read_excel:
        mock_exists.return_value = True
        mock_read_excel.return_value = pd.DataFrame({"id": [1]})

        # Вызываем тестируемую функцию
        read_transactions_from_excel("test.xlsx")

        # Проверяем, что read_excel был вызван с правильными параметрами
        mock_read_excel.assert_called_once_with("test.xlsx", engine="openpyxl")


def test_complete_data_structure() -> None:
    """Тестирует полную структуру данных с реальными примерами транзакций.Проверяет корректность
    обработки всех полей транзакции и сохранение полной структуры данных."""

    # Полный пример данных, соответствующий реальной структуре
    mock_data = pd.DataFrame(
        {
            "id": [650703, 5380041],
            "state": ["EXECUTED", "CANCELED"],
            "date": ["2023-09-05T11:30:32Z", "2021-02-01T11:54:58Z"],
            "amount": [16210, 23789],
            "currency_name": ["Sol", "Peso"],
            "currency_code": ["PEN", "UYU"],
            "from": ["Счет 58803664561298323391", None],  # Вторая транзакция - открытие вклада
            "to": ["Счет 39745660563456619397", "Счет 23294994494356835683"],
            "description": ["Перевод организации", "Открытие вклада"],
        }
    )

    with patch("os.path.exists") as mock_exists, patch("pandas.read_excel") as mock_read_excel:
        mock_exists.return_value = True
        mock_read_excel.return_value = mock_data

        result: List[Dict[str, Any]] = read_transactions_from_excel("test.xlsx")

        # Проверяем полную структуру первой транзакции
        first_transaction = result[0]
        assert first_transaction["id"] == 650703
        assert first_transaction["state"] == "EXECUTED"
        assert first_transaction["date"] == "2023-09-05T11:30:32Z"
        assert first_transaction["amount"] == 16210
        assert first_transaction["currency_name"] == "Sol"
        assert first_transaction["currency_code"] == "PEN"
        assert first_transaction["from"] == "Счет 58803664561298323391"
        assert first_transaction["to"] == "Счет 39745660563456619397"
        assert first_transaction["description"] == "Перевод организации"

        # Проверяем, что поле 'from' может быть None (для операций открытия вклада)
        assert result[1]["from"] is None


def test_pandas_replace_called() -> None:
    """Тестирует вызов метода replace для обработки пустых значений. Проверяет, что функция
    замены pd.NA на None действительно вызывается в процессе обработки данных."""

    # Создаем мок DataFrame с методом replace
    mock_df = MagicMock()
    # Настраиваем цепочку вызовов: read_excel возвращает mock_df,
    # mock_df.replace возвращает тот же mock_df (или новый DataFrame)
    processed_df = MagicMock()
    processed_df.to_dict.return_value = [{"id": 1}]
    mock_df.replace.return_value = processed_df

    with patch("os.path.exists") as mock_exists, patch("pandas.read_excel") as mock_read_excel:
        mock_exists.return_value = True
        mock_read_excel.return_value = mock_df

        # Вызываем тестируемую функцию (ВНУТРИ блока with!)
        read_transactions_from_excel("test.xlsx")

        # Проверяем, что replace был вызван с правильными параметрами
        mock_df.replace.assert_called_once_with({pd.NA: None})
