import os
from typing import List, Dict, Any

from src.utils import load_transactions
from src.transactions_csv import read_transactions_from_csv
from src.transactions_excel import read_transactions_from_excel
from src.processing import filter_by_state, sort_by_date
from src.transaction_processor import process_bank_search
from src.widget import mask_account_card, get_date
from src.masks import get_mask_card_number, get_mask_account
from src.generators import filter_by_currency as filter_by_currency_gen, transaction_descriptions


def convert_currency_generator_to_list(transactions: List[Dict[str, Any]], currency: str) -> List[Dict[str, Any]]:
    """Конвертирует результат генератора filter_by_currency в список."""
    # Используем существующий генератор из generators.py
    currency_iterator = filter_by_currency_gen(transactions, currency)
    return list(currency_iterator)


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str = "RUB") -> List[Dict[str, Any]]:
    """Фильтрует транзакции по валюте (обертка над генератором)."""
    if not transactions:
        return []

    # Приводим код валюты к нужному формату (RUB, USD, EUR и т.д.)
    currency_upper = currency_code.upper()

    # Пробуем разные варианты кода валюты
    currency_variants = []
    if currency_upper == "RUB":
        currency_variants = ["RUB", "руб.", "RUR", "RUB"]
    elif currency_upper == "USD":
        currency_variants = ["USD", "доллар", "долларов"]
    elif currency_upper == "EUR":
        currency_variants = ["EUR", "евро"]
    else:
        currency_variants = [currency_upper]

    # Пробуем каждую вариацию валюты
    for currency_var in currency_variants:
        try:
            result = convert_currency_generator_to_list(transactions, currency_var)
            if result:
                return result
        except Exception:
            continue

    return []


