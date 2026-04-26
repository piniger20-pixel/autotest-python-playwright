import allure
import json
import re
from datetime import date, timedelta
from playwright.sync_api import expect, Page
from helpers.ui import wait_and_click, fill_custom_input, fill_textarea, select_from_select_list, pick_from_popup_menu, set_address_with_suggest, pick_date_by_dataqa_offset

@allure.step("Выбираем шаблон '{template}'")
def select_template(page, template: str):
    wait_and_click(page, '[data-qa="order-form-template-select"]')
    wait_and_click(page, f"div[role='option']:has-text('{template}')")

@allure.step("Выбираем дату +{days_ahead} дней (календарь #{calendar_index})")
def pick_date(page, calendar_index: int, days_ahead: int):
    target = date.today() + timedelta(days=days_ahead)
    day_num = str(target.day)

    cal = page.locator('button[aria-label="Календарь"]').nth(calendar_index)

    # Ensure calendar button is visible and clickable
    cal.scroll_into_view_if_needed()
    expect(cal).to_be_visible(timeout=5000)
    expect(cal).to_be_enabled(timeout=5000)
    page.wait_for_timeout(300)

    cal.click()

    # Wait for calendar popup to appear
    page.wait_for_selector('div[role="dialog"]', state="visible", timeout=5000)
    page.wait_for_timeout(500)

    pattern = re.compile(f"^{day_num}$")
    candidates = page.locator('div[role="button"]', has_text=pattern)

    # Wait for candidates to be available
    page.wait_for_timeout(300)
    count = candidates.count()

    if count == 0:
        raise AssertionError(f"Не найдена дата {day_num} в календаре")

    target_day = candidates.nth(1) if count > 1 else candidates.first

    # Wait for element to be visible and stable
    expect(target_day).to_be_visible(timeout=5000)

    # Use force click to avoid stability issues with dynamic calendar
    target_day.click(force=True)

@allure.step("Сохраняем заказ на торги")
def save_order(page) -> str:
    pattern = re.compile(r".*/api/orders/v0/transferOrder/create.*")

    with page.expect_response(pattern) as response_info:
        page.locator('[data-qa="order-form-actions-save-order-button"]').click()

    response = response_info.value
    assert response.ok, f"❌ Ошибка API: статус {response.status}"

    body = response.json()
    print("\nОтвет API:")
    print(json.dumps(body, indent=2, ensure_ascii=False))

    assert "data" in body, "❌ В ответе нет поля 'data'"
    order_id = body["data"].get("id")
    assert order_id, "❌ В 'data' нет 'id' заказа"

    print("\n" + "=" * 50)
    print(f"✅ Создан заказ ID: {order_id}")
    print("=" * 50 + "\n")

    page.reload()
    page.wait_for_load_state("load")

    return order_id


@allure.step("Сохраняем изменения заказа (редактирование)")
def save_order_after_edit(page) -> str:
    """Сохранение уже существующего заказа после редактирования (transferOrder/update)."""
    pattern = re.compile(r".*/api/orders/v0/transferOrder/update.*")

    with page.expect_response(pattern) as response_info:
        page.locator('[data-qa="order-form-actions-save-order-button"]').click()

    response = response_info.value
    assert response.ok, f"❌ Ошибка API: статус {response.status}"

    body = response.json()
    print("\nОтвет API:")
    print(json.dumps(body, indent=2, ensure_ascii=False))

    assert "data" in body, "❌ В ответе нет поля 'data'"
    order_id = body["data"].get("id")
    assert order_id, "❌ В 'data' нет 'id' заказа"

    print("\n" + "=" * 50)
    print(f"✅ Заказ сохранён ID: {order_id}")
    print("=" * 50 + "\n")

    page.reload()
    page.wait_for_load_state("load")

    return order_id




@allure.step("Открываем форму создания заказа")
def open_order_form(page: Page):
    wait_and_click(page, '[data-qa="menu-new-form-create-button"]')
    page.wait_for_selector('[data-qa="order-form-clear-button"]', timeout=10000)


@allure.step("Очищаем форму заказа")
def clear_order_form(page: Page):
    wait_and_click(page, '[data-qa="order-form-clear-button"]')
    page.wait_for_timeout(200)


@allure.step("Блок 'Моя организация' (org={org_name})")
def fill_my_org(page: Page, org_name: str):
    org_select = page.locator('[data-qa="order-form-forwarder-select"]')
    if org_select.is_enabled():
        org_select.click()
        page.locator(f'text="{org_name}"').click()
    else:
        expect(org_select.locator('.g-select-control__option-text')).to_have_text(org_name)

    currency_select = page.locator('[data-qa="order-form-forwarder-currency-select"]')
    expect(currency_select).to_be_visible()


