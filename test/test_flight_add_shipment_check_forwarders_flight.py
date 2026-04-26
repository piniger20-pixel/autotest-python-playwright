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
@allure.title("Добавление груза в существующий рейс и проверка рейса заказчиком")
@allure.description("""Создать рейс. Добавить к рейсу груз. Проверить видимость рейса со стороны заказчика""")
def test_flight_add_shipment_check_forwarders_flight(chromium_page: Page):
    """
    Тест проверяет:
    1. Создание двух заказов из Excel
    2. Принятие предложений по обоим заказам
    3. Создание рейса с первым заказом
    4. Добавление второго заказа к существующему рейсу
    5. Проверку видимости рейса со стороны заказчика
    6. Проверку наличия обоих грузов в деталях рейса
    """
    page = chromium_page
    
    # Подготовка данных
    base_dir = Path(__file__).parent.parent
    file_path = base_dir / "testdata" / "excel_1x1_two_order_in_flight.xlsm"
    
    # Шаг 1: Создаём два заказа и принимаем предложения
    order_ids = biz.create_two_orders_and_accept_offers(page, file_path)
    
    # Шаг 2: Создаём рейс с первым заказом
    flight_id = biz.create_flight_with_first_order_and_verify(page, order_ids)
    
    # Шаг 3: Добавляем второй заказ к рейсу
    biz.add_second_order_to_flight(page, flight_id, order_ids)
    
    # Шаг 4: Проверяем рейс со стороны заказчика
    biz.verify_flight_from_forwarder_side(page, flight_id, order_ids)
    
    # Шаг 5: Проверяем грузы в деталях рейса
    biz.verify_shipments_in_flight_details(page, flight_id)
    
    
    steps.close_filters(page)