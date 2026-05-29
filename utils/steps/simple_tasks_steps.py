import allure
from playwright.sync_api import expect
import json
import re



@allure.step("Выбрать и отменить простую задачу '{lable}'")
def cancel_simple_task(page, lable):
    # Нажимаем "Ускорить" если виден
    accelerate_element = page.locator(f'text="{lable}"').first
    expect(accelerate_element).to_be_visible(timeout=5000)
    accelerate_element.click()
    # Нажимаем "Отменить" если виден
    cancel_button = page.locator('button:has-text("Отменить")')
    expect(cancel_button).to_be_visible(timeout=5000)
    cancel_button.click()