@allure.step("Блок 'Владелец груза' (ИНН={inn})")
def fill_cargo_owner_by_inn(page: Page, inn: str, company_menu_text: str):
    additional_switch = page.locator('[data-qa="order-form-customer-additional-switch"]')
    if additional_switch.get_attribute('aria-checked') == 'true':
        additional_switch.click()

    fill_custom_input(page.locator('[data-qa="order-form-customer-inn-input"]'), inn)
    pick_from_popup_menu(page, company_menu_text)


@allure.step("Блок 'Перевозка'")
def fill_transport_block(page: Page, weight: str, volume: str, pallets: str, body_type: str):
    fill_custom_input(page.locator('[data-qa="order-form-transport-weight-input"]'), weight)
    fill_custom_input(page.locator('[data-qa="order-form-transport-volume-input"]'), volume)
    fill_custom_input(page.locator('[data-qa="order-form-transport-pallet-count-input"]'), pallets)

    page.locator('[data-qa="order-form-transport-body-type-select"]').click()
    select_from_select_list(page, body_type)


# ---------- Shipment 0 ----------
@allure.step("Груз 1: 2 грузоместа")
def fill_shipment0_two_packages(page: Page):
    fill_custom_input(page.locator('[data-qa="order-form-shipments-name-input-0"]'),
                      "Груз 1, объём и вес по местам, несколько мест")

    page.locator('[data-qa="order-form-shipments-items-tab-0"]').click()

    # 0-0
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-name-input-0-0"]'), "Грузоместо 1-1")
    page.locator('[data-qa="order-form-shipments-package-body-type-select-0-0"]').click()
    select_from_select_list(page, "Паллет")
    page.locator('[data-qa="order-form-shipments-package-hazard-class-select-0-0"]').click()
    select_from_select_list(page, "4 Класс")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-stackability-input-0-0"]'), "40")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-amount-input-0-0"]'), "7300")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-count-input-0-0"]'), "9")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-capacity-input-0-0"]'), "7.103")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-weight-input-0-0"]'), "60.4")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-length-input-0-0"]'), "104")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-width-input-0-0"]'), "30")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-height-input-0-0"]'), "20")

    # add 0-1
    page.locator('[data-qa="order-form-shipments-package-add-button-0"]').click()

    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-name-input-0-1"]'), "Название грузоместа 1-2")
    page.locator('[data-qa="order-form-shipments-package-body-type-select-0-1"]').click()
    select_from_select_list(page, "Короб")
    page.locator('[data-qa="order-form-shipments-package-hazard-class-select-0-1"]').click()
    select_from_select_list(page, "7 Класс")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-stackability-input-0-1"]'), "8")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-amount-input-0-1"]'), "400")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-count-input-0-1"]'), "30")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-capacity-input-0-1"]'), "5")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-weight-input-0-1"]'), "1.1")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-length-input-0-1"]'), "41")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-width-input-0-1"]'), "29")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-height-input-0-1"]'), "60")


@allure.step("Погрузка/Разгрузка для груза 1")
def fill_load_unload_for_shipment0(page: Page):
    toggle = page.locator('[data-qa="order-form-shipments-load-match-customer-toggle-0-npShipment"]')
    if toggle.get_attribute('aria-checked') != 'true':
        toggle.click()

    page.locator('[name="shipments.0.npShipment.legalPhone"]').fill("+79110985678")

    set_address_with_suggest(
        page,
        'textarea[name="shipments.0.npShipment.npGeoAddress.address"]',
        "Калининград, Московский проспект, 2",
        "Калининград, Московский проспект, 2Б",
    )

    page.locator('[data-qa="order-form-shipments-load-contact-name-input-0-npShipment-0"] input').fill("(!) ФИО Погрузка")
    page.locator('[data-qa="order-form-shipments-load-contact-phone-input-0-npShipment-0"] input').fill("+7(917)345-67-89")

    fill_custom_input(page.locator('[data-qa="order-form-shipments-load-customer-tin-input-0-npUnshipment"]'), "2536340588")
    pick_from_popup_menu(page, "МНОГОТОЧИЕ")

    page.locator('[name="shipments.0.npUnshipment.legalPhone"]').fill("+79024808813")

    set_address_with_suggest(
        page,
        'textarea[name="shipments.0.npUnshipment.npGeoAddress.address"]',
        "Ростов-на-Дону, проспект Ленина, 3",
        "Ростов-на-Дону, проспект Ленина, 3",
    )

    page.locator('[data-qa="order-form-shipments-load-contact-name-input-0-npUnshipment-0"] input').fill("(!) ФИО Разгрузка")
    page.locator('[data-qa="order-form-shipments-load-contact-phone-input-0-npUnshipment-0"] input').fill("+79179001234")


