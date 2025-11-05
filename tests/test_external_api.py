from unittest.mock import patch, Mock
import requests
import pytest

# Импортируем тестируемую функцию
from src.external_api import convert_currency, URL


@patch('src.external_api.API_KEY', 'test-api-key')
@patch('src.external_api.requests.get')
def test_success_conversion(mock_get: Mock) -> None:
    """Тест успешной конвертации валюты."""
    # Настройка мок-ответа
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True, "result": 7500.50}
    mock_get.return_value = mock_response

    # Вызов тестируемой функции
    result = convert_currency(100, 'USD', 'RUB')

    # Проверки
    assert result == 7500.50
    # Проверяем что функция вызвана ровно один раз
    assert mock_get.call_count == 1
    # Проверяем что функция вызвана с правильными аргументами
    mock_get.assert_called_once_with(
        URL,
        headers={"apikey": 'test-api-key'},
        params={"from": "USD", "to": "RUB", "amount": 100}
    )


@patch('src.external_api.API_KEY', 'test-api-key')
@patch('src.external_api.requests.get')
def test_api_error(mock_get: Mock) -> None:
    """Тест обработки ошибки от API."""
    # Настройка мок-ответа с ошибкой
    mock_response = Mock()
    mock_response.json.return_value = {
        "success": False,
        "error": {"info": "Invalid currency"}
    }
    mock_get.return_value = mock_response

    # Проверяем что исключение выбрасывается
    with pytest.raises(Exception, match="API error: Invalid currency"):
        convert_currency(100, 'INVALID', 'RUB')

    # Проверяем что функция вызвана ровно один раз с правильными аргументами
    # ИСПРАВЛЕНИЕ: используем 'INVALID' вместо 'USD'
    assert mock_get.call_count == 1
    mock_get.assert_called_once_with(
        URL,
        headers={"apikey": 'test-api-key'},
        params={"from": "INVALID", "to": "RUB", "amount": 100}
    )


@patch('src.external_api.API_KEY', 'test-api-key')
@patch('src.external_api.requests.get')
def test_network_error(mock_get: Mock) -> None:
    """Тест обработки сетевой ошибки."""
    # Настройка мока для генерации сетевой ошибки
    mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

    # Проверяем что исключение выбрасывается
    with pytest.raises(Exception, match="Request to exchange rate API failed"):
        convert_currency(100, 'USD', 'RUB')

    # Проверяем что функция вызвана ровно один раз с правильными аргументами
    assert mock_get.call_count == 1
    mock_get.assert_called_once_with(
        URL,
        headers={"apikey": 'test-api-key'},
        params={"from": "USD", "to": "RUB", "amount": 100}
    )


@patch('src.external_api.API_KEY', None)
def test_no_api_key() -> None:
    """Тест отсутствия API ключа."""
    # Проверяем что исключение выбрасывается
    with pytest.raises(Exception, match="API_KEY not found"):
        convert_currency(100, 'USD', 'RUB')


@patch('src.external_api.API_KEY', 'test-api-key')
@patch('src.external_api.requests.get')
def test_default_currency(mock_get: Mock) -> None:
    """Тест конвертации в валюту по умолчанию (RUB)."""
    # Настройка мок-ответа
    mock_response = Mock()
    mock_response.json.return_value = {"success": True, "result": 5000.0}
    mock_get.return_value = mock_response

    # Вызываем функцию без указания целевой валюты (должен использоваться RUB по умолчанию)
    result = convert_currency(50, 'EUR')

    # Проверки
    assert result == 5000.0
    # Проверяем что функция вызвана ровно один раз
    assert mock_get.call_count == 1
    # Проверяем что в параметрах указана валюта по умолчанию (RUB)
    # ИСПРАВЛЕНИЕ: используем 'EUR' вместо 'USD'
    mock_get.assert_called_once_with(
        URL,
        headers={"apikey": 'test-api-key'},
        params={"from": "EUR", "to": "RUB", "amount": 50}
    )


# Дополнительный тест для проверки вызова с явным указанием валюты
@patch('src.external_api.API_KEY', 'test-api-key')
@patch('src.external_api.requests.get')
def test_explicit_currencies(mock_get: Mock) -> None:
    """Тест конвертации с явным указанием обеих валют."""
    # Настройка мок-ответа
    mock_response = Mock()
    mock_response.json.return_value = {"success": True, "result": 0.92}
    mock_get.return_value = mock_response

    # Вызываем функцию с явным указанием обеих валют
    result = convert_currency(1, 'USD', 'EUR')

    # Проверки
    assert result == 0.92
    # Проверяем что функция вызвана ровно один раз
    assert mock_get.call_count == 1
    # Проверяем что в параметрах указаны правильные валюты
    mock_get.assert_called_once_with(
        URL,
        headers={"apikey": 'test-api-key'},
        params={"from": "USD", "to": "EUR", "amount": 1}
    )
