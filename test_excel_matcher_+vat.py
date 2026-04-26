import pytest
from playwright.sync_api import Page
from pathlib import Path
import allure
from config import EMPLOYEE_EMAIL
import logging

import utils.common_steps as steps
import utils.business_steps as business

log = logging.getLogger(__name__)


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.critical
@pytest.mark.order_flow
@allure.feature("Orders")
@allure.story("Matcher")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Excel заказ с механиками торгов: не выше заявленной, только на понижение, шаг торгов, ставки с НДС и без НДС")
@allure.description("""
Проверка на excel заказе механик торгов и валидации их ошибок:
- Не выше заявленной стоимости
- Только на понижение
- Шаг торгов
- Использование ставок с НДС и без НДС
- Проверка заявленной стоимости с НДС в детализации торгов исполнителя
""")
def test_excel_matcher_vat(chromium_page: Page):
    """
    Тест проверяет механики торгов при работе с заказом из Excel файла.
    
    Сценарий:
    1. Создание заказа из Excel и переход к торгам
    2. Проверка механик торгов и открытие окна ставки
    3. Валидация всех механик торгов (не выше заявленной, шаг торгов)
    4. Создание ставки с НДС
    5. Проверка механики "Только на понижение" и создание ставки без НДС
    6. Завершение торгов выбором победителя
    """
    page = chromium_page

    # Подготовка пути к тестовым данным
    base_dir = Path(__file__).parent.parent
    file_path = base_dir / "testdata" / "excel_matcher_+vat.xlsm"
   
    # Шаг 1: Создание заказа из Excel и переход к торгам
    order_ids = business.create_order_from_excel_and_open_auction(
        page, 
        file_path, 
        EMPLOYEE_EMAIL
    )

    # Шаг 2: Проверка механик торгов и открытие окна ставки
    expected_mechanics = {"Закрытые торги", "Только на понижение", "Не выше заявленной"}
    business.verify_auction_mechanics_and_open_bet(
        page, 
        expected_mechanics=expected_mechanics,
        amount_no_vat="10 000",
        amount_with_vat="12 000",
        vat_rate="20%",
        org_name="Autotests_GP_НДС"
    )

    # Шаг 3: Проверка всех механик валидации
    business.validate_all_auction_mechanics(page)

    # Шаг 4: Создание ставки с НДС
    business.make_and_verify_bet_with_vat(
        page,
        amount="5000",
        amount_display="5 000",
        amount_with_vat="6 000",
        vat_amount="1 000",
        vat_rate="20%"
    )

    # Шаг 5: Проверка механики "Только на понижение" и создание ставки без НДС
    business.validate_decrease_and_make_bet_without_vat(
        page,
        org_name="Autotests_GP_БезНДС",
        invalid_amount="7000",
        valid_amount="3000",
        amount_display="3 000"
    )

    # Шаг 6: Завершение торгов выбором победителя
    business.complete_auction_with_winner(page, order_ids[0])


if __name__ == "__main__":
    log.setLevel(logging.DEBUG)
    test_excel_matcher_vat()