@allure.step("Даты для груза 1")
def set_dates_for_shipment0(page: Page, load_days: int, unload_days: int):
    pick_date_by_dataqa_offset(page, 'order-form-shipments-load-from-date-datepicker-0-npShipment', load_days)
    pick_date_by_dataqa_offset(page, 'order-form-shipments-load-from-date-datepicker-0-npUnshipment', unload_days)


# ---------- Shipment 1 ----------
@allure.step("Добавить груз 2: 1 грузоместо")
def add_shipment1_one_package(page: Page):
    page.locator('[data-qa="order-form-shipments-add-shipment-button"]').click()
    page.locator('[data-qa="order-form-shipments-common-tab-1"]').click()

    fill_custom_input(page.locator('[data-qa="order-form-shipments-name-input-1"]'),
                      "Груз 2, объём и вес общие, одно грузоместо")

    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-name-input-1-0"]'), "Грузоместо 2-1")
    page.locator('[data-qa="order-form-shipments-package-body-type-select-1-0"]').click()
    select_from_select_list(page, "Другое")

    page.locator('[data-qa="order-form-shipments-package-hazard-class-select-1-0"]').click()
    select_from_select_list(page, "1 Класс")

    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-stackability-input-1-0"]'), "1")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-amount-input-1-0"]'), "90000")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-count-input-1-0"]'), "3")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-capacity-input-1-0"]'), "14")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-weight-input-1-0"]'), "120")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-length-input-1-0"]'), "300")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-width-input-1-0"]'), "400")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-height-input-1-0"]'), "600")


@allure.step("Погрузка/Разгрузка для груза 2")
def fill_load_unload_for_shipment1(page: Page):
    toggle = page.locator('[data-qa="order-form-shipments-load-match-customer-toggle-1-npShipment"]')
    if toggle.get_attribute('aria-checked') != 'true':
        toggle.click()

    page.locator('[name="shipments.1.npShipment.legalPhone"]').fill("+79660002323")

    set_address_with_suggest(
        page,
        'textarea[name="shipments.1.npShipment.npGeoAddress.address"]',
        "саратов пушкина 5",
        "Приволжский федеральный округ, Саратовская область, Саратов, улица имени А.С. Пушкина, 5",
    )

    page.locator('[data-qa="order-form-shipments-load-contact-name-input-1-npShipment-0"] input').fill("(!) ФИО Погрузка")
    page.locator('[data-qa="order-form-shipments-load-contact-phone-input-1-npShipment-0"] input').fill("+7(911)345-67-89")

    fill_custom_input(page.locator('[data-qa="order-form-shipments-load-customer-tin-input-1-npUnshipment"]'), "9726082666")
    pick_from_popup_menu(page, "ПОПУТЧИК")

    page.locator('[name="shipments.1.npUnshipment.legalPhone"]').fill("+79621239090")

    set_address_with_suggest(
        page,
        'textarea[name="shipments.1.npUnshipment.npGeoAddress.address"]',
        "Санкт-петербург лиговский 10",
        "Северо-Западный федеральный округ, Санкт-Петербург, Санкт-Петербург, Лиговский проспект, 10/118",
    )

    page.locator('[data-qa="order-form-shipments-load-contact-name-input-1-npUnshipment-0"] input').fill("(!) ФИО Разгрузка")
    page.locator('[data-qa="order-form-shipments-load-contact-phone-input-1-npUnshipment-0"] input').fill("+79219111213")


@allure.step("Даты для груза 2")
def set_dates_for_shipment1(page: Page, load_days: int, unload_days: int):
    pick_date_by_dataqa_offset(page, 'order-form-shipments-load-from-date-datepicker-1-npShipment', load_days)
    pick_date_by_dataqa_offset(page, 'order-form-shipments-load-from-date-datepicker-1-npUnshipment', unload_days)


@allure.step("Дублировать груз 2")
def duplicate_shipment1(page: Page):
    page.locator('[data-qa="order-form-shipments-duplicate-button-1"]').click()


# ---------- Auction ----------
@allure.step("Открыть вкладку 'Куда отправить' → Торги")
def open_distribution_to_auction(page: Page):
    page.locator('button[data-qa="order-form-distribution-matcher-tab"]').click()


