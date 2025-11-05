from typing import Dict, Any
from src.external_api import convert_currency  # type:ignore


def get_transaction_amount_in_rub(transaction: Dict[str, Any]) -> float:
    """Функция, которая принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях."""

    # Проверка обязательных полей в транзакции
    if "amount" not in transaction or "currency" not in transaction:
        raise ValueError("Transaction must contain 'amount' and 'currency' fields")

    # Извлечение данных из транзакции
    amount = float(transaction["amount"])
    currency = transaction["currency"].upper().strip()

    # Обработка транзакции в рублях (без конвертации)
    if currency == "RUB":
        return amount

    # Обработка транзакции в USD (конвертация через API)
    elif currency == "USD":
        try:
            converted_amount: float = convert_currency(amount, "USD", "RUB")
            return converted_amount
        except Exception as e:
            raise Exception(f"USD to RUB conversion failed: {e}")

    # Обработка транзакции в EUR (конвертация через API)
    elif currency == "EUR":
        try:
            converted_amount = convert_currency(amount, "EUR", "RUB")
            return converted_amount
        except Exception as e:
            raise Exception(f"EUR to RUB conversion failed: {e}")

    # Обработка неподдерживаемых валют
    else:
        raise ValueError(f"Unsupported currency: {currency}. Only RUB, USD, EUR are supported")


# Примеры использования
if __name__ == "__main__":
    transactions = [
        {"amount": 2000.0, "currency": "RUB"},
        {"amount": 300.0, "currency": "USD"},
        {"amount": 200.0, "currency": "EUR"},
    ]

    for transaction in transactions:
        try:
            rub_amount = get_transaction_amount_in_rub(transaction)
            print(f"{transaction['amount']} {transaction['currency']} = {rub_amount:.2f} RUB")
        except Exception as e:
            print(f"Error: {e}")
