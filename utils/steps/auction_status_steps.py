import allure
import pytest
from playwright.sync_api import Page


@allure.step("Ожидаем смены статуса торгов на '{expected_status}'")
def wait_for_auction_status_change(page: Page, expected_status: str, max_attempts: int = 12, wait_seconds: int = 10):
    """
    Ожидает смены статуса торгов на указанный.
    
    Args:
        page: Playwright page object
        expected_status: Ожидаемый статус торгов
        max_attempts: Максимальное количество попыток
        wait_seconds: Время ожидания между попытками в секундах
    """
    print(f"⏳ Ожидаем смены статуса торгов на '{expected_status}' ⏳")
    status_found = False
    
    for attempt in range(max_attempts):
        try:
            status_text = page.locator('[data-qa="orders-table-auction-status-0"]').get_by_text(expected_status)
            if status_text.is_visible(timeout=3000):
                status_found = True
                print(f"✅ Статус '{expected_status}' найден (попытка {attempt + 1})")
                break
        except:
            pass  # Статус еще не изменился
        
        if attempt < max_attempts - 1:
            page.reload()
            page.wait_for_load_state('load')
            page.wait_for_timeout(wait_seconds * 1000)
    
    if not status_found:
        pytest.fail(f"❌ Статус не изменился на '{expected_status}' за {max_attempts * wait_seconds} секунд")


@allure.step("Ожидаем смены статуса заказа на '{expected_status}'")
def wait_for_order_status_change(page: Page, expected_status: str, max_attempts: int = 10, wait_seconds: int = 5):
    """
    Ожидает смены статуса заказа на указанный.
    
    Args:
        page: Playwright page object
        expected_status: Ожидаемый статус заказа
        max_attempts: Максимальное количество попыток
        wait_seconds: Время ожидания между попытками в секундах
    """
    print(f"⏳ Ожидаем смены статуса заказа на '{expected_status}' ⏳")
    status_found = False
    
    for attempt in range(max_attempts):
        try:
            status_text = page.locator('[data-qa="orders-table-order-status-0"]').get_by_text(expected_status)
            if status_text.is_visible(timeout=3000):
                status_found = True
                print(f"✅ Статус '{expected_status}' найден (попытка {attempt + 1})")
                break
        except:
            pass  # Статус еще не изменился
        
        if attempt < max_attempts - 1:
            page.reload()
            page.wait_for_load_state('load')
            page.wait_for_timeout(wait_seconds * 1000)
    
    if not status_found:
        pytest.fail(f"❌ Статус не изменился на '{expected_status}' за {max_attempts * wait_seconds} секунд")


@allure.step("Проверяем статус ТОРГОВ в таблице Заказчика")
def assert_auction_status_in_customer_table(page: Page, expected_status: str):
    """
    Проверяет статус торгов в таблице заказчика.
    
    Args:
        page: Playwright page object
        expected_status: Ожидаемый статус торгов (например, "Идут")
    """
    from playwright.sync_api import expect
    
    status_text = page.locator('[data-qa="orders-table-auction-status-0"]').get_by_text(expected_status)
    expect(status_text).to_be_visible(timeout=5000)
    expect(status_text).to_have_text(expected_status)
    full_block = page.locator('[data-qa="orders-table-auction-status-0"]')
    full_text = full_block.text_content().strip()
    print(f"✅ Статус торгов корректный:: '{full_text}'")