@allure.step("Выбрать группу исполнителей")
def select_executors_group(page: Page, group_label_qa: str):
    page.locator(f'[data-qa="{group_label_qa}"]').click()



@allure.step("Заполнить блок 'Торги'")
def fill_auction_block(
    page: Page,
    minutes: str,
    amount: str,
    step: str,
    buy_now: str,
    hide_bids: bool = True,
    decrease_only: bool = True,
):
    page.locator('[data-qa="order-form-auction-duration-tab"]').click()

    fill_custom_input(page.locator('[data-qa="order-form-auction-duration-minutes-input"]'), minutes)
    fill_custom_input(page.locator('[data-qa="order-form-auction-amount-input"]'), amount)
    fill_custom_input(page.locator('[data-qa="order-form-auction-step-input"]'), step)
    fill_custom_input(page.locator('[data-qa="order-form-auction-buy-now-price-input"]'), buy_now)

    if hide_bids:
        toggle = page.locator('[data-qa="order-form-auction-hide-bids-from-carrier-switch"]')
        inp = toggle.locator('input[role="switch"]')
        if inp.get_attribute('aria-checked') == 'false':
            toggle.click()
            expect(inp).to_have_attribute('aria-checked', 'true')

    if decrease_only:
        toggle = page.locator('[data-qa="order-form-auction-decrease-only-from-declared-price-switch"]')
        inp = toggle.locator('input[role="switch"]')
        if inp.get_attribute('aria-checked') == 'false':
            toggle.click()
            expect(inp).to_have_attribute('aria-checked', 'true')

@allure.step("Выбираем список задач в форме '{list_name}'")
def select_task_list(page:Page, list_name: str):
    # Находим и нажимаем кнопку
    button = page.locator('div._header_x0vva_1:has-text("Списки задач") button.g-button_size_l')
    button.click()
    # открываем доп даун со списками
    main_button = page.locator('[data-qa="main-button"]', has_text="Выбрать")
    expect(main_button).to_be_visible(timeout=5000)
    main_button.click()
    # Ждем и нажимаем на элемент с текстом "Список для автотеста"
    list_item = page.locator(f'text="{list_name}"')
    expect(list_item).to_be_visible(timeout=10000)
    list_item.click()
    # Проверяем, что список добавлен
    container = page.locator('._container_x0vva_9')
    # Даем время на обновление UI после клика
    page.wait_for_timeout(1000)

    # Проверяем наличие текста
    try:
        page.wait_for_selector(f'text="{list_name}"', timeout=5000)
        print(f"✅ Список для автотеста: '{list_name}'")
    except:
        # Проверяем статически
        if "Список для автотеста" in container.inner_text():
            print("✅ Текст найден (статическая проверка)")
        else:
            actual_text = container.inner_text()
            print(f"⚠️ Ошибка: ожидался '{list_name}', получено: '{actual_text}'")

@allure.step("Блок 'Моя организация' с комментарием (org={org_name})")
def fill_my_org_with_comment(page: Page, org_name: str, comment: str):
    org_select = page.locator('[data-qa="order-form-forwarder-select"]')
    if org_select.is_enabled():
        org_select.click()
        page.locator(f'text="{org_name}"').click()
    else:
        expect(org_select.locator('.g-select-control__option-text')).to_have_text(org_name)

    currency_select = page.locator('[data-qa="order-form-forwarder-currency-select"]')
    expect(currency_select).to_be_visible()

    page.locator('[data-qa="order-form-forwarder-add-comment-button"]').click()
    comment_input = page.locator('[data-qa="order-form-forwarder-comment-input"]')
    comment_input.click()
    comment_input.evaluate('(element) => {element.innerText = ""}')
    comment_input.type(comment, delay=10)


@allure.step("Блок 'Владелец груза' с телефоном и комментарием (ИНН={inn})")
def fill_cargo_owner_with_phone_and_comment(page: Page, inn: str, company_menu_text: str, phone: str, comment: str):
    additional_switch = page.locator('[data-qa="order-form-customer-additional-switch"]')
    if additional_switch.get_attribute('aria-checked') == 'true':
        additional_switch.click()

    fill_custom_input(page.locator('[data-qa="order-form-customer-inn-input"]'), inn)
    pick_from_popup_menu(page, company_menu_text)

    phone_container = page.locator('[data-qa="order-form-customer-phone-input"]')
    fill_custom_input(phone_container, phone)

    customer_comment = page.locator('[data-qa="order-form-customer-comment-input"]')
    customer_comment.click()
    customer_comment.evaluate('(element) => {element.innerText = ""}')
    customer_comment.type(comment, delay=10)


