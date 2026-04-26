import allure
from playwright.sync_api import expect, Page
import json
import re
from datetime import date, timedelta
from config import EMPLOYEE_EMAIL, APP_URL
from helpers.ui import wait_and_click


@allure.step("Отозвать заказ заказчиком с причиной '{reason_text}' и комментарием '{comment_text}'")
def cancel_order_by_customer(
    page: Page, 
    reason_text: str = "Исполнитель не подал ТС под погрузку",
    comment_text: str = "тест по отмене заказа заказчиком"
):
    # Нажать на кнопку "отозвать заказ
    revoke_button = page.locator('[data-qa="orders-table-identifier-menu-forwarder-revoke-order-button"]')
    revoke_button.wait_for(state="visible", timeout=10000)
    revoke_button.click()  
    # открыть дропдаун с причинами
    choose_reason_button = page.locator('button:has-text("Запрос не актуален")').first
    choose_reason_button.wait_for(state="visible", timeout=10000)
    choose_reason_button.click()
    page.wait_for_timeout(1500) 
    # Выбираем причину
    reason_option = page.locator(f'[role="option"]:has-text("{reason_text}")').first
    reason_option.wait_for(state="visible", timeout=5000)
    reason_option.click()
    # Пишем комментарий
    comment_textarea = page.locator('textarea[name="comment"]')
    comment_textarea.click()
    page.wait_for_timeout(1500)
    comment_textarea.fill(comment_text)
    # Проверяем что текст ввёлся (опционально)
    entered_text = comment_textarea.input_value()
    assert entered_text == comment_text, f"❌ Ожидалось '{comment_text}', получено '{entered_text}'"
    print("✅ Комментарий добавлен")
    # Нажать кнопку отменить заказ
    cancel_order_button = page.get_by_text("Отменить заказ", exact=True)
    cancel_order_button.click()
    page.wait_for_timeout(1500)


@allure.step("Выбрать 'Отменить торги' в меню заказа")
def click_cancel_auction_menu_item(page: Page):
    """Нажать на пункт меню 'Отменить торги'"""
    cancel_menu_item = page.locator('[data-qa="orders-table-identifier-menu-forwarder-cancel-demand-button"]')
    cancel_menu_item.wait_for(state="visible", timeout=5000)
    cancel_menu_item.click()


@allure.step("Нажать на кнопку с текстом 'не актуально' в попапе отмены")
def click_not_actual_reason_button(page: Page):
    """Нажать на кнопку 'не актуально' в модальном окне отмены"""
    reason_button = page.locator('button:has-text("не актуально")').first
    reason_button.wait_for(state="visible", timeout=10000)
    reason_button.click()
    page.wait_for_timeout(1500)


@allure.step("Выбрать причину 'другое' в дропдауне отмены")
def select_other_reason(page: Page):
    """Выбрать причину 'другое' в выпадающем списке"""
    reason_option = page.locator('[role="option"]:has-text("другое")').first
    reason_option.wait_for(state="visible", timeout=5000)
    reason_option.click()


@allure.step("Ввести комментарий в поле для комментария")
def enter_cancellation_comment(page: Page, comment_text: str):
    """Ввести текст комментария в textarea"""
    comment_textarea = page.locator('textarea[placeholder*="Комментарий"]')
    comment_textarea.wait_for(state="visible", timeout=5000)
    comment_textarea.click()
    page.wait_for_timeout(1500)
    comment_textarea.fill(comment_text)
    entered_text = comment_textarea.input_value()
    assert entered_text == comment_text, f"❌ Ожидалось '{comment_text}', получено '{entered_text}'"


@allure.step("Подтвердить отмену торгов")
def confirm_cancel_auction(page: Page):
    """Нажать кнопку подтверждения отмены торгов"""
    page.wait_for_timeout(2000)
    cancel_confirm_button = page.locator('button:has-text("Отменить торги")').nth(1)
    cancel_confirm_button.wait_for(state="visible", timeout=5000)
    cancel_confirm_button.click(force=True)
    page.wait_for_timeout(2000)

@allure.step("Отозвать заказ исполнителем с причиной '{reason_text}' и комментарием '{comment_text}'")
def cancel_order_by_executor(
    page: Page, 
    reason_text: str = "Ошибочно активировал",
    comment_text: str = "тест по отмене заказа исполнителем"
):
    # Нажать на кнопку "отозвать заказ
    revoke_button = page.locator('[data-qa="orders-table-identifier-menu-executor-revoke-order-button"]')
    revoke_button.wait_for(state="visible", timeout=10000)
    revoke_button.click()  
    # открыть дропдаун с причинами
    choose_reason_button = page.locator('button:has-text("Неисправность ТС")').first
    choose_reason_button.wait_for(state="visible", timeout=10000)
    choose_reason_button.click()
    page.wait_for_timeout(1500) 
    # Выбираем причину
    reason_option = page.locator(f'[role="option"]:has-text("{reason_text}")').first
    reason_option.wait_for(state="visible", timeout=5000)
    reason_option.click()
    # Пишем комментарий
    comment_textarea = page.locator('textarea[name="comment"]')
    comment_textarea.click()
    page.wait_for_timeout(1500)
    comment_textarea.fill(comment_text)
    # Проверяем что текст ввёлся (опционально)
    entered_text = comment_textarea.input_value()
    assert entered_text == comment_text, f"❌ Ожидалось '{comment_text}', получено '{entered_text}'"
    print("✅ Комментарий добавлен")
    # Нажать кнопку отменить заказ
    cancel_order_button = page.get_by_text("Отменить заказ", exact=True)
    cancel_order_button.click()
    page.wait_for_timeout(1500)