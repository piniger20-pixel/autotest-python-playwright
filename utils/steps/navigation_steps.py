import allure
from playwright.sync_api import Page, expect
from helpers.ui import wait_and_click, fill_custom_input, fill_textarea, select_from_select_list, pick_from_popup_menu, set_address_with_suggest, pick_date_by_dataqa_offset

@allure.step("Открываем форму создания заказа")
def open_order_form(page: Page):
    # Дополнительное ожидание стабилизации UI перед открытием формы
    page.wait_for_load_state('load', timeout=30000)
    page.wait_for_timeout(1000)
    
    # Увеличенный таймаут для headless режима
    wait_and_click(page, '[data-qa="menu-new-form-create-button"]', timeout=20000)
    
    # Ждем полной загрузки формы заказа
    page.wait_for_load_state('domcontentloaded', timeout=15000)
    page.wait_for_timeout(1000)
    
@allure.step("Открываем таблицу исполнителя")
def open_executor_orders(page: Page):
    # Небольшая пауза для стабилизации UI перед навигацией
    page.wait_for_timeout(500)
    wait_and_click(page, '[role="menuitem"]:has-text("Исполнитель")', timeout=10000)

@allure.step("Открываем таблицу Заказчика")
def open_forwarder_orders(page: Page):
    # Небольшая пауза для стабилизации UI перед навигацией
    page.wait_for_timeout(500)
    wait_and_click(page, '[role="menuitem"]:has-text("Заказчик")', timeout=10000)
    


@allure.step("Очищаем форму заказа")
def clear_order_form(page: Page):
    wait_and_click(page, '[data-qa="order-form-clear-button"]')
    page.wait_for_timeout(500)


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
def fill_auction_block(page: Page, minutes: str, amount: str, step: str, buy_now: str,
                      hide_bids: bool, decrease_only: bool):
    page.locator('[data-qa="order-form-auction-duration-tab"]').click()

    fill_custom_input(page.locator('[data-qa="order-form-auction-duration-minutes-input"]'), minutes)
    fill_custom_input(page.locator('[data-qa="order-form-auction-amount-input"]'), amount)
    fill_custom_input(page.locator('[data-qa="order-form-auction-step-input"]'), step)
    fill_custom_input(page.locator('[data-qa="order-form-auction-buy-now-price-input"]'), buy_now)

    if hide_bids:
        sw = page.locator('[data-qa="order-form-auction-hide-bids-from-carrier-switch"]').locator('input[role="switch"]')
        if sw.get_attribute('aria-checked') == 'false':
            sw.click()
            expect(sw).to_have_attribute('aria-checked', 'true')

    if decrease_only:
        sw = page.locator('[data-qa="order-form-auction-decrease-only-from-declared-price-switch"]').locator('input[role="switch"]')
        if sw.get_attribute('aria-checked') == 'false':
            sw.click()
            expect(sw).to_have_attribute('aria-checked', 'true')

@allure.step("Открыть детализацию заказа #'{value}'")
def open_details_order(page: Page, value ):
    # Используем более точный селектор с exact match для текста ссылки
    order_link = page.locator(f'a[data-qa="order-link"]:has-text("{value}")').first
    order_link.wait_for(state="visible", timeout=5000)
    order_link.click()