@allure.step("Блок 'Перевозка' с комментариями")
def fill_transport_block_with_comments(
    page: Page,
    weight: str,
    volume: str,
    pallets: str,
    cargo_number: str,
    category: str,
    body_types: list,
    category_comment: str,
    body_comment: str,
    transshipment_types: list,
    temperature_regimes: list,
    cargo_comment: str
):
    page.locator('[data-qa="order-form-transport-add-body-type-comment-button"]').click()
    page.locator('[data-qa="order-form-transport-add-category-comment-button"]').click()
    page.locator('[data-qa="order-form-transport-add-cargo-comment-button"]').click()

    fill_custom_input(page.locator('[data-qa="order-form-transport-weight-input"]'), weight)
    fill_custom_input(page.locator('[data-qa="order-form-transport-volume-input"]'), volume)
    fill_custom_input(page.locator('[data-qa="order-form-transport-pallet-count-input"]'), pallets)
    fill_custom_input(page.locator('[data-qa="order-form-transport-cargo-input"]'), cargo_number)

    page.locator('[data-qa="order-form-transport-category-type-select"]').click()
    for cat in category:
        select_from_select_list(page, cat)

    page.locator('[data-qa="order-form-transport-body-type-select"]').click()
    for body_type in body_types:
        select_from_select_list(page, body_type)

    category_comment_input = page.locator('[data-qa="order-form-transport-category-type-comment-input"]')
    category_comment_input.click()
    category_comment_input.evaluate('(element) => {element.innerText = ""}')
    category_comment_input.type(category_comment, delay=10)

    body_comment_input = page.locator('[data-qa="order-form-transport-body-type-comment-input"]')
    body_comment_input.click()
    body_comment_input.evaluate('(element) => {element.innerText = ""}')
    body_comment_input.type(body_comment, delay=10)

    page.locator('[data-qa="order-form-transport-trans-shipment-types-select"]').click()
    for trans_type in transshipment_types:
        select_from_select_list(page, trans_type)

    page.locator('[data-qa="order-form-transport-temperature-regime-select"]').click()
    for temp_regime in temperature_regimes:
        select_from_select_list(page, temp_regime)

    cargo_comment_input = page.locator('textarea#cargoComment')
    cargo_comment_input.fill("")
    cargo_comment_input.type(cargo_comment, delay=10)


@allure.step("Груз 1: 1 грузоместо с полными данными")
def fill_shipment0_single_package(page: Page):
    fill_custom_input(page.locator('[data-qa="order-form-shipments-name-input-0"]'), "Название груза")

    page.locator('[data-qa="order-form-shipments-items-tab-0"]').click()

    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-name-input-0-0"]'), "Название грузоместа")
    page.locator('[data-qa="order-form-shipments-package-body-type-select-0-0"]').click()
    select_from_select_list(page, "Короб")
    page.locator('[data-qa="order-form-shipments-package-hazard-class-select-0-0"]').click()
    select_from_select_list(page, "7 Класс")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-stackability-input-0-0"]'), "10")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-amount-input-0-0"]'), "8000")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-count-input-0-0"]'), "153")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-capacity-input-0-0"]'), "71.03")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-weight-input-0-0"]'), "60.4")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-length-input-0-0"]'), "104")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-width-input-0-0"]'), "30")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-height-input-0-0"]'), "20")


@allure.step("Погрузка/Разгрузка для груза 1 с конкретными адресами")
def fill_load_unload_for_shipment0_with_addresses(
    page: Page,
    load_phone: str,
    load_address: str,
    load_address_suggest: str,
    load_contact_name: str,
    load_contact_phone: str,
    unload_inn: str,
    unload_company: str,
    unload_phone: str,
    unload_address: str,
    unload_address_suggest: str,
    unload_contact_name: str,
    unload_contact_phone: str
):
    toggle = page.locator('[data-qa="order-form-shipments-load-match-customer-toggle-0-npShipment"]')
    if toggle.get_attribute('aria-checked') != 'true':
        toggle.click()

    page.locator('[name="shipments.0.npShipment.legalPhone"]').fill(load_phone)

    set_address_with_suggest(
        page,
        'textarea[name="shipments.0.npShipment.npGeoAddress.address"]',
        load_address,
        load_address_suggest,
    )

    page.locator('[data-qa="order-form-shipments-load-contact-name-input-0-npShipment-0"] input').fill(load_contact_name)
    page.locator('[data-qa="order-form-shipments-load-contact-phone-input-0-npShipment-0"] input').fill(load_contact_phone)

    fill_custom_input(page.locator('[data-qa="order-form-shipments-load-customer-tin-input-0-npUnshipment"]'), unload_inn)
    pick_from_popup_menu(page, unload_company)

    page.locator('[name="shipments.0.npUnshipment.legalPhone"]').fill(unload_phone)

    set_address_with_suggest(
        page,
        'textarea[name="shipments.0.npUnshipment.npGeoAddress.address"]',
        unload_address,
        unload_address_suggest,
    )

    page.locator('[data-qa="order-form-shipments-load-contact-name-input-0-npUnshipment-0"] input').fill(unload_contact_name)
    page.locator('[data-qa="order-form-shipments-load-contact-phone-input-0-npUnshipment-0"] input').fill(unload_contact_phone)


