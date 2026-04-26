# Что тестируют автоесты
1.test_basic_conditions_template_v_default - создания шаблона условия для заказа, проверка фильтров для ШУ и подставновка ШУ в заказ
2.test_excel_matcher_+vat - проверка ставок в заказе НДС/без НДС
3.test_executor_cancel_order_in_work - Создание рейса для заказ, отмена рейса исполнителем
4.test_flight_add_shipment_check_forwarders_flight - создание рейса, добавление заказа к существующему рейсу 
5.test_flight_cancel - Отмена рейса в разных статусах
6.test_flight_two_order_delete_shipment - Создание рейса и удаление груза из рейсов
7.test_forwarder_cancel_order_in_work - Создание рейса для заказ, отмена рейса заказчиком
8.test_new_driver - создание водителя
9.test_new_order_to_closed_trade - Создание заказ в закрытые торги
10.test_partners_groups - создание группы партнёров, активация группы в заказе, удаление группы партнёров
11.test_simpleTask_autogen_cancelTask - создать заказ с простой задачей, отображение задач для разных ролей, удаение простой задаче в заказе

## Структура проекта
Project Root
├── tests/                # Тесты (e2e, api, smoke, regression)
│   ├── conftest.py       # Фикстуры pytest
│   ├── e2e/              # Сквозные тесты
│ 
├── pages/                # Page Object классы
│   ├── base_page.py
│   ├── login_page.py
│   └── dashboard_page.py
├── components/           # UI-компоненты (Navbar, Modal, Table)
├── elements/             # Базовые элементы (Button, Input, Dropdown)
├── fixtures/             # Кастомные фикстуры (db, browser, api_client)
├── helpers/              # Вспомогательные функции (wait, random_data)
├── utils/                # Утилиты (logger, config_loader, db_connector)
│   ├── business_steps    # Шаги объёдинённые в значемые бизнес действия 
│   └── steps             # Шаги для автотестов
├── qa_agent/             # AI-модуль (генерация тестов, анализ coverage)
├── scripts/              # Скрипты автоматизации (deploy, prepare_env)
├── allure-results/       # Результаты Allure (временные)
├── allure-report/        # Готовый отчёт Allure (HTML)
└── config.py             # Централизованная конфигурация

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