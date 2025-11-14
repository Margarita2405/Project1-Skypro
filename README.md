# Проект Банковский виджет "Последние операции"

## Описание:

Проект разработан для IT-отдела крупного банка с целью
реализации новой функциональности в личном кабинете 
клиента - виджета, отображающего несколько последних
успешных банковских операций. Проект представляет
собой бэкенд-составляющую, которая готовит и обрабатывает
данные для отображения в новом виджете.

## Функциональность:

1. **Маскировка номеров карт** (get_mask_card_number)
def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты в формате 
    XXXX XX** **** XXXX, оставляя видимыми первые 6 и 
    последние 4 цифры.
    Пример: '7000792289606361'-> '7000 79** **** 6361'"""

2. **Маскировка номеров счетов** (get_mask_account)
def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета в формате
    **XXXX, оставляя видимыми последние 4 цифры.
    Пример:'73654108430135874305' -> '**4305'"""

3. **Универсальная маскировка** (mask_account_card)
def mask_account_card(info_string: str) -> str:
    """Обрабатывает строку, содержащую тип и номер 
    банковской карты/счета, и возвращает строку с
    замаскированным номером.
    Пример: 'Visa Platinum 7000792289606361' -> 
    'Visa Platinum 7000 79** **** 6361'
    'Счет 73654108430135874305' -> 'Счет **4305'"""

4. **Форматирование даты** (get_date)
def get_date(date_string: str) -> str:
    """Преобразует строку с датой в международном формате 
    в строку с датой в российском формате "ДД.ММ.ГГГГ.
    Пример:'2024-03-11T02:26:18.671407' -> '11.03.2024'"""
     
