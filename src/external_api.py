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

# Проверяем, загрузился ли API-ключ
print(f"API_KEY loaded: {API_KEY is not None}")


def convert_currency(amount: float, from_currency: str, to_currency: str = "RUB") -> float:
    """Конвертирует сумму из одной валюты в другую используя Exchange Rates Data API."""

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

        # Дополнительная диагностика
        print(f"Response status: {response.status_code}")

        # Проверка статуса ответа
        response.raise_for_status()

        # Получение данных из ответа API в формате JSON
        data: Dict[str, Any] = response.json()

        # Диагностика ответа
        print(f"API Response: {data}")

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