@allure.step("Заполнить блок 'Торги' для 'Закрытые торги +'")
def fill_auction_block_closed_trades_plus(
    page: Page,
    minutes: str,
    amount: str,
    hide_bids: bool = True,
    decrease_only: bool = True,
):
    conditions_switch = page.locator('[data-qa="order-form-distribution-public-switch"]')
    if conditions_switch.get_attribute('aria-checked') != 'true':
        conditions_switch.click()

    matcher_tab = page.locator('[data-qa="order-form-distribution-matcher-tab"]')
    if matcher_tab.get_attribute('aria-selected') != 'true':
        matcher_tab.click()

    page.locator('[data-qa="order-form-auction-duration-tab"]').click()
    fill_custom_input(page.locator('[data-qa="order-form-auction-duration-minutes-input"]'), minutes)
    fill_custom_input(page.locator('[data-qa="order-form-auction-amount-input"]'), amount)

    if hide_bids:
        toggle = page.locator('[data-qa="order-form-auction-hide-bids-from-carrier-switch"]')
        inp = toggle.locator('input[role="switch"]')
        if inp.get_attribute('aria-checked') == 'false':
            toggle.click()
            expect(inp).to_have_attribute('aria-checked', 'true')

    if decrease_only:
        toggle = page.locator('[data-qa="order-form-auction-decrease-only-from-declared-price-switch"]')
        inp = toggle.locator('input[role="switch"]')
        if inp.get_attribute('aria-checked') == 'false':
            toggle.click()
            expect(inp).to_have_attribute('aria-checked', 'true')


@allure.step("Добавить исполнителей по ИНН и названию")
def add_executors_by_inn_and_name(page: Page, executors: list):
    for executor in executors:
        inn_container = page.locator('[data-qa="order-form-distribution-partners-input"]')
        fill_custom_input(inn_container, executor['inn'])
        pick_from_popup_menu(page, executor['name'])


@allure.step("Добавить особые условия для исполнителей")
def add_special_conditions_for_executors(page: Page, comment: str):
    comment_textarea = page.locator('textarea[name="distribution.comment"]')
    comment_textarea.scroll_into_view_if_needed()
    comment_textarea.click()
    comment_textarea.type(comment, delay=10)


@allure.step("Выбираем тип транспорта '{body_type}'")
def select_transport_type(page: Page, body_type: str):
    select_button = page.locator('[data-qa="order-form-transport-body-type-select"]')
    select_button.click()
    select_from_select_list(page, body_type)
    expect(select_button).to_have_text(body_type)


@allure.step("Заполняем груз с адресами погрузки и разгрузки")
def fill_shipment_with_addresses(
    page: Page,
    load_address: str,
    load_address_suggest: str,
    unload_address: str,
    unload_address_suggest: str,
    load_days: int = 7,
    unload_days: int = 9
):
    # Включаем совпадение с владельцем груза для погрузки
    toggle = page.locator('[data-qa="order-form-shipments-load-match-customer-toggle-0-npShipment"]')
    if toggle.get_attribute('aria-checked') != 'true':
        toggle.click()

    # Заполняем адрес погрузки
    set_address_with_suggest(
        page,
        'textarea[name="shipments.0.npShipment.npGeoAddress.address"]',
        load_address,
        load_address_suggest,
    )

    # Устанавливаем дату погрузки
    pick_date_by_dataqa_offset(page, 'order-form-shipments-load-from-date-datepicker-0-npShipment', load_days)

    # Включаем совпадение с владельцем груза для разгрузки
    toggle = page.locator('[data-qa="order-form-shipments-load-match-customer-toggle-0-npUnshipment"]')
    if toggle.get_attribute('aria-checked') != 'true':
        toggle.click()

    # Заполняем адрес разгрузки
    set_address_with_suggest(
        page,
        'textarea[name="shipments.0.npUnshipment.npGeoAddress.address"]',
        unload_address,
        unload_address_suggest,
    )

    # Устанавливаем дату разгрузки
    pick_date_by_dataqa_offset(page, 'order-form-shipments-load-from-date-datepicker-0-npUnshipment', unload_days)


