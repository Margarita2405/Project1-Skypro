from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info_string: str) -> str:
    """Функция, которая принимает строку, содержащую тип и номер банковской карты/счета,
    и возвращает строку с замаскированным номером"""

    # Разделяем строку на части (тип и номер) по последнему пробелу
    parts = info_string.rsplit(" ", 1)

    type_card, number = parts
    type_card = type_card.strip()
    number = number.strip()

    if len(parts) != 2:
        raise ValueError("Некорректный формат строки")

    # Проверяем, что номер состоит только из цифр
    if not number.isdigit():
        raise ValueError("Некорректный ввод, номер должен состоять только из цифр")

    # Проверяем, является ли это счетом
    if type_card.lower() == "счет":
        if len(number) < 20:
            raise ValueError("Некорректный ввод, номер счета слишком короткий")

        # Создаем замаскированную строку для счета
        masked_account = get_mask_account(number)
        return f"{type_card} {masked_account}"
    else:
        # Маскировка для карты
        if len(number) < 16:
            raise ValueError("Некорректный ввод, номер карты слишком короткий")

        # Создаем замаскированную строку для карты
        masked_card = get_mask_card_number(number)
        return f"{type_card} {masked_card}"


# Тестирование функции
if __name__ == "__main__":
    test_examples = [
        "Visa Platinum 7000792289606361",
        "Счет 73654108430135874305",
        "Maestro 1596837868705199",
        "Счет 64686473678894779589",
        "MasterCard 7158300734726758",
        "Счет 35383033474447895560",
        "Visa Classic 6831982476737658",
        "Visa Platinum 8990922113665229",
        "Visa Gold 5999414228426353",
    ]

    print("Результаты работы функции mask_account_card :")

    for test_example in test_examples:
        result = mask_account_card(test_example)
        print(f"Вход: {test_example}")
        print(f"Выход: {result}")


def get_date(date_string: str) -> str:
    """Функция, которая преобразует строку с датой в международном формате  в строку
     с датой в российском формате "ДД.ММ.ГГГГ"""

    # Разделяем строку по символу 'Т', чтобы отделить дату от времени
    date_part = date_string.split("T")[0]

    # Разделяем дату на элементы
    year, month, day = date_part.split("-")

    # Возвращаем строку в нужном формате
    return f"{day}.{month}.{year}"


# Тестирование функции
if __name__ == "__main__":
    test_examples = ["2024-03-11T02:26:18.671407", "2025-07-23T10:45:34.256130"]
    print("Результаты работы функции get_date:")

    for test_example in test_examples:
        result = get_date(test_example)
        print(f"Вход: {test_example}")
        print(f"Выход: {result}")
