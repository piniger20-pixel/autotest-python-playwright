import allure
from helpers.ui import qa_key, wait_and_click
import utils.common_steps as steps
from playwright.sync_api import expect, Page

ORDER_LINK_BTN = 'order-link'

ORDER_STATUS_LABEL = 'orders-table-order-status-0'
ORDER_BIDDING_STATUS_LABEL = 'orders-table-auction-status-0'

ORDER_IDENTIFIER_MENU_BTN = 'orders-table-identifier-menu-button-0'
ORDER_CANCEL_BIDDING_BTN = 'orders-table-identifier-menu-forwarder-cancel-demand-button'
ORDER_DRAFT_EDIT_BTN = 'orders-table-identifier-menu-forwarder-edit-button'


@allure.step("Открываем таблицу Заказчика")
def open_table_via_menu(page: Page):
    wait_and_click(page, '[role="menuitem"]:has-text("Заказчик")')


@allure.step("Проверяем статус заказа")
def check_order_status(page: Page, status: str):
    status_label = page.locator(qa_key(ORDER_STATUS_LABEL))
    expect(status_label).to_be_visible(timeout=5000)
    order_status = status_label.text_content().strip()
    status = status.strip()
    print(f"Статус заказа: {order_status}, ожидаемый статус: {status}")
    assert status in order_status, f"❌ Статус заказа не {status}"
    print(f"✅ Статус заказа корректный: {status}")


@allure.step("Проверяем статус торгов заказа")
def check_order_bidding_status(page: Page, status: str):
    status_label = page.locator(qa_key(ORDER_BIDDING_STATUS_LABEL))
    expect(status_label).to_be_visible(timeout=5000)
    order_bidding_status = status_label.text_content().strip()
    status = status.strip()
    print(
        f"Статус торгов: {order_bidding_status}, ожидаемый статус торгов: {status}")
    assert status in order_bidding_status, f"❌ Статус торгов не {status}"
    print(f"✅ Статус торгов корректный: {status}")


@allure.step("Отменяем заказ с торгов")
def cancel_order_bidding(page: Page):
    wait_and_click(page, qa_key(ORDER_IDENTIFIER_MENU_BTN))
    wait_and_click(page, qa_key(ORDER_CANCEL_BIDDING_BTN))
    wait_and_click(page, '[type="submit"]:has-text("Отменить торги")')


@allure.step("Открываем заказ Черновик на редактирование")
def open_edit_draft_order(page: Page):
    wait_and_click(page, qa_key(ORDER_IDENTIFIER_MENU_BTN))
    wait_and_click(page, qa_key(ORDER_DRAFT_EDIT_BTN))
