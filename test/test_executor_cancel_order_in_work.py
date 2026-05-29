import pytest
from playwright.sync_api import Page
from pathlib import Path
import allure

import utils.business_steps as biz


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.critical
@pytest.mark.order_flow
@allure.feature("Orders")
@allure.story("Forwarder Order cancel")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Отмена заказа заказчиком")
@allure.description("""
Проверка отмены заказа и отмены рейса после отказа от заказа.

Сценарий:
1. Создание заказа из Excel файла
2. Принятие предложения исполнителем (переход в статус "В работе")
3. Создание рейса для заказа
4. Отмена заказа заказчиком с указанием причины
5. Проверка причины отмены и комментария в детализации
6. Проверка статуса заказа "Отзыв из исполнения"
7. Проверка автоматической отмены рейса (статус "Отменен до начала")
""")
def test_forwarder_cancel_order_in_work(chromium_page: Page):
    """
    Тест проверяет полный цикл отмены заказа заказчиком:
    - Создание и принятие заказа
    - Создание рейса
    - Отмену заказа с проверкой причины
    - Автоматическую отмену рейса
    """
    page = chromium_page
    base_dir = Path(__file__).parent.parent
    file_path = base_dir / "testdata" / "excel_1x1_flight_cancel.xlsm"
    
    # 1. Создаём заказ из Excel и принимаем предложение 1x1
    order_id = biz.create_order_from_excel_and_accept_offer(page, file_path)
    
    # 2. Создаём рейс для заказа
    flight_id = biz.create_flight_for_order_and_verify(page, order_id)
    
    # 3. Отменяем заказ исполнителем и проверяем комментарий в черновике и в дарксайде
    biz.cancel_order_by_executor_and_verify(page, order_id)
    
    # 4. Проверяем что рейс автоматически отменён
    biz.verify_flight_cancelled_after_order_cancellation(page, flight_id, skip_forwarder_steps=True)


if __name__ == "__main__":
    import logging
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    test_forwarder_cancel_order_in_work()