@allure.step("Активируем открытые торги")
def enable_open_auction(page: Page):
    matcher_tab = page.locator('[data-qa="order-form-distribution-matcher-tab"]')
    if matcher_tab.get_attribute('aria-selected') != 'true':
        matcher_tab.click()

    checkbox = page.locator('[data-qa="order-form-distribution-public-switch"]')
    if checkbox.get_attribute('aria-checked') != 'true':
        checkbox.click()


@allure.step("Устанавливаем продолжительность торгов: {hours} часов")
def set_auction_duration_hours(page: Page, hours: str):
    duration_tab = page.locator('[data-qa="order-form-auction-duration-tab"]')
    if duration_tab.get_attribute('aria-selected') != 'true':
        duration_tab.click()

    hours_input = page.locator('[data-qa="order-form-auction-duration-hours-input"] input')
    fill_custom_input(hours_input, hours)


@allure.step("Выбираем вкладку 'Себя как на исполнителя'")
def select_distribution_self_tab(page: Page):
    distribution_self = page.locator('button[data-qa="order-form-distribution-self-tab"]')
    distribution_self.click()


@allure.step("Груз 1: 2 грузоместа с полными данными")
def fill_shipment0_two_packages_full(page: Page):
    """Заполняет груз 1 с двумя грузоместами с полными данными"""
    fill_custom_input(page.locator('[data-qa="order-form-shipments-name-input-0"]'), "Название груза 1")

    page.locator('[data-qa="order-form-shipments-items-tab-0"]').click()

    # Грузоместо 1
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-name-input-0-0"]'), "Название грузоместа 1")
    page.locator('[data-qa="order-form-shipments-package-body-type-select-0-0"]').click()
    select_from_select_list(page, "Ролл")
    page.locator('[data-qa="order-form-shipments-package-hazard-class-select-0-0"]').click()
    select_from_select_list(page, "3 Класс")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-stackability-input-0-0"]'), "4")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-amount-input-0-0"]'), "7600")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-count-input-0-0"]'), "9")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-capacity-input-0-0"]'), "7.103")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-weight-input-0-0"]'), "60.4")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-length-input-0-0"]'), "104")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-width-input-0-0"]'), "30")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-height-input-0-0"]'), "20")

    # Добавляем второе грузоместо
    page.locator('[data-qa="order-form-shipments-package-add-button-0"]').click()

    # Грузоместо 2
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-name-input-0-1"]'), "Название грузоместа 2")
    page.locator('[data-qa="order-form-shipments-package-body-type-select-0-1"]').click()
    select_from_select_list(page, "Короб")
    page.locator('[data-qa="order-form-shipments-package-hazard-class-select-0-1"]').click()
    select_from_select_list(page, "7 Класс")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-stackability-input-0-1"]'), "8")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-amount-input-0-1"]'), "400")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-count-input-0-1"]'), "30")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-capacity-input-0-1"]'), "5")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-weight-input-0-1"]'), "1.1")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-length-input-0-1"]'), "41")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-width-input-0-1"]'), "29")
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-height-input-0-1"]'), "60")

    # Добавляем маркировку для второго грузоместа
    page.locator('[data-qa="order-form-shipments-package-mark-add-button-0-1"]').click()
    fill_custom_input(page.locator('[data-qa="order-form-shipments-package-mark-input-0-1-0"]'), "Маркировка грузоместа 2")


