import requests
import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Dict, Any, Union

# Загрузка переменных из .env-файла
BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")

# Получение API-ключа из переменных окружения
API_KEY = os.getenv("API_KEY")
URL = "https://api.apilayer.com/exchangerates_data/convert"


def convert_currency_api(amount: float, from_currency: str, to_currency: str = "RUB") -> float:
    """Вспомогательная функция для конвертации валют через API."""

    # Проверяем наличие API-ключа
    if not API_KEY:
        raise Exception("API_KEY not found. Check your .env file.")

    # Создаем заголовки запроса с API-ключом
    headers: Dict[str, str] = {"apikey": API_KEY}

    # Параметры запроса для конвертации
    params: Dict[str, Union[str, float]] = {"from": from_currency, "to": to_currency, "amount": amount}

    try:
        # Выполнение GET запроса к API
        response = requests.get(URL, headers=headers, params=params)

        # Проверка статуса ответа
        response.raise_for_status()

        # Получение данных из ответа API в формате JSON
        data: Dict[str, Any] = response.json()

        # Проверка успешности запроса по полю success
        if data.get("success", False):
            converted_amount = float(data["result"])
            return converted_amount
        else:
            # Обработка ошибки API
            error_info = data.get("error", {}).get("info", "Unknown error")
            raise Exception(f"API error: {error_info}")

    except requests.exceptions.RequestException as e:
        # Обработка сетевых ошибок
        raise Exception(f"Request to exchange rate API failed: {e}")
    except (KeyError, ValueError) as e:
        # Обработка ошибок получения ответа
        raise Exception(f"Invalid API response format: {e}")


def convert_currency(transaction: Dict[str, Any]) -> float:
    """Конвертирует сумму транзакции в рубли."""

    # Проверяем наличие необходимых полей в транзакции
    if "operationAmount" not in transaction:
        raise ValueError("Transaction missing 'operationAmount' field")

    operation_amount = transaction["operationAmount"]

    if "amount" not in operation_amount or "currency" not in operation_amount:
        raise ValueError("Transaction missing 'amount' or 'currency' field")

    currency_info = operation_amount["currency"]
    if "code" not in currency_info:
        raise ValueError("Currency information missing 'code' field")

    # Извлекаем сумму и валюту
    amount_str = operation_amount["amount"]
    currency_code = currency_info["code"]

    try:
        amount = float(amount_str)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid amount format: {amount_str}")

    # Обработка транзакции в рублях (без конвертации)
    if currency_code == "RUB":
        return amount

    # Обработка транзакции в USD и EUR (конвертация через API)
    if currency_code in ["USD", "EUR"]:
        return convert_currency_api(amount, currency_code, "RUB")

    return amount


# Пример использования
if __name__ == "__main__":
    # Пример транзакции в USD
    sample_transaction_usd = {
        "id": 41428829,
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
        "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "MasterCard 7158300734726758",
        "to": "Счет 35383033474447895560",
    }

    # Пример транзакции в RUB
    sample_transaction_rub = {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589",
    }

    try:
        # Конвертируем USD транзакцию
        amount_in_rub = convert_currency(sample_transaction_usd)
        print(f"USD transaction converted to RUB: {amount_in_rub:.2f}")

        # RUB транзакция (без конвертации)
        amount_in_rub = convert_currency(sample_transaction_rub)
        print(f"RUB transaction amount: {amount_in_rub:.2f}")

    except Exception as e:
        print(f"Error: {e}")
