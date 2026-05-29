import pytest
from playwright.sync_api import Page
import allure
from pathlib import Path

import utils.common_steps as steps
import utils.business_steps as biz


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.critical
@pytest.mark.order_flow
@allure.feature("Orders")
@allure.story("Flight cancel")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Два заказа в один рейс и удалить груз из рейса")
@allure.description("""
1. Загрузить два заказа в один рейс через меню управление рейсом
2. Удалить один из грузов в рейсе
3. Завершить рейс
4. Проверить заказ с удалённым грузом
""")
def test_flight_two_order_delete_shipment(chromium_page: Page):
    """
    Тест проверяет сценарий создания рейса с двумя заказами,
    удаления одного груза и завершения рейса.
    
    Ожидаемый результат:
    - Заказ с удалённым грузом должен быть в статусе "В работе"
    - Заказ с завершённым грузом должен быть в статусе "Завершен"
    """
    page = chromium_page
    
    # Подготовка: путь к тестовым данным
    base_dir = Path(__file__).parent.parent
    file_path = base_dir / "testdata" / "excel_1x1_two_order_in_flight.xlsm"
    
    # Шаг 1: Авторизация
    steps.login(page)
    
    # Шаг 2: Создание двух заказов из Excel и принятие предложений
    order_ids = biz.create_two_orders_and_accept_offers(page, file_path)
    
    # Шаг 3: Создание рейса с двумя заказами, удаление груза и завершение
    flight_id = biz.create_flight_with_two_orders_delete_shipment_and_complete(
        page, 
        order_ids
    )
    
    # Шаг 4: Переход на вкладку "Все" для проверки статусов
    steps.switch_to_tab(page, "Все")
    
    # Шаг 5: Проверка финальных статусов заказов
    steps.assert_order_statuses_present(page, ["В работе", "Завершен"])
    
    steps.close_filters(page)