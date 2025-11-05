import json
from unittest.mock import patch, mock_open, Mock
from src.utils import load_transactions


@patch("src.utils.os.path.exists")
@patch("src.utils.os.path.isfile")
@patch("src.utils.os.path.getsize")
def test_load_transactions_success(mock_getsize: Mock, mock_isfile: Mock, mock_exists: Mock) -> None:
    """Тестирование успешной загрузки транзакций из JSON-файла."""
    # Настройка моков
    mock_exists.return_value = True
    mock_isfile.return_value = True
    mock_getsize.return_value = 100

    # Мокируем данные файла
    mock_data = [{"id": 1, "amount": 100, "currency": "USD"}, {"id": 2, "amount": 200, "currency": "EUR"}]

    with patch("src.utils.open", mock_open(read_data=json.dumps(mock_data))):
        with patch("src.utils.json.load") as mock_json_load:
            mock_json_load.return_value = mock_data

            # Вызов тестируемой функции
            result = load_transactions("data/operations.json")

    # Проверки
    assert result == mock_data
    mock_exists.assert_called_once()
    mock_isfile.assert_called_once()
    mock_getsize.assert_called_once()


@patch("src.utils.os.path.exists")
def test_load_transactions_file_not_found(mock_exists: Mock) -> None:
    """Тестирование случая, когда файл не существует."""
    mock_exists.return_value = False

    result = load_transactions("data/operations.json")

    assert result == []
    mock_exists.assert_called_once()


@patch("src.utils.os.path.exists")
@patch("src.utils.os.path.isfile")
def test_load_transactions_path_is_directory(mock_isfile: Mock, mock_exists: Mock) -> None:
    """Тестирование случая, когда путь ведет к директории, а не к файлу."""
    mock_exists.return_value = True
    mock_isfile.return_value = False

    result = load_transactions("data/operations.json")

    assert result == []
    mock_exists.assert_called_once()
    mock_isfile.assert_called_once()


@patch("src.utils.os.path.exists")
@patch("src.utils.os.path.isfile")
@patch("src.utils.os.path.getsize")
def test_load_transactions_empty_file(mock_getsize: Mock, mock_isfile: Mock, mock_exists: Mock) -> None:
    """Тестирование случая с пустым файлом."""
    mock_exists.return_value = True
    mock_isfile.return_value = True
    mock_getsize.return_value = 0

    result = load_transactions("data/operations.json")

    assert result == []
    mock_exists.assert_called_once()
    mock_isfile.assert_called_once()
    mock_getsize.assert_called_once()
