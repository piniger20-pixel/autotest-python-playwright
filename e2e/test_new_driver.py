import pytest
from playwright.sync_api import Page
import allure
from faker import Faker
import logging

import utils.common_steps as steps
import utils.business_steps as biz
from config import EMPLOYEE_EMAIL, ORGANIZATION_NAME

log = logging.getLogger(__name__)
fake = Faker("ru_RU")
fio = fake.name()


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.critical
@pytest.mark.driver_management
@allure.feature("Drivers")
@allure.story("Create new driver")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Создание нового водителя и проверка его в системе")
@allure.description("""
Тест проверяет полный цикл создания водителя:
1. Авторизация в системе
2. Создание водителя с заполнением всех обязательных полей
3. Поиск созданного водителя в списке
""")
def test_driver_creation(chromium_page: Page):
    """
    Тест создания нового водителя:
    - Авторизуется в системе
    - Создает водителя через бизнес-шаг
    - Проверяет наличие водителя в списке
    """
    page = chromium_page
    log.info("Starting test with existing user: %s", EMPLOYEE_EMAIL)
    
    # Шаг 1: Авторизация
    steps.login(page)
    
    # Шаг 2: Создание водителя и проверка
    biz.create_driver_and_verify(
        page=page,
        org_name=ORGANIZATION_NAME,
        fio=fio,
        phone="+7 903 770-66-63",
        inn="44444444444",
        passport_number="1234567890",
        passport_issue="УФМС",
        department_code="076666",
        issue_date="07022000",
        license_number="08 10 202566"
    )
    
    # Логирование успешного завершения
    log.info("="*50)
    print("\n" + "✅ " + "="*44 + " ✅")
    print(f"   ВОДИТЕЛЬ СОЗДАН: {fio}")
    print("✅ " + "="*44 + " ✅\n")
    log.info(f"Водитель '{fio}' успешно создан и найден в списке")
    log.info("="*50)