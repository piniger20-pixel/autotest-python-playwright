import pytest
from playwright.sync_api import Page
from pathlib import Path
import utils.common_steps as steps
import utils.business_steps as biz
import allure
import logging
from config import EMPLOYEE_EMAIL

log = logging.getLogger(__name__)


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.critical
@pytest.mark.order_creation
@allure.feature("Orders")
@allure.story("basic default condition template")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("БШУ по умолчанию")
@allure.description("""
Тест проверяет:
1. Включение фильтров ШУ
2. Удаление старых БШУ из списка                    
3. Создание БШУ
4. Проверка подстановки условий на форме создания
5. Проверить условия БШУ в детализации заказа                    
6. Удаление БШУ
""")
def test_basic_conditions_template_v_default(chromium_page: Page):
    """Тест БШУ по умолчанию"""
    page = chromium_page
    
    base_dir = Path(__file__).parent.parent
    file_path = base_dir / "testdata" / "test_basic_conditions_template_v_default_TestQaOrg.xlsm"
    
    # Переменные для отслеживания статуса теста
    failed_checks = []
    template_id = None
    trans_id = None

    with allure.step("Шаг 1: Авторизация"):
        steps.login(page, EMPLOYEE_EMAIL)

    with allure.step("Шаг 2: Подготовка - удаление старых БШУ"):
        biz.cleanup_old_templates(page, org_name="Test qa org")

    with allure.step("Шаг 3: Создание и активация БШУ"):
        template_id, trans_id = biz.create_default_basic_template(
            page,
            org_name="Test qa org",
            doc_days="100",
            payment_days="200"
        )

    with allure.step("Шаг 4: Загрузка заказа через Excel и проверка переменных шаблона"):
        variables_check = biz.upload_order_and_verify_template_variables(
            page,
            file_path=file_path,
            expected_trans_id=trans_id,
            expected_doc_delay="100",
            expected_payment_delay="200"
        )
        
        if not variables_check:
            failed_checks.append("Проверка переменных шаблона через API")

    with allure.step("Шаг 5: Проверка значений шаблона в форме"):
        form_checks = steps.verify_template_in_order_form(
            page,
            expected_doc_delay="100",
            expected_payment_delay="200"
        )
        
        if not form_checks:
            failed_checks.append("Проверка данных на странице создания заказа")

    with allure.step("Шаг 6: Создание заказов из Excel"):
        order_ids = steps.create_orders_from_file(page)
        
        if not order_ids:
            failed_checks.append("Создание заказов из файла")
            pytest.fail("Не удалось создать заказы из файла")

    with allure.step("Шаг 7: Переход к таблице заказов и фильтрация"):
        steps.open_forwarder_orders(page)
        page.wait_for_timeout(5000)
        steps.close_filters(page)
        page.wait_for_timeout(2000)
        steps.filter_by(page, "ID заказа", order_ids[0])
        page.reload()
        page.wait_for_load_state('load')

    with allure.step("Шаг 8: Проверка БШУ в детализации заказа"):
        details_check = biz.verify_template_in_order_details_flow(page)
        
        if not details_check:
            failed_checks.append("Проверка группировки элементов в детализации заказа")

    with allure.step("Шаг 9: Удаление БШУ"):
        steps.navigate_to_templates_page(page)
        deletion_success = steps.delete_template_by_id(page, template_id)
        
        if not deletion_success:
            failed_checks.append("Проверка удаления шаблона")

    # Финальная проверка статуса теста
    if failed_checks:
        print(f"\n❌ ТЕСТ ЗАВЕРШЕН С ОШИБКАМИ. Непройденные проверки:")
        for check in failed_checks:
            print(f"   - {check}")
        pytest.fail(f"Тест завершен с непройденными проверками: {', '.join(failed_checks)}")
    else:
        print("\n✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО!")


if __name__ == "__main__":
    log.setLevel(logging.DEBUG)
    test_basic_conditions_template_v_default()