import allure
from helpers.ui import qa_key, wait_and_click
import utils.common_steps as steps
from playwright.sync_api import Page

ORDER_CARGO_ID_INPUT = 'order-form-transport-cargo-input'
ORDER_CARGO_DELETE_BTN = 'order-form-shipments-remove-shipment-button'

ORDER_START_BIDDING_DATE_INPUT = 'order-form-auction-start-date-datepicker'

ORDER_SAVE_BTN = 'order-form-actions-save-order-button'


@allure.step("Редактируем ID заказа клиента на {text}")
def edit_order_cargo_id(page: Page, text: str):
    steps.write_input(page, qa_key(ORDER_CARGO_ID_INPUT), text)


@allure.step("Удаляем груз {index}")
def delete_cargo(page: Page, index: int):
    wait_and_click(page, qa_key(ORDER_CARGO_DELETE_BTN, index))


@allure.step("Изменяем дату начала торгов на сейчас")
def edit_start_bidding_date_now(page: Page):
    datepicker = page.locator(qa_key(ORDER_START_BIDDING_DATE_INPUT))

    clear_btn = datepicker.locator('button[aria-label="Очистить"]')
    if clear_btn.count() > 0 and clear_btn.is_visible():
        clear_btn.click()


@allure.step("Сохраняем изменения")
def save_changes(page: Page):
    wait_and_click(page, qa_key(ORDER_SAVE_BTN))