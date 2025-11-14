import logging
import os


# Определяем абсолютный путь к папке logs в корне проекта
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # Поднимаемся на уровень выше (из src в корень)
log_dir = os.path.join(project_root, 'logs')

# Создаем отдельный объект логера для модуля masks
logger = logging.getLogger('masks')
logger.setLevel(logging.DEBUG)

# Создаем обработчик файла для логера модуля masks
log_file_path = os.path.join(log_dir, 'masks.log')
file_handler = logging.FileHandler(log_file_path, mode="w", encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# Создаем форматтер для логов
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Устанавливаем форматтер для обработчика
file_handler.setFormatter(file_formatter)

# Добавляем handler для логера модуля masks
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Функция, которая маскирует номер банковской карты, оставляя видимыми первые 6 и последние 4 цифры"""

    logger.debug(f"Начало маскировки номера карты: {card_number}")

    try:
        # Проверяем, что номер карты состоит только из цифр
        if not card_number.isdigit():
            logger.error(f"Номер карты содержит недопустимые символы: {card_number}")
            return "Неверный формат номера карты"

        # Проверяем длину номера карты
        if len(card_number) != 16:
            logger.error(f"Некорректная длина номера карты: {len(card_number)} (ожидается 16)")
            return "Неверная длина номера карты"

        # Разбиваем номер карты на части
        first_part = card_number[:4]  # Первые 4 цифры номера карты
        second_part = card_number[4:6]  # Следующие 2 цифры номера карты
        last_part = card_number[-4:]  # Последние 4 цифры номера карты

        # Создаем замаскированную строку
        masked_number = f"{first_part} {second_part} ** **** {last_part}"

        logger.info(f"Успешная маскировка номера карты: {card_number} -> {masked_number}")
        return masked_number

    except Exception as e:
        logger.error(f"Ошибка при маскировке номера карты {card_number}: {str(e)}")
        return "Ошибка при обработке номера карты"


def get_mask_account(account_number: str) -> str:
    """Функция, которая маскирует номер банковского счета, оставляя видимыми последние 4 цифры"""

    logger.debug(f"Начало маскировки номера счета: {account_number}")

    try:
        # Проверяем, что номер счета состоит только из цифр
        if not account_number.isdigit():
            logger.error(f"Номер счета содержит недопустимые символы: {account_number}")
            return "Неверный формат номера счета"

        # Проверяем длину номера счета
        if len(account_number) < 4:
            logger.error(f"Номер счета слишком короткий: {len(account_number)} (минимум 4 символа)")
            return "Неверная длина номера счета"

        # Получаем последние 4 цифры номера счета
        last_four_digits = account_number[-4:]

        # Создаем замаскированную строку
        masked_account = f"** {last_four_digits}"

        logger.info(f"Успешная маскировка номера счета: {account_number} -> {masked_account}")
        return masked_account

    except Exception as e:
        logger.error(f"Ошибка при маскировке номера счета {account_number}: {str(e)}")
        return "Ошибка при обработке номера счета"


if __name__ == "__main__":
    # Тестирование функции маскировки карты
    print(get_mask_card_number("5946823031801656"))

    # Тестирование функции маскировки счета
    print(get_mask_account("40817810207005367456"))

    # Тестирование с ошибочными данными
    print(get_mask_card_number("123"))  # Слишком короткий номер
    print(get_mask_card_number("594682303180165A"))  # Недопустимые символы
    print(get_mask_account("123"))  # Слишком короткий номер счета
    print(get_mask_account("4081781020700536745A"))  # Недопустимые символы