5. **Фильтрация операций** (filter_by_state)
def filter_by_state(operations: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Фильтрует список словарей по значению ключа 'state'
    (по умолчанию 'EXECUTED') и возвращает новый список словарей,
    у которых ключ 'state' соответствует указанному значению"""

6. **Сортировка операций** (sort_by_date)
def sort_by_date(operations: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """Принимает список словарей с операциями и возвращает новый
    список, отсортированный по ключу 'date'. Сортировка выполняется
    по умолчанию в порядке убывания."""

7. **Фильтрация транзакций по валюте** (filter_by_currency)
def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """Фильтрует транзакции по заданной валюте. Функция принимает список транзакций и возвращает
    итератор, который поочередно выдает транзакции, где валюта операции соответствует заданной."""

8. **Описание транзакций**
def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """Генератор, который возвращает описание каждой транзакции по очереди. Функция принимает
    список транзакций и возвращает итератор, который поочередно выдает строки с описанием операций."""

9. **Генерация номеров банковских карт**
def card_number_generator(start: int, stop: int) -> Generator[str]:
    """Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.Генерирует номера карт
    в заданном диапазоне, начиная с начального значения и заканчивая конечным значением
    включительно. Каждый номер карты форматируется как четыре группы по четыре цифры,
    разделенные пробелами."""

10. **Декоратор для логирования функции**
def log(filename: Optional[str] = None) -> Callable:
    """Декоратор для логирования начала и конца выполнения функции, а также результатов или ошибок.
    Принимает необязательный аргумент filename для записи логов в файл. Если None, логи выводятся в
    консоль."""

11. **Файл с данными о финансовых транзациях**
    data/operations.json

12. **Конвертация валюты с помощью APILayer**
def convert_currency(amount: float, from_currency: str, to_currency: str = "RUB") -> float:
    """Конвертирует сумму из одной валюты в другую используя 
    Exchange Rates Data API"""

13. **Обработка транзакций**
def get_transaction_amount_in_rub(transaction: Dict[str, Any]) -> float:
    """Функция, которая принимает на вход транзакцию и возвращает
    сумму транзакции (amount) в рублях."""

14. **Получение данных из JSON-файла**
def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает данные о финансовых транзакциях из JSON-файла."""


## Установка:

1. Клонируйте репозиторий:
```
git clone https://github.com/Margarita2405/Project1-Skypro
```
2. Установите зависимости:
```
pip install -r requirements.txt
poetry add requests
```
3. НАСТРОЙКИ API ДЛЯ КОНВЕРТАЦИИ ВАЛЮТ. API-ключ для Exchange 
   Rates Data API:
```
Зарегистрируйтесь на https://apilayer.com/marketplace/exchangerates_data-api
и получите бесплатный ключ
API_KEY=your_actual_api_key_here
```
## Использование функций:

from src.masks.py import get_mask_card_number, get_mask_account
from src.widget.py import mask_account_card, get_date
from src.processing.py import filter_by_state, sort_by_date
from src.generators.py import card_number_generator, filter_by_currency, transaction_descriptions
from src.decorators.py import log
from src.external_api.py import convert_currency
from src.transactions.py import get_transaction_amount_in_rub
from src.utils.py import load_transactions

# Пример использования:
masked_number = get_mask_card_number('7000792289606361')
masked_account = get_mask_account('73654108430135874305')
masked_card = mask_account_card('Visa Platinum 7000792289606361')
formatted_date = get_date('2024-03-11T02:26:18.671407')
executed_operations = filter_by_state(operations, "EXECUTED")
canceled_operations = filter_by_state(operations, "CANCELED")
sort_descending = sort_by_date(operations)
sort_ascending = sort_by_date(operations, reverse=False)
usd_transaction = filter_by_currency(transactions, "USD")
descriptions = transaction_descriptions(transactions)
card_numbers = card_number_generator(1, 5)
@log(filename="mylog.txt")
rub_amount = get_transaction_amount_in_rub(transaction)
transactions = load_transactions("data/operations.json")

# Обработка операций:
filtered_operations = filter_by_state('id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364')
sorted_operations = sort_by_date('id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572')

## Тестирование

В этом разделе описываются процедуры тестирования для проекта.

# Цель тестирования

Этот раздел объясняет, зачем нужны тесты для данного проекта.

*   Тесты помогают обеспечить стабильность и качество кода.
*   Проверка функциональности и отсутствие регрессий.

# Использование

Для работы с проектом используются следующие фикстуры в модуле 
conftest.py и параметризация в модулях test_masks.py, 
test_widget.py, test_processing.py, test_generators.py,
test_decorators.py, test_external_api.py, test_transactions.py,
test_utils.py

## Фикстуры

* `standard_card_numbers`: содержит тестовые данные со 
     стандартными номерами банковских карт.
*   `edge_case_card_numbers`: содержит тестовые данные с 
     граничными случаями.
*   `account_samples`: содержит тестовые данные с 
     номерами счетов. 
*   `valid_card_examples`: содержит тестовые данные с 
     валидными примерами карт разных типов.
*   `valid_account_examples`: содержит тестовые данные с 
     валидными примерами счетов.
*   `invalid_input_examples`: содержит тестовые данные с 
     некорректными входными данными и ожидаемыми ошибками.
*   `sample_dates`: содержит тестовые данные с 
     с примерами дат.
*   `sample_operations`: содержит тестовые данные с 
     с примерами операций.
*   `operations_with_same_dates`: содержит тестовые данные с 
     с операциями, содержащими одинаковые даты.
*   `sample_transactions`: содержит тестовые данные с примером 
     транзакций с разными валютами и состояниями.
*   `transactions_with_invalid_structure`: содержит тестовые данные 
     с транзакциями, имеющими некорректную структуру с отсутствующими полями.
*   `empty_transactions`: содержит пустой список транзакций.
*   `transactions_with_missing_fields`: содержит тестовые с
     транзакциями с отсутствующими или некорректными полями.
*   `small_range`: предоставляет малый диапазон для тестирования.
*   `medium_range`: предоставляет средний диапазон для тестирования.
*   `edge_range`: предоставляет крайние значения для тестирования.
*   `small_edge_range`: предоставляет небольшой диапазон для тестирования 
     крайних случаев.
*   `single_number_range`: предоставляет диапазон из одного числа.

## Параметризация
  
*   `test_card_number_mask_correct_format`: тестирование 
    правильности формата маскирования номера карты.
*   `test_card_number_visible_first_6_last_4_digits`: 
    тестирование, что первые 6 и последние 4 цифры остаются 
    видимыми.
*   `test_invalid_inputs`: тестирование некорректных входных 
    данных.
*   `test_account_mask_correct_format`: тестирование правильности
    маскирования банковского номера счета.
*   `test_various_account_lengths`: проверка работы с различными 
    длинами номеров счетов.
*   `test_short_accounts`: проверка обработки очень коротких 
    номеров счетов.
*   `test_only_last_4_digits_visible`: проверка что видны только
    последние 4 цифры.
*   `test_different_card_and_account_types`: тест различных типов
    карт и счетов.
*   `test_invalid_input_handling`: тестирование обработки некорректных 
    входных данных.
*   `test_edge_values`: тестирование граничных значений длины
    номеров.
*   `test_various_date_formats`: проверка работы функции на 
    различных входных форматах даты.
*   `test_non_standard_date_strings`: проверка нестандартных
    строк с датами.
*   `test_problematic_inputs`: тестирование входных данных,
    которые функция обрабатывает без ошибок.
*   `test_filter_by_various_states`: тестирование для 
    различных возможных значений статуса state.
*   `test_sort_parameterized`: тестирование для 
    для различных направлений сортировки.
*   `test_transaction_descriptions_different_sizes`: тестирование для
    проверки работы с разным количеством транзакций.
*   `test_transaction_descriptions_various_formats`: тестирование для
    проверки различных форматов транзакций.
*   `test_card_number_generator_specific_numbers`: Тестирует 
    форматирование конкретных номеров карт.

# Подготовка к тестированию

Для запуска тестов необходимо выполнить следующие действия:

1. Установка зависимостей:
    ```
    pip install -r requirements.txt
    poetry add --group dev pytest
    poetry add --group dev pytest-cov
    poetry add requests
    ```
# Запуск тестов

1. Для запуска всех тестов используйте следующую команду в 
терминале: 
    ```
    pytest tests
    ```
2. Запуск тестов из конкретного файла:
    ```
    pytest tests/test_masks.py
    pytest tests/test_widget.py
    pytest tests/test_processing.py
    pytest tests/test_generators.py
    pytest tests/test_decorators.py
    pytest tests/test_external_api.py
    pytest tests/test_transactions.py
    pytest tests/test_utils.py
    ```
3. Ожидаемый результат.
После успешного выполнения тестов вы должны увидеть вывод, 
подтверждающий, что все тесты успешно пройдены, например:
    ```
    === 10 passed in 0.01s ===
    ```
4. Если тесты не прошли.
Проверьте вывод команды на наличие ошибок.
Обратитесь к файлам тестов для анализа причин сбоев. 

5. Для запуска тестов с оценкой покрытия, используйте следующую
команду в терминале: 
    ```
    pytest --cov
    ```
6. Для создания отчета о покрытии в HTML-формате, используйте 
следующую команду в терминале: 
    ```
    pytest --cov=src --cov-report=html
    ```

## Документация:

Для получения дополнительной информации обратитесь 
к [документации](README.md).

## Лицензия

Проект разработан для внутреннего использования в банковской 
системе.

