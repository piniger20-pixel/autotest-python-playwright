import pytest
from playwright.sync_api import Page
import allure
import logging
from config import EMPLOYEE_EMAIL
import utils.common_steps as steps
import utils.business_steps as biz

log = logging.getLogger(__name__)

@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.critical
@allure.feature("Orders")
@allure.story("Create new order to closed trade")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Создание заказа типа 'авто закрытые торги' и проверка его в таблице заказов")
@allure.description("""
Тест проверяет полный цикл создания заказа типа 'авто закрытые торги':
1. Авторизация в системе
2. Создание нового заказа с заполнением обязательных полей
3. Сохранение заказа на торги
4. Поиск созданного заказа в таблице заказов
5. Проверка статуса и типа торгов созданного заказа
""")

def test_order_creation_1x1_closed_trade(chromium_page: Page):
    """
    Бизнес-тест: Создание заказа типа 1x1 с закрытыми торгами и проверка в таблице заказов.
    
    Этот тест следует слоистой архитектуре:
    - Использует бизнес-шаги для высокоуровневых сценариев
    - Использует атомарные шаги для взаимодействия с UI
    - Без UI-локаторов в самом тесте
    """
    page = chromium_page
    
    # Шаг 1: Авторизация в системе
    steps.login(page, email=EMPLOYEE_EMAIL)
    
    # Шаг 2: Создание заказа на торги с типом "закрытые торги"
    # Бизнес-шаг, который композирует атомарные шаги:
    # - Открытие формы создания заказа
    # - Выбор шаблона
    # - Выбор дат
    # - Сохранение заказа
    order_id = biz.create_order_on_auction(
        page,
        template_name="авто закрытые торги",
        pickup_date_offset=7,
        delivery_date_offset=9
    )
    
    # Шаг 3: Переход в таблицу заказов Заказчика
    steps.open_forwarder_orders(page)
    page.wait_for_load_state('load')
    steps.close_filters(page)
    
    # Шаг 4: Фильтрация по ID заказа
    steps.filter_by(page, "ID заказа", order_id)
    log.info(f"✅ Заказ {order_id} успешно найден в таблице")
    
    # Шаг 5: Проверка статуса заказа
    steps.assert_order_in_table(page, order_id, "Торги")
    
    # Шаг 6: Проверка типа торгов
    steps.assert_trade_type(page, order_id, "Закрытые торги")
    
    # Очистка: закрытие фильтров
    steps.close_filters(page)