@allure.step("Закрыть детализацию заказа")
def close_details_order(page: Page):
    # Находим заголовок для проверки что детализация открыта
    details_title = page.get_by_text("Детализация заказа").first
    expect(details_title).to_be_visible(timeout=10000)
    
    # Ищем кнопку закрытия с правильными классами
    close_button = page.locator('button.g-button.g-button_view_flat.g-button_size_m.g-button_pin_round-round:has(svg.g-icon)').first
    expect(close_button).to_be_visible(timeout=5000)
    
    # Скроллим к кнопке
    close_button.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    
    # Кликаем с повторными попытками
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            print(f"🔄 Попытка {attempt + 1}/{max_attempts} закрыть детализацию...")
            
            if attempt == 0:
                # Первая попытка - обычный клик
                close_button.click(force=True, timeout=3000)
            else:
                # Последующие попытки - JavaScript клик
                close_button.evaluate("element => element.click()")
            
            print("✅ Клик по кнопке закрытия выполнен")
            
            # Ждем исчезновения детализации
            page.wait_for_timeout(1000)
            
            # Проверяем что детализация действительно закрылась
            expect(details_title).to_be_hidden(timeout=5000)
            print("✅ Детализация успешно закрыта")
            break
            
        except Exception as e:
            if attempt < max_attempts - 1:
                print(f"⚠️ Попытка {attempt + 1} не удалась: {e}")
                page.wait_for_timeout(1000)
            else:
                print(f"❌ Не удалось закрыть детализацию после {max_attempts} попыток")
                # Последняя попытка - нажатие Escape
                print("🔄 Пробуем закрыть через Escape...")
                page.keyboard.press("Escape")
                page.wait_for_timeout(1000)
                
                # Финальная проверка
                try:
                    expect(details_title).to_be_hidden(timeout=5000)
                    print("✅ Детализация закрыта через Escape")
                except:
                    print("❌ Детализация все еще открыта, продолжаем выполнение...")

    # Дополнительный Escape для закрытия возможного модального окна,
    # которое могло появиться после закрытия детализации
    page.wait_for_timeout(500)
    page.keyboard.press("Escape")
    print("🔄 Дополнительный Escape для закрытия возможного модального окна")
    page.wait_for_timeout(1000)
    
    # Дополнительное ожидание для стабилизации UI
    page.wait_for_timeout(2000)

@allure.step("Раскрыть блок комментариев в детализации")
def open_comment_order(page: Page):
    # 1. Находим элемент с текстом "Новые сверху"
        new_comments = page.locator('div.g-box.g-flex:has-text("Новые сверху")').first
        if new_comments.count() == 0:
            # Запасной вариант
            new_comments = page.get_by_text("Новые сверху", exact=True).first
        expect(new_comments).to_be_visible(timeout=10000)
        print("✅ Найден текст 'Новые сверху'")
        # 2. Скроллим к элементу
        new_comments.scroll_into_view_if_needed()
        page.wait_for_timeout(500)
        # 3. Поднимаемся к родительскому контейнеру с классом _header_1afyn_7
        header_container = new_comments.locator('xpath=ancestor::div[contains(@class, "_header_")]').first
        expect(header_container).to_be_visible(timeout=5000)
        # 4. Ищем кнопку в контейнере
        button = header_container.locator('button.g-button.g-button_view_outlined.g-button_size_l.g-button_pin_round-round').first
        # Проверяем что кнопка видима
        expect(button).to_be_visible(timeout=5000)
        # 5. Нажимаем кнопку
        button.click(force=True)
        print("✅ Кнопка раскрытия комментариев нажата")

@allure.step("Показать архивные заказы")
def show_archived_orders(page: Page):
    # Увеличенное ожидание для полного исчезновения overlay после закрытия детализации
    page.wait_for_timeout(1500)
    
    # Находим span с текстом "Архивные"
    archive_span = page.locator('span.g-control-label__text.g-switch__text:has-text("Архивные")').first
    expect(archive_span).to_be_visible(timeout=10000)
    
    # Скроллим к элементу
    archive_span.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    
    # Находим родительский label для доступа к switch
    archive_label = archive_span.locator('xpath=ancestor::label').first
    expect(archive_label).to_be_visible(timeout=5000)
    
    # Находим input switch для проверки состояния
    archive_switch = archive_label.locator('input[role="switch"]').first
    expect(archive_switch).to_be_visible(timeout=5000)
    
    # Проверяем текущее состояние через aria-checked
    is_checked = archive_switch.get_attribute('aria-checked') == 'true'
    
    if not is_checked:
        print("🔄 Переключатель выключен, включаем архивные заказы...")
        
        # Кликаем на span с текстом "Архивные"
        try:
            archive_span.click(force=True, timeout=3000)
            page.wait_for_timeout(1500)
            
            # Проверяем что состояние изменилось
            new_state = archive_switch.get_attribute('aria-checked')
            if new_state == 'true':
                print("✅ Включены архивные заказы")
            else:
                print("⚠️ Состояние не изменилось, пробуем JavaScript")
                archive_span.evaluate("element => element.click()")
                page.wait_for_timeout(1500)
                print("✅ Включены архивные заказы (через JavaScript)")
        except Exception as e:
            print(f"⚠️ Обычный клик не сработал: {e}")
            print("🔄 Используем JavaScript клик на span")
            archive_span.evaluate("element => element.click()")
            page.wait_for_timeout(1500)
            print("✅ Включены архивные заказы (через JavaScript)")
    else:
        print("✅ Архивные заказы уже включены")
    
    # Закрываем модальное окно если оно открыто
    page.wait_for_timeout(500)
    
    # Проверяем наличие модального окна
    modal = page.locator('div.g-modal__content-aligner').first
    if modal.count() > 0:
        print("🔄 Обнаружено модальное окно, закрываем...")
        # Пробуем нажать Escape для закрытия модального окна
        page.keyboard.press("Escape")
        page.wait_for_timeout(1000)
        
        # Проверяем что модальное окно закрылось
        try:
            expect(modal).to_be_hidden(timeout=3000)
            print("✅ Модальное окно закрыто")
        except:
            print("⚠️ Модальное окно все еще открыто, кликаем вне его области")
            # Кликаем в безопасную область (левый верхний угол)
            page.mouse.click(10, 10)
            page.wait_for_timeout(1000)
    
    page.wait_for_timeout(1000)

@allure.step("Скрыть архивные заказы")
def hide_archived_orders(page: Page):
    """
    Выключает переключатель архивных заказов (скрывает архивные заказы).
    """
    # Увеличенное ожидание для полного исчезновения overlay после закрытия детализации
    page.wait_for_timeout(1500)
    
    # Находим span с текстом "Архивные"
    archive_span = page.locator('span.g-control-label__text.g-switch__text:has-text("Архивные")').first
    expect(archive_span).to_be_visible(timeout=10000)
    
    # Скроллим к элементу
    archive_span.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    
    # Находим родительский label для доступа к switch
    archive_label = archive_span.locator('xpath=ancestor::label').first
    expect(archive_label).to_be_visible(timeout=5000)
    
    # Находим input switch для проверки состояния
    archive_switch = archive_label.locator('input[role="switch"]').first
    expect(archive_switch).to_be_visible(timeout=5000)
    
    # Проверяем текущее состояние через aria-checked
    is_checked = archive_switch.get_attribute('aria-checked') == 'true'
    
    if is_checked:
        print("🔄 Переключатель включен, выключаем архивные заказы...")
        
        # Кликаем на span с текстом "Архивные"
        try:
            archive_span.click(force=True, timeout=3000)
            page.wait_for_timeout(1500)
            
            # Проверяем что состояние изменилось
            new_state = archive_switch.get_attribute('aria-checked')
            if new_state == 'false':
                print("✅ Выключены архивные заказы")
            else:
                print("⚠️ Состояние не изменилось, пробуем JavaScript")
                archive_span.evaluate("element => element.click()")
                page.wait_for_timeout(1500)
                print("✅ Выключены архивные заказы (через JavaScript)")
        except Exception as e:
            print(f"⚠️ Обычный клик не сработал: {e}")
            print("🔄 Используем JavaScript клик на span")
            archive_span.evaluate("element => element.click()")
            page.wait_for_timeout(1500)
            print("✅ Выключены архивные заказы (через JavaScript)")
    else:
        print("✅ Архивные заказы уже выключены")
    
    # Закрываем модальное окно если оно открыто
    page.wait_for_timeout(500)
    
    # Проверяем наличие модального окна
    modal = page.locator('div.g-modal__content-aligner').first
    if modal.count() > 0:
        print("🔄 Обнаружено модальное окно, закрываем...")
        # Пробуем нажать Escape для закрытия модального окна
        page.keyboard.press("Escape")
        page.wait_for_timeout(1000)
        
        # Проверяем что модальное окно закрылось
        try:
            expect(modal).to_be_hidden(timeout=3000)
            print("✅ Модальное окно закрыто")
        except:
            print("⚠️ Модальное окно все еще открыто, кликаем вне его области")
            # Кликаем в безопасную область (левый верхний угол)
            page.mouse.click(10, 10)
            page.wait_for_timeout(1000)
    
    page.wait_for_timeout(1000)