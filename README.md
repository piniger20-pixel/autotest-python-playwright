# Репозиторий создан для демонстрации подходов к автоматизации, архитектуры тестов и стиля кода.

## Список тестов

| № | Название теста | Что проверяет |
|---|----------------|----------------|
| 1 | `test_basic_conditions_template_v_default` | Создание шаблона условия для заказа, проверка фильтров для ШУ |
| 2 | `test_excel_matcher_+vat` | Проверка ставок НДС/без НДС |
| 3 | `test_executor_cancel_order_in_work` | Создание рейса, отмена рейса исполнителем |
| 4 | `test_flight_add_shipment_check_forwarders_flight` | Создание рейса, добавление заказа к существующему рейсу |
| 5 | `test_flight_cancel` | Отмена рейса в разных статусах |
| 6 | `test_flight_two_order_delete_shipment` | Создание рейса и удаление груза |
| 7 | `test_forwarder_cancel_order_in_work` | Создание рейса, отмена рейса заказчиком |
| 8 | `test_new_driver` | Создание водителя |
| 9 | `test_new_order_to_closed_trade` | Создание заказа в закрытые торги |
| 10 | `test_partners_groups` | CRUD операций с группами партнёров |
| 11 | `test_simpleTask_autogen_cancelTask` | Задачи для разных ролей, удаление задачи |

## Структура проекта

- `Project Root/`
  - test/` - папка с автотестами
  - `fixtures/`
  - `helpers/`
  - `utils/`
    - `business_steps/`Бизнес шаги
    - `steps/`Шаги для тестов
  - `requirments.txt
  - `config.py`

### Требования

Убедитесь, что в вашей системе установлено:

- Python 3.12 or later
- pip (Python package manager)
- Git

### Установка

Создание и активация виртуальной среды:

```shell
python3 -m venv venv # Create virtual environment
```

Установить плагин Python в VSCode, активируйте виртуальную среду:
```shell
В VS Code нажать Cmd+shift+P -> найти Python: Select Interpreter -> выбрать (venv)
В VS Code нажать Cmd+shift+P - найти Python: Configure Test -> pytest (и выбрать tests)
```


Установка dependencies:

```shell
pip install --upgrade pip # Upgrade pip to the latest version
pip install -r requirements.txt # Install required dependencies
playwright install # Install playwright dependencies
```

## Запуск тестов

Запустить все тесты:

```shell
pytest
```

Запустить конкретного теста:

```shell
pytest {путь до теста}
```


Для запуска UI тестов с помощью pytest: (-m Маркировка):

```shell
pytest -m regression
```

Выполнить регрессионные тесты параллельно:

```shell
pytest -m regression --numprocesses 2
```

## Генерация Allure Reports

Выполнить тесты и создать Allure результат:

```shell
pytest -m regression --alluredir=allure-results
```

Открыть результаты Allure локально:

```shell
allure serve allure-results
```