def filter_by_description_keyword(transactions: List[Dict[str, Any]], keyword: str) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по ключевому слову в описании."""
    if not transactions or not keyword:
        return transactions

    # Используем существующую функцию process_bank_search из transaction_processor.py
    return process_bank_search(transactions, keyword)


def format_transaction(transaction: Dict[str, Any]) -> str:
    """Форматирует транзакцию для вывода в консоль."""
    result = []

    # Форматируем дату
    if "date" in transaction and transaction["date"]:
        try:
            # Используем функцию get_date из widget.py
            date_formatted = get_date(str(transaction["date"]))
            result.append(f"{date_formatted} ")
        except Exception:
            # Если не удалось преобразовать дату, используем оригинальную строку
            result.append(f"{transaction['date']} ")

    # Добавляем описание
    if "description" in transaction and transaction["description"]:
        result.append(f"{transaction['description']}\n")

    # Форматируем отправителя и получателя
    from_account = transaction.get("from", "")
    to_account = transaction.get("to", "")

    if from_account and to_account:
        # Маскируем оба счета/карты с помощью функции mask_account_card из widget.py
        masked_from = mask_account_card(str(from_account))
        masked_to = mask_account_card(str(to_account))
        result.append(f"{masked_from} -> {masked_to}\n")
    elif to_account:
        # Только получатель
        masked_to = mask_account_card(str(to_account))
        result.append(f"{masked_to}\n")

    # Форматируем сумму
    if "operationAmount" in transaction and isinstance(transaction["operationAmount"], dict):
        amount_info = transaction["operationAmount"]
        amount = amount_info.get("amount", "")
        currency_info = amount_info.get("currency", {})

        if isinstance(currency_info, dict):
            currency_name = currency_info.get("name", "")
            currency_code = currency_info.get("code", "")

            # Используем название валюты или код, если название отсутствует
            currency_display = currency_name if currency_name else currency_code
            result.append(f"Сумма: {amount} {currency_display if currency_display else 'руб.'}\n")
        else:
            result.append(f"Сумма: {amount} руб.\n")
    elif "amount" in transaction:
        amount = transaction.get("amount", "")
        currency = transaction.get("currency", "руб.")
        result.append(f"Сумма: {amount} {currency}\n")

    result.append("\n")  # Пустая строка между транзакциями
    return "".join(result)


def get_user_yes_no(prompt: str) -> bool:
    """Запрашивает у пользователя ответ Да/Нет и возвращает True/False."""
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in ["да", "д", "yes", "y"]:
            return True
        elif user_input in ["нет", "н", "no", "n"]:
            return False
        else:
            print('Пожалуйста, ответьте "Да" или "Нет"')


def get_valid_status() -> str:
    """Запрашивает у пользователя статус транзакции до тех пор, пока не будет введен корректный статус."""
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

        user_input = input("Ваш выбор: ").strip().upper()

        if user_input in valid_statuses:
            return user_input
        else:
            print(f'Статус операции "{user_input}" недоступен.\n')


def get_transaction_descriptions(transactions: List[Dict[str, Any]]) -> List[str]:
    """Получает список всех описаний транзакций с помощью генератора transaction_descriptions."""
    # Используем генератор из generators.py
    descriptions_iterator = transaction_descriptions(transactions)
    return list(descriptions_iterator)


def generate_card_numbers(start: int, stop: int) -> List[str]:
    """Генерирует список номеров карт для демонстрации (опционально)."""
    from src.generators import card_number_generator

    result = []
    for card_number in card_number_generator(start, stop):
        result.append(card_number)

    return result


def main() -> None:
    """Основная функция программы для работы с банковскими транзакциями."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    file_choice = input("\nВаш выбор: ").strip()

    file_path = ""
    transactions = []

    # Загрузка данных в зависимости от выбора пользователя
    if file_choice == "1":
        # Используем существующий файл
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(current_dir, "data", "operations.json")
        print("Для обработки выбран JSON-файл.")
        transactions = load_transactions(file_path)

    elif file_choice == "2":
        # Используем существующий файл
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(current_dir, "data", "transactions.csv")
        print("Для обработки выбран CSV-файл.")
        transactions = read_transactions_from_csv(file_path)

    elif file_choice == "3":
        # Используем существующий файл
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(current_dir, "data", "transactions_excel.xlsx")
        print("Для обработки выбран XLSX-файл.")
        transactions = read_transactions_from_excel(file_path)

    else:
        print("Неверный выбор. Программа завершена.")
        return

    # Проверяем, загрузились ли транзакции
    if not transactions:
        print("Не удалось загрузить транзакции или файл пуст.")
        return

    print(f"Загружено {len(transactions)} транзакций.\n")

    # Демонстрация генератора описаний (опционально)
    if get_user_yes_no("Показать все описания транзакций? Да/Нет: "):
        descriptions = get_transaction_descriptions(transactions)
        print("\nВсе описания транзакций:")
        for i, desc in enumerate(descriptions, 1):
            print(f"{i}. {desc}")
        print()

    # Фильтрация по статусу
    status = get_valid_status()
    print(f'Операции отфильтрованы по статусу "{status}"\n')

    # Используем существующую функцию filter_by_state из processing.py
    filtered_transactions = filter_by_state(transactions, status)

    if not filtered_transactions:
        print("Не найдено ни одной транзакции с выбранным статусом.")
        return

    print(f"Найдено {len(filtered_transactions)} транзакций с статусом {status}.\n")

    # Сортировка по дате
    if get_user_yes_no("Отсортировать операции по дате? Да/Нет: "):
        sort_order = (
            input("Отсортировать по возрастанию или по убыванию? (по возрастанию/по убыванию): ").strip().lower()
        )

        reverse_sort = False
        if sort_order in ["по убыванию", "убыванию", "desc", "обратный"]:
            reverse_sort = True
            print("Сортировка по убыванию даты.")
        else:
            print("Сортировка по возрастанию даты.")

        # Используем существующую функцию sort_by_date из processing.py
        filtered_transactions = sort_by_date(filtered_transactions, reverse_sort)

    # Фильтрация по валюте (только рублевые транзакции)
    if get_user_yes_no("Выводить только рублевые транзакции? Да/Нет: "):
        filtered_transactions = filter_by_currency(filtered_transactions, "RUB")
        print("Отфильтровано по рублевым транзакциям.")

    # Фильтрация по ключевому слову в описании
    if get_user_yes_no("Отфильтровать список транзакций по определенному слову в описании? Да/Нет: "):
        keyword = input("Введите слово для поиска в описании: ").strip()
        if keyword:
            # Используем существующую функцию process_bank_search из transaction_processor.py
            filtered_transactions = filter_by_description_keyword(filtered_transactions, keyword)
            print(f'Отфильтровано по ключевому слову "{keyword}".')

    # Демонстрация генератора номеров карт (опционально)
    if get_user_yes_no("Сгенерировать примеры номеров банковских карт? Да/Нет: "):
        try:
            card_numbers = generate_card_numbers(1, 5)
            print("\nПримеры номеров карт:")
            for card in card_numbers:
                print(card)
            print()
        except Exception as e:
            print(f"Не удалось сгенерировать номера карт: {e}")

    # Вывод результатов
    print("\nРаспечатываю итоговый список транзакций...\n")
    print(f"Всего банковских операций в выборке: {len(filtered_transactions)}\n")

    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    # Ограничиваем вывод 10 транзакциями
    display_limit = min(10, len(filtered_transactions))
    for i in range(display_limit):
        transaction = filtered_transactions[i]
        print(format_transaction(transaction))

    if len(filtered_transactions) > 10:
        print(f"... и еще {len(filtered_transactions) - 10} транзакций.")

    # Демонстрация работы масок (опционально)
    if get_user_yes_no("\nПоказать работу функций маскирования отдельно? Да/Нет: "):
        print("\nПримеры работы масок:")

    # Примеры для функции get_mask_card_number
    test_cards = ["7000792289606361", "1234567812345678", "5555555555554444"]
    print("Маскировка номеров карт (первые 6 и последние 4 цифры):")
    for card in test_cards:
        masked = get_mask_card_number(card)
        print(f"  {card} -> {masked}")

    # Примеры для функции get_mask_account
    test_accounts = ["73654108430135874305", "12345678901234567890"]
    print("\nМаскировка номеров счетов (последние 4 цифры):")
    for account in test_accounts:
        masked = get_mask_account(account)
        print(f"  {account} -> {masked}")

    # Примеры для функции mask_account_card
    test_info = ["Visa Platinum 7000792289606361", "Счет 73654108430135874305", "MasterCard 1234567812345678"]
    print("\nМаскировка через mask_account_card (универсальная):")
    for info in test_info:
        masked = mask_account_card(info)
        print(f"  {info} -> {masked}")


if __name__ == "__main__":
    main()
