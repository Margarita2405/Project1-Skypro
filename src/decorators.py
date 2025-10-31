from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """Декоратор для логирования начала и конца выполнения функции, а также результатов или ошибок.
    Принимает необязательный аргумент filename для записи логов в файл. Если None, логи выводятся в
    консоль."""

    def decorator(func: Callable) -> Callable:
        """Внутренний декоратор, который применяется к целевой функции. Принимает функцию, которую
        нужно декорировать."""

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Обертка функции, добавляющая логирование, принимающая позиционные и именованные
            аргументы функции."""
            try:
                # Выполняем исходную функцию
                result = func(*args, **kwargs)

                # Логируем успешное выполнение
                log_message = f"{func.__name__} ok"

            except Exception as e:
                # Логируем ошибку с информацией о входных параметрах
                log_message = f"{func.__name__} error: {type(e).__name__}: {str(e)}. Inputs: {args}, {kwargs}"
                raise  # Пробрасываем исключение дальше

            finally:
                # Записываем лог в файл или выводим в консоль
                if filename:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(log_message + "\n")
                else:
                    print(log_message)

            return result

        return wrapper

    return decorator


# Примеры использования
if __name__ == "__main__":

    @log(filename="mylog.txt")
    def my_function(x: int, y: int) -> int:
        """Складывает два числа."""
        return x + y

    @log()  # Логирование в консоль
    def failing_function(x: int, y: int) -> int:
        """Функция, которая всегда вызывает ошибку."""
        raise ValueError("Test error message")

    @log(filename="operations.log")
    def divide(a: float, b: float) -> float:
        """Делит a на b."""
        return a / b
