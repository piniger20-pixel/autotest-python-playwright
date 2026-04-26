import pytest
from playwright.sync_api import Page
from pathlib import Path
import allure
import logging

import utils.common_steps as steps
import utils.business_steps as biz

log = logging.getLogger(__name__)


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.critical
@pytest.mark.order_flow
@allure.feature("Orders")
@allure.story("Flight cancel")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Отмена рейса до и после погрузки")
@allure.description("""
Проверка отмены рейса в двух сценариях:
1. Отмена рейса до начала выполнения (статус "Не начат" -> "Отменен до начала")
2. Отмена рейса после начала выполнения (статус "В пути" -> "Отказ")
""")
def test_flight_cancel(chromium_page: Page):
    """
    Тест проверяет два сценария отмены рейса:
    
    Сценарий 1: Отмена рейса до начала
    - Создаём заказ из Excel
    - Принимаем предложение 1x1
    - Создаём рейс
    - Отменяем рейс до начала выполнения
    - Проверяем статус "Отменен до начала"
    
    Сценарий 2: Отмена рейса после начала
    - Создаём второй рейс для того же заказа
    - Начинаем выполнение рейса (меняем статус на "В пути")
    - Отменяем рейс
    - Проверяем статус "Отказ"
    """
    page = chromium_page
    
    # Подготовка: путь к тестовым данным
    base_dir = Path(__file__).parent.parent
    file_path = base_dir / "testdata" / "excel_1x1_flight_cancel.xlsm"
    
    # Создаём заказ из Excel и принимаем предложение
    order_id = biz.create_order_from_excel_and_accept_offer(page, file_path)
    
    # Сценарий 1: Отмена рейса до начала выполнения
    with allure.step("Сценарий 1: Создаём рейс и отменяем до начала"):
        flight_id_1 = biz.create_flight_and_cancel_before_start(page, order_id)
        print(f"\n✅ Рейс {flight_id_1} успешно отменен до начала\n")
    
    # Сценарий 2: Отмена рейса после начала выполнения
    with allure.step("Сценарий 2: Создаём рейс, начинаем выполнение и отменяем"):
        flight_id_2 = biz.create_flight_start_and_cancel(page, order_id)
        print(f"\n✅ Рейс {flight_id_2} успешно отменен после начала (статус 'Отказ')\n")


if __name__ == "__main__":
    log.setLevel(logging.DEBUG)
    test_flight_cancel()