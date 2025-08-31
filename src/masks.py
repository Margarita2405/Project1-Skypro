def get_mask_card_number(card_number: str) -> str:
    """Функция, которая маскирует номер банковской карты, оставляя видимыми первые 6 и последние 4 цифры"""

    # Разбиваем номер карты на части
    first_part = card_number[:4]  # Первые 4 цифры номера карты
    second_part = card_number[4:6]  # Следующие 2 цифры номера карты
    last_part = card_number[-4:]  # Последние 4 цифры номера карты

    # Создаем замаскированную строку
    masked_number = f"{first_part} {second_part} ** **** {last_part}"
    return masked_number


if __name__ == "__main__":
    # Тестирование функции
    print(get_mask_card_number("5946823031801656"))


def get_mask_account(account_number: str) -> str:
    """Функция, которая маскирует номер банковского счета, оставляя видимыми последние 4 цифры"""

    # Получаем последние 4 цифры номера счета
    last_four_digits = account_number[-4:]

    # Создаем замаскированную строку
    masked_account = f"** {last_four_digits}"
    return masked_account


if __name__ == "__main__":
    # Тестирование функции
    print(get_mask_account("40817810207005367456"))
