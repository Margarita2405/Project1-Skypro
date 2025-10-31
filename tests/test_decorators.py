import os
import tempfile
from typing import NoReturn

import pytest
from pytest import CaptureFixture

from src.decorators import log


@log()
def successful_function_no_file(x: int, y: int) -> int:
    """Функция, которая всегда выполняется успешно для тестирования вывода в консоль."""
    return x + y


@log()
def failing_function_no_file(x: int, y: int) -> NoReturn:
    """Функция, которая всегда вызывает исключение для тестирования вывода ошибок в консоль."""
    raise ValueError("Test error")


def test_additional_scenario_with_kwargs(capsys: CaptureFixture[str]) -> None:
    """Тестирует работу декоратора с именованными аргументами."""

    @log()
    def func_with_kwargs(a: int, b: int = 10) -> int:
        """Вспомогательная функция для тестирования ключевых аргументов."""
        return a + b

    # Вызываем функцию с именованным аргументом
    result = func_with_kwargs(5, b=15)

    # Проверяем результат и вывод
    captured = capsys.readouterr()
    assert result == 20
    assert "func_with_kwargs ok" in captured.out


def test_empty_arguments_function(capsys: CaptureFixture[str]) -> None:
    """Тестирует работу декоратора с функцией без аргументов."""

    @log()
    def no_args_func() -> int:
        """Вспомогательная функция без аргументов для тестирования."""
        return 25

    # Вызываем функцию без аргументов
    result = no_args_func()

    # Проверяем результат и логирование
    captured = capsys.readouterr()
    assert result == 25
    assert "no_args_func ok" in captured.out


def test_successful_function_execution(capsys: CaptureFixture[str]) -> None:
    """Тестирует успешное выполнение декорированной функции с выводом в консоль."""

    # Подготавливаем тестовые данные
    test_x = 10
    test_y = 5
    expected_result = 15

    # Вызываем успешную функцию
    actual_result = successful_function_no_file(test_x, test_y)

    # Проверяем результат и логи
    captured = capsys.readouterr()
    assert actual_result == expected_result, f"Ожидался результат {expected_result}, получен {actual_result}"
    assert "successful_function_no_file ok" in captured.out, "Должно быть сообщение об успешном выполнении"


def test_failing_function_execution(capsys: CaptureFixture[str]) -> None:
    """Тестирует выполнение декорированной функции с исключением и выводом в консоль."""

    # Подготавливаем тестовые данные
    test_x = 7
    test_y = 3

    # Проверяем, что исключение выбрасывается
    with pytest.raises(ValueError, match="Test error"):
        failing_function_no_file(test_x, test_y)

    # Проверяем логи на ошибки
    captured = capsys.readouterr()
    expected_log = f"failing_function_no_file error: ValueError: Test error. Inputs: ({test_x}, {test_y}), {{}}\n"
    assert captured.out == expected_log


def test_successful_execution_file_logging() -> None:
    """Тестирует успешное выполнение функции с записью в файл."""
    # Создаем временный файл
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as temp_file:
        temp_filename = temp_file.name

    try:
        # Тестируем запись в файл
        @log(filename=temp_filename)
        def multiply(x: int, y: int) -> int:
            return x * y

        result = multiply(5, 6)

        assert result == 30

        # Проверяем содержимое файла
        with open(temp_filename, "r") as file:
            log_content = file.read()

        assert "multiply ok" in log_content

    finally:
        # Удаляем временный файл
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)


def test_failing_execution_file_logging() -> None:
    """Тестирует выполнение функции с ошибкой и записью в файл."""
    # Создаем временный файл
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as temp_file:
        temp_filename = temp_file.name

    try:

        @log(filename=temp_filename)
        def divide(a: int, b: int) -> float:
            """Тестовая функция, которая может вызвать ZeroDivisionError."""
            return a / b

        # Проверяем, что при вызове функции с нулевым делителем возникает ZeroDivisionError
        with pytest.raises(ZeroDivisionError):
            divide(10, 0)

        # Читаем содержимое файла лога после выполнения функции
        with open(temp_filename, "r") as file:
            log_content = file.read()

        # Проверяем, что в логе содержится ожидаемое сообщение об ошибке
        assert "divide error: ZeroDivisionError: division by zero. Inputs: (10, 0), {}" in log_content

    finally:
        # Удаляем временный файл
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)
