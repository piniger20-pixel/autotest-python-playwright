import allure
from playwright.sync_api import expect
import json
import re
from datetime import date, timedelta
from config import EMPLOYEE_EMAIL, APP_URL
from helpers.ui import wait_and_click


@allure.step("вкл/выкл организацию '{label}'")
def switch_state_of_organization(page, label):
    # Открыть панель организаций
    user_button = page.locator('[data-qa="user-name"]')
    expect(user_button).to_be_visible(timeout=5000)
    user_button.click()
    # Выключить видимость для организации заказчика 
    user_with_text = page.locator(f'[data-qa="user-name"]', has_text=label)
    user_with_text.wait_for(state="visible", timeout=5000)
    user_with_text.click()
    # Перезагрузить страницу
    page.reload()
    page.wait_for_load_state('load')