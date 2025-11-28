import logging
import json
import os
from typing import List, Dict, Any


# Определяем абсолютный путь к папке logs в корне проекта
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # Поднимаемся на уровень выше (из src в корень)
log_dir = os.path.join(project_root, 'logs')

# Создаем отдельный логгер для модуля utils
logger = logging.getLogger('utils')
logger.setLevel(logging.DEBUG)

# Создаем обработчик файла с абсолютным путем
log_file_path = os.path.join(log_dir, 'utils.log')
file_handler = logging.FileHandler(log_file_path, mode="w", encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# Создаем форматтер для логов
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Устанавливаем форматтер для обработчика
file_handler.setFormatter(file_formatter)

# Добавляем обработчик к логгеру
logger.addHandler(file_handler)


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает данные о финансовых транзакциях из JSON-файла."""
    logger.debug(f"Попытка загрузить транзакции из файла: {file_path}")

    # Проверяем существование файла
    if not os.path.exists(file_path):
        logger.error(f"Файл не найден: {file_path}")
        return []

    # Проверяем, что это файл, а не директория
    if not os.path.isfile(file_path):
        logger.error(f"Указанный путь не является файлом: {file_path}")
        return []

    # Проверяем, что файл не пустой
    if os.path.getsize(file_path) == 0:
        logger.warning(f"Файл пустой: {file_path}")
        return []

    try:
        # Открываем и читаем файл
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Проверяем, что данные являются списком
        if isinstance(data, list):
            logger.info(f"Успешно загружено {len(data)} транзакций из файла {file_path}")
            return data
        else:
            logger.warning(f"Данные в файле {file_path} не являются списком")
            return []

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}: {str(e)}")
        return []
    except FileNotFoundError:
        logger.error(f"Файл не найден после проверки существования: {file_path}")
        return []
    except Exception as e:
        logger.error(f"Неизвестная ошибка при загрузке файла {file_path}: {str(e)}")
        return []


# Пример использования
if __name__ == "__main__":
    # Формируем путь к файлу
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(current_dir, "data", "operations.json")

    # Загрузка транзакций из файла
    transactions = load_transactions(file_path)

    # Вывод результата
    print(f"Загружено {len(transactions)} транзакций")
    for transaction in transactions:
        print(transaction)
