
import allure
import re
from datetime import date, timedelta
from playwright.sync_api import Page, expect, Locator

def wait_visible(page: Page, selector: str, timeout: int = 5000) -> Locator:
    el = page.locator(selector)
    el.wait_for(state="visible", timeout=timeout)
    return el


def wait_and_click(page: Page, selector: str, timeout: int = 5000) -> Locator:
    el = wait_visible(page, selector, timeout=timeout)
    el.click()
    return el


def wait_enabled(page: Page, selector: str, timeout: int = 15000) -> Locator:
    page.wait_for_selector(f"{selector}:not([disabled])", timeout=timeout)
    el = page.locator(selector)
    assert el.is_enabled(), f"Element is still disabled: {selector}"
    return el

def qa_key(name: str, *suffix) -> str:
    if suffix:
        return f'[data-qa="{name}-{"-".join(map(str, suffix))}"]'
    return f'[data-qa="{name}"]'


@allure.step("Заполнить кастомный input значением {text}")
def fill_custom_input(locator, text: str, delay: int = 10):
    locator.click()
    input_el = locator.locator("input")
    input_el.fill("")
    input_el.type(str(text), delay=delay)

@allure.step("Заполнить textarea значением {text} и Enter")
def fill_textarea(locator, text: str, delay: int = 10):
    locator.click()
    locator.fill("")
    locator.type(text, delay=delay)
    locator.press("Enter")

@allure.step("Выбрать в select-list: {option_text}")
def select_from_select_list(page: Page, option_text: str):
    option = page.locator(
        f'[data-qa="select-list"]:visible [role="option"]:has-text("{option_text}")'
    ).first
    expect(option).to_be_visible(timeout=10000)
    option.click()

@allure.step("Выбрать из popup menu: {menu_item_text}")
def pick_from_popup_menu(page: Page, menu_item_text: str):
    menu = page.locator(".g-popup_open [role='menu']")
    menu.wait_for(state="visible", timeout=10000)
    menu.locator(f'[role="menuitem"]:has-text("{menu_item_text}")').first.click()

@allure.step("Адрес: {query} → выбрать подсказку")
def set_address_with_suggest(page: Page, textarea_selector: str, query: str, suggest_text: str):
    textarea = page.locator(textarea_selector)
    fill_textarea(textarea, query)
    page.wait_for_selector('[role="menuitem"]', state="visible", timeout=15000)
    page.click(f'[role="menuitem"]:has-text("{suggest_text}")')



@allure.step("Выбрать дату по datepicker '{datepicker_dataqa}' offset={days_ahead}d")
def pick_date_by_dataqa_offset(page: Page, datepicker_dataqa: str, days_ahead: int, timeout: int = 15000):
    target = date.today() + timedelta(days=days_ahead)
    day_num = str(target.day)

    # открываем конкретный календарь внутри нужного datepicker
    calendar_btn = page.locator(f'[data-qa="{datepicker_dataqa}"] button[aria-label="Календарь"]')
    calendar_btn.scroll_into_view_if_needed()
    calendar_btn.wait_for(state="visible", timeout=10000)
    expect(calendar_btn).to_be_enabled(timeout=5000)
    page.wait_for_timeout(300)
    calendar_btn.click()

    # Wait for calendar popup to be visible and stable
    page.wait_for_selector('div[role="dialog"]', state="visible", timeout=5000)
    page.wait_for_timeout(500)

    # ищем кнопки дней (используем nth(1) для игнорирования дней из других месяцев)
    target_day = page.locator(
        f'div[role="button"]:has-text("{day_num}")'
    ).filter(has_not=page.locator('.g-date-calendar__button_out-of-boundary'))

    # Wait for candidates to be available
    page.wait_for_timeout(300)

    # Ждем появления кнопки дня
    expect(target_day.first).to_be_visible(timeout=timeout)

    # Use force click to avoid stability issues with dynamic calendar
    target_day.first.click(force=True)

    # Ждем закрытия календаря
    page.wait_for_timeout(500)