import allure
from playwright.sync_api import Page
from config import ORGANIZATION_NAME


@allure.step("Открываем раздел 'Моя организация'")
def open_my_organization(page: Page):
    """Открывает раздел 'Моя организация' в меню"""
    page.get_by_text("Моя организация").click()


@allure.step("Открываем раздел 'Водители'")
def open_drivers_section(page: Page):
    """Открывает раздел 'Водители' в меню"""
    page.get_by_text("Водители").click()


@allure.step("Открываем форму создания водителя")
def open_create_driver_form(page: Page):
    """Открывает форму создания нового водителя"""
    page.locator('a[href="/drivers/create"]').click()


@allure.step("Выбираем организацию владельца: {org_name}")
def select_owner_organization(page: Page, org_name: str):
    """Выбирает организацию владельца в форме водителя"""
    org_owner_button = page.locator('button[data-qa="drivers-form-org-owner-select"]:not([disabled])')
    org_owner_button.wait_for(state="visible", timeout=10000)
    org_owner_button.click()
    page.wait_for_selector('[role="listbox"]', timeout=5000)
    option = page.locator('.g-select-list__option-default-label', has_text=org_name)
    option.wait_for(state="visible", timeout=5000)
    option.click()


@allure.step("Выбираем организацию: {org_name}")
def select_organization(page: Page, org_name: str):
    """Выбирает организацию в форме водителя"""
    org_button = page.locator('button[data-qa="drivers-form-orgs-select"]')
    org_button.wait_for(state="visible", timeout=10000)
    org_button.focus()
    org_button.click()
    page.wait_for_selector('[role="listbox"]', timeout=5000)
    option = page.locator('.g-select-list__option-default-label', has_text=org_name)
    option.wait_for(state="visible", timeout=5000)
    option.click()


@allure.step("Заполняем ФИО водителя: {fio}")
def fill_driver_fio(page: Page, fio: str):
    """Заполняет поле ФИО водителя"""
    fio_input = page.get_by_role("textbox", name="Иванов Александр Владимирович")
    fio_input.click()
    fio_input.fill(fio)


@allure.step("Заполняем телефон водителя: {phone}")
def fill_driver_phone(page: Page, phone: str):
    """Заполняет поле телефона водителя"""
    phone_input = page.locator('[data-qa="drivers-form-phone-input"] input')
    phone_input.click()
    phone_input.fill(phone)


@allure.step("Заполняем ИНН водителя: {inn}")
def fill_driver_inn(page: Page, inn: str):
    """Заполняет поле ИНН водителя"""
    page.get_by_role("textbox", name="00 000000 00").click()
    page.get_by_role("textbox", name="00 000000 00").fill(inn)


@allure.step("Заполняем паспортные данные")
def fill_driver_passport(page: Page, passport_number: str, passport_issue: str, 
                        department_code: str, issue_date: str):
    """Заполняет паспортные данные водителя"""
    page.locator('input[name="passport"]').click()
    page.locator('input[name="passport"]').fill(passport_number)
    page.locator('input[name="passportIssue"]').click()
    page.locator('input[name="passportIssue"]').fill(passport_issue)
    page.get_by_role("textbox", name="Код подразделения").click()
    page.get_by_role("textbox", name="Код подразделения").fill(department_code)
    page.get_by_role("group").filter(has_text="Поле должно быть заполнено").get_by_placeholder("Когда выдан").click()
    page.get_by_role("group").filter(has_text="Поле должно быть заполнено").get_by_placeholder("Когда выдан").type(issue_date, delay=50)


@allure.step("Заполняем номер водительского удостоверения: {license_number}")
def fill_driver_license(page: Page, license_number: str):
    """Заполняет номер водительского удостоверения"""
    page.locator('input[name="driverLicense"]').click()
    page.locator('input[name="driverLicense"]').fill(license_number)


@allure.step("Сохраняем водителя")
def save_driver(page: Page):
    """Нажимает кнопку сохранения водителя"""
    page.get_by_role("button", name="Сохранить").click()
    page.wait_for_timeout(1000)


@allure.step("Очищаем поле поиска водителей")
def clear_driver_search(page: Page):
    """Очищает поле поиска в списке водителей"""
    page.locator("#wrapper").get_by_role("combobox").click()
    page.wait_for_timeout(1000)
    clear_button = page.locator('[data-qa="select-clear"]')
    if clear_button.is_visible(timeout=2000):
        clear_button.click()


@allure.step("Ищем водителя по имени: {driver_name}")
def search_driver_by_name(page: Page, driver_name: str):
    """Ищет водителя в списке по имени"""
    page.get_by_role("textbox", name="Поиск по имени").click()
    page.get_by_role("textbox", name="Поиск по имени").fill(driver_name)


@allure.step("Проверяем, что водитель '{driver_name}' отображается в списке")
def assert_driver_in_list(page: Page, driver_name: str):
    """Проверяет наличие водителя в списке"""
    page.wait_for_selector(f"text={driver_name}", timeout=10000)
    assert page.get_by_text(driver_name).is_visible()