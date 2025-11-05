import pytest
from unittest.mock import patch
from typing import Dict, Any
from src.transactions import get_transaction_amount_in_rub


def test_rub_transaction() -> None:
    """Тестирует обработку транзакции в рублях без конвертации."""
    transaction: Dict[str, Any] = {"amount": 1000.0, "currency": "RUB"}
    result: float = get_transaction_amount_in_rub(transaction)
    assert result == 1000.0


def test_usd_transaction() -> None:
    """Тестирует конвертацию USD в RUB с использованием mock."""
    transaction = {"amount": 100.0, "currency": "USD"}

    with patch("src.transactions.convert_currency") as mock_convert:
        mock_convert.return_value = 7500.0
        result = get_transaction_amount_in_rub(transaction)

        mock_convert.assert_called_once_with(100.0, "USD", "RUB")
        assert result == 7500.0


def test_eur_transaction() -> None:
    """Тестирует конвертацию EUR в RUB с использованием mock."""
    transaction = {"amount": 50.0, "currency": "EUR"}

    with patch("src.transactions.convert_currency") as mock_convert:
        mock_convert.return_value = 4500.0
        result = get_transaction_amount_in_rub(transaction)

        mock_convert.assert_called_once_with(50.0, "EUR", "RUB")
        assert result == 4500.0


def test_missing_amount_field() -> None:
    """Тестирует обработку транзакции с отсутствующим полем amount."""
    transaction = {"currency": "USD"}

    with pytest.raises(ValueError, match="Transaction must contain 'amount' and 'currency' fields"):
        get_transaction_amount_in_rub(transaction)


def test_missing_currency_field() -> None:
    """Тестирует обработку транзакции с отсутствующим полем currency."""
    transaction = {"amount": 100.0}

    with pytest.raises(ValueError, match="Transaction must contain 'amount' and 'currency' fields"):
        get_transaction_amount_in_rub(transaction)


def test_unsupported_currency() -> None:
    """Тестирует обработку неподдерживаемой валюты."""
    transaction = {"amount": 100.0, "currency": "GBP"}

    with pytest.raises(ValueError, match="Unsupported currency: GBP. Only RUB, USD, EUR are supported"):
        get_transaction_amount_in_rub(transaction)


def test_usd_conversion_failure() -> None:
    """Тестирует обработку ошибки конвертации USD в RUB."""
    transaction = {"amount": 100.0, "currency": "USD"}

    with patch("src.transactions.convert_currency") as mock_convert:
        mock_convert.side_effect = Exception("API error")

        with pytest.raises(Exception, match="USD to RUB conversion failed."):
            get_transaction_amount_in_rub(transaction)


def test_eur_conversion_failure() -> None:
    """Тестирует обработку ошибки конвертации EUR в RUB."""
    transaction = {"amount": 100.0, "currency": "EUR"}

    with patch("src.transactions.convert_currency") as mock_convert:
        mock_convert.side_effect = Exception("API error")

        with pytest.raises(Exception, match="EUR to RUB conversion failed."):
            get_transaction_amount_in_rub(transaction)


def test_currency_case_insensitive() -> None:
    """Тестирует обработку валюты в нижнем регистре."""
    transaction = {"amount": 100.0, "currency": "usd"}

    with patch("src.transactions.convert_currency") as mock_convert:
        mock_convert.return_value = 7500.0
        result = get_transaction_amount_in_rub(transaction)

        assert result == 7500.0


def test_currency_with_whitespace() -> None:
    """Тестирует обработку валюты с пробелами."""
    transaction = {"amount": 100.0, "currency": "  USD  "}

    with patch("src.transactions.convert_currency") as mock_convert:
        mock_convert.return_value = 7500.0
        result: float = get_transaction_amount_in_rub(transaction)

        mock_convert.assert_called_once_with(100.0, "USD", "RUB")
        assert result == 7500.0


def test_zero_amount() -> None:
    """Тестирует обработку нулевой суммы транзакции."""
    transaction = {"amount": 0.0, "currency": "USD"}

    with patch("src.transactions.convert_currency") as mock_convert:
        mock_convert.return_value = 0.0
        result = get_transaction_amount_in_rub(transaction)

        mock_convert.assert_called_once_with(0.0, "USD", "RUB")
        assert result == 0.0