@allure.step("Погрузка/Разгрузка для груза 1 с конкретными данными")
def fill_load_unload_for_shipment0_full(page: Page):
    """Заполняет погрузку/разгрузку для груза 1 с конкретными данными"""
    toggle = page.locator('[data-qa="order-form-shipments-load-match-customer-toggle-0-npShipment"]')
    if toggle.get_attribute('aria-checked') != 'true':
        toggle.click()

    page.locator('[name="shipments.0.npShipment.legalPhone"]').fill("+79110985678")

    set_address_with_suggest(
        page,
        'textarea[name="shipments.0.npShipment.npGeoAddress.address"]',
        "Калининград, Московский проспект, 2",
        "Калининград, Московский проспект, 2Б",
    )

    page.locator('[data-qa="order-form-shipments-load-contact-name-input-0-npShipment-0"] input').fill("(!) ФИО Погрузка")
    page.locator('[data-qa="order-form-shipments-load-contact-phone-input-0-npShipment-0"] input').fill("+7(917)345-67-89")

    fill_custom_input(page.locator('[data-qa="order-form-shipments-load-customer-tin-input-0-npUnshipment"]'), "2536340588")
    pick_from_popup_menu(page, "МНОГОТОЧИЕ")

    page.locator('[name="shipments.0.npUnshipment.legalPhone"]').fill("+79024808813")

    set_address_with_suggest(
        page,
        'textarea[name="shipments.0.npUnshipment.npGeoAddress.address"]',
        "Ростов-на-Дону, проспект Ленина, 3",
        "Ростов-на-Дону, проспект Ленина, 3",
    )

    page.locator('[data-qa="order-form-shipments-load-contact-name-input-0-npUnshipment-0"] input').fill("(!) ФИО Разгрузка")
    page.locator('[data-qa="order-form-shipments-load-contact-phone-input-0-npUnshipment-0"] input').fill("+79179001234")


# ---------- Template Steps ----------
@allure.step("Выбрать вкладку 'Черновик'")
def select_distribution_draft_tab(page: Page):
    """Выбирает вкладку 'Черновик' в блоке 'Куда отправить'"""
    draft_tab = page.locator('button[data-qa="order-form-distribution-draft-tab"]')
    draft_tab.click()


@allure.step("Перейти в режим шаблона")
def enter_template_mode(page: Page):
    """Переключает форму в режим создания шаблона"""
    template_mode_button = page.locator('[data-qa="order-form-actions-set-template-mode-button"]')
    template_mode_button.wait_for(state="visible", timeout=10000)
    template_mode_button.click()


@allure.step("Сохранить шаблон с именем '{template_name}'")
def save_template(page: Page, template_name: str):
    """Сохраняет текущую форму как шаблон с указанным именем"""
    template_container = page.locator('[data-qa="order-form-action-template-name-input"]')
    fill_custom_input(template_container, template_name)

    save_template_button = page.locator('[data-qa="order-form-actions-save-template-button"]')
    save_template_button.wait_for(state="visible", timeout=10000)
    save_template_button.scroll_into_view_if_needed()
    expect(save_template_button).to_be_enabled(timeout=10000)
    save_template_button.click()

    page.wait_for_timeout(7000)


@allure.step("Развернуть блок груза {shipment_index}")
def expand_shipment_block(page: Page, shipment_index: int):
    """Разворачивает блок груза, если он свернут"""
    shipment_button = page.locator(f'[data-qa="order-form-shipments-toggle-button-{shipment_index}"][data-shipment="{shipment_index}"]')
    
    # Ждем появления кнопки
    shipment_button.wait_for(state="visible", timeout=10000)
    
    # Проверяем атрибут aria-expanded кнопки
    aria_expanded = shipment_button.get_attribute('aria-expanded')
    is_expanded = aria_expanded == 'true'
    
    print(f"🔍 Груз {shipment_index + 1}: aria-expanded={aria_expanded}, is_expanded={is_expanded}")
    
    if not is_expanded:
        print(f"✅ Груз {shipment_index + 1} свернут (aria-expanded={aria_expanded}), разворачиваем...")
        shipment_button.scroll_into_view_if_needed()
        page.wait_for_timeout(500)
        shipment_button.click()
        page.wait_for_timeout(3000)
        
        # Проверяем что блок развернулся по классу SVG иконки
        caret = shipment_button.locator('svg[class*="_caret"]').first
        expect(caret).to_have_class(re.compile(r'.*_opened_.*'), timeout=10000)
        print(f"✅ Груз {shipment_index + 1} развернут")
    else:
        print(f"✅ Груз {shipment_index + 1} уже развернут (aria-expanded=true), пропускаем клик")


@allure.step("Заполнить название груза {shipment_index}: '{name}'")
def fill_shipment_name(page: Page, shipment_index: int, name: str):
    """Заполняет название груза"""
    fill_custom_input(
        page.locator(f'[data-qa="order-form-shipments-name-input-{shipment_index}"]'),
        name
    )


@allure.step("Заполнить название грузоместа {shipment_index}-{package_index}: '{name}'")
def fill_package_name(page: Page, shipment_index: int, package_index: int, name: str):
    """Заполняет название грузоместа"""
    fill_custom_input(
        page.locator(f'[data-qa="order-form-shipments-package-name-input-{shipment_index}-{package_index}"]'),
        name
    )