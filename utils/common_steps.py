# utils/common_steps.py
# ФАСАД: оставляем внешний интерфейс стабильным для тестов

from utils.steps.auth_steps import login

from utils.steps.cancel_order_steps import (
    cancel_order_by_customer,
    cancel_order_by_executor,
    click_cancel_auction_menu_item,
    click_not_actual_reason_button,
    select_other_reason,
    enter_cancellation_comment,
    confirm_cancel_auction
)

from utils.steps.navigation_steps import (
    open_order_form,
    open_executor_orders,
    open_forwarder_orders,
    open_details_order,
    close_details_order,
    open_comment_order,
    show_archived_orders,
    hide_archived_orders
)

from utils.steps.filters_steps import (
    reset_filters,
    close_filters,
    filter_by,
    set_date_range_filter,
    filter_by_multiple_order_ids,
)

from utils.steps.order_form_steps import (
    select_template,
    pick_date,
    save_order,
    save_order_after_edit,
    select_task_list,
    select_transport_type,
    fill_shipment_with_addresses,
    enable_open_auction,
    set_auction_duration_hours,
    select_distribution_self_tab,
    select_distribution_draft_tab,
    enter_template_mode,
    save_template,
    expand_shipment_block,
    fill_shipment_name,
    fill_package_name,
)

from utils.steps.orders_table_asserts import (
    assert_order_in_table,
    assert_trade_type,
    assert_table_empty,
    assert_any_row_matches,
    assert_any_row_date_matches,
    assert_order_status_in_first_row,
    assert_multiple_orders_in_table,
    assert_order_statuses_present,
    wait_for_order_in_table,
    assert_order_status_by_index,
)

from utils.steps.orders_api_steps import (
    get_executor_order_after_filter,
    get_forwarder_order_after_filter,
    wait_orders_table_reload,
)

from utils.steps.flights_steps import (
    create_flight,
    create_flight_from_bottom_menu,
    delete_flights_cargo,
    type_saveflight_button,
    complete_flight_button,
    open_flight_saidbar_trgouht_bottom_menu,
    add_order_to_ready_flight,
    cancel_flight,
    change_flight_point_status_to_arrived
)

from utils.steps.flights_asserts import (
    assert_flight_in_table,
    assert_order_in_flight,
    assert_multiple_orders_in_flight,
    assert_shipments_in_route,
    open_flight_details,
    close_flight_details,
    assert_flight_status,
)

from utils.steps.order_details_asserts import (
    assert_text_in_order_details,
    assert_cancellation_reason_and_comment,
    open_order_by_status_with_retry,
    assert_order_status_draft_with_retry,
)

from utils.steps.table_steps import (
    select_order_checkbox,
    switch_to_tab,
    open_order_menu,
    disable_table_optimization,
)

from utils.steps.excel_create_orders_steps import (
    create_orders_from_file,
    select_upload_order_from_file,
    upload_file_on_order_form,
)

from utils.steps.order_1x1_steps import accept_offer_1x1_from_table_order

from utils.steps.organization_steps import switch_state_of_organization

from utils.steps.simple_tasks_steps import cancel_simple_task

from utils.steps.drivers_steps import (
    open_my_organization,
    open_drivers_section,
    open_create_driver_form,
    select_owner_organization,
    select_organization,
    fill_driver_fio,
    fill_driver_phone,
    fill_driver_inn,
    fill_driver_passport,
    fill_driver_license,
    save_driver,
    clear_driver_search,
    search_driver_by_name,
    assert_driver_in_list
)

from utils.steps.templates_steps import (
    navigate_to_templates_page,
    apply_template_filters,
    delete_all_filtered_templates,
    create_basic_template,
    verify_template_variables,
    verify_template_in_order_form,
    verify_template_in_order_details,
    delete_template_by_id,
    create_template_with_two_shipments,
    select_template_by_date,
)

from utils.steps.matcher_steps import (
    assert_trade_mechanics_in_table,
    open_bet_window_from_executor_table,
    assert_vat_display_in_bet_window,
    open_bet_form,
    select_organization_for_bet,
    enter_bet_amount,
    assert_bet_validation_errors,
    assert_bet_button_disabled,
    submit_bet,
    assert_best_bet_with_vat,
    assert_best_bet_without_vat,
    assert_bet_not_decrease_error,
    open_auction_window_from_customer_table,
    select_auction_winner,
    confirm_auction_winner,
    cancel_bet_by_executor,
    enter_bet_comment,
    open_replace_bet_form,
    replace_bet,
    reject_bet_by_customer,
    enter_rejection_comment,
    confirm_bet_rejection,
    assert_customer_rejection_comment,
    close_bet_details,
    close_order_details_window,
)

from utils.steps.auction_timer_steps import (
    assert_auction_timer_less_than_60_seconds,
    assert_auction_timer_more_than_60_seconds,
    assert_auction_timer_in_details_more_than_60_seconds,
)

from utils.steps.auction_status_steps import (
    wait_for_auction_status_change,
    wait_for_order_status_change,
    assert_auction_status_in_customer_table,
)

from utils.steps.draft_order_steps import (
    open_order_for_editing,
    switch_to_auction_tab,
    activate_auction_duration,
    set_auction_duration_hours,
    submit_order_to_auction,
    click_buy_now_button,
    buy_order_now,
)

from utils.steps.requirements_steps import (
    enable_requirements_flag,
    open_requirements_table,
    switch_to_drafts_tab,
    expand_requirement_cargo_block,
    expand_specific_requirement_cargo,
    expand_cargo_details,
    assert_requirement_status,
    open_requirement_details,
    assert_requirement_cargo_match_status,
    assert_requirement_cargo_linked_to_order,
    find_requirement_by_id,
    extract_requirement_id_from_response,
    assert_requirement_link_in_order_details,
    perform_action_on_requirement,
    assert_requirement_status_in_details,
)

from utils.steps.lite_order_steps import (
    open_lite_order_form,
    fill_lite_departure_address,
    fill_lite_destination_address,
    fill_lite_cargo_weight,
    toggle_lite_switch,
    fill_lite_cargo_comment,
    fill_lite_price,
    submit_lite_order,
    assert_lite_order_search_status,
)

from utils.steps.lite_bets_steps import (
    get_demand_id_for_order,
    create_bet_via_api,
    assert_lite_order_has_offers_status,
    open_lite_order_details,
    assert_lite_offers_block,
    select_lite_offer,
    assert_lite_carrier_block,
)

# если нужно оставить тут же
from helpers.ui import wait_and_click  # опционально

# import allure
# from playwright.sync_api import expect
# import json
# import re
# from datetime import date, timedelta
# from config import EMPLOYEE_EMAIL
# from helpers.ui import wait_and_click

# from utils import create_order, order_table, draft_order

# @allure.step("Сбросить фильтры")
# def reset_filters(page):

#         reset_button = page.locator('button.g-button:has-text("Сбросить")')
#         reset_button.scroll_into_view_if_needed()
#         expect(reset_button).to_be_visible(timeout=5000)
#         expect(reset_button).to_be_enabled(timeout=5000)
#         reset_button.click()
#         print("✅ Нажата кнопка 'Сбросить'")



# @allure.step("Закрываем все открытые фильтры")
# def close_filters(page):
#                 close_buttons = page.locator('button[data-qa="close-button"]')
#                 page.wait_for_timeout(500)
#                 were_filters_closed = False
#                 while close_buttons.count() > 0:
#                     if close_buttons.first.is_visible():
#                         close_buttons.first.click()
#                         were_filters_closed = True
#                         page.wait_for_timeout(500)
#                     else:
#                         break  # Выходим если кнопка не видима
#                     close_buttons = page.locator('button[data-qa="close-button"]')
#                 if were_filters_closed:
#                    print("✅ Фильтр(ы) закрыты", flush=True)


# @allure.step("Авторизация через insecure endpoint")
# def login(page, email=EMPLOYEE_EMAIL):
#     url = f"https://yamagistrali.tst.yandex.net/api/set_ya_cookie_insecure?tkn={email}"
#     page.goto(url)
#     page.wait_for_load_state("networkidle")
#     page.goto("https://yamagistrali.tst.yandex.net/")
#     page.wait_for_selector("div#wrapper", timeout=15000)

# @allure.step("Открываем форму создания заказа")
# def open_order_form(page):
#     wait_and_click(page, '[data-qa="menu-new-form-create-button"]')

# @allure.step("Выбираем шаблон '{template}'")
# def select_template(page, template):
#     wait_and_click(page, '[data-qa="order-form-template-select"]')
#     wait_and_click(page, f"div[role='option']:has-text('{template}')")
#     page.wait_for_timeout(500)

# @allure.step("Выбираем загрузку заказа из файла")
# def select_upload_order_from_file(page):
#     wait_and_click(page, '[data-qa="order-form-upload-order-from-file-tab"]', 10000)

# @allure.step("Загружаем файл на форме создания заказа")
# def upload_file_on_order_form(page, file_path):
#     with page.expect_file_chooser() as fc_info:
#         wait_and_click(page, '[data-qa="order-form-upload-file-select-file-button"]', 3000)
#         file_chooser = fc_info.value
#         file_chooser.set_files(file_path.absolute())
#         page.wait_for_timeout(1000)

# @allure.step("Выбираем дату +{days_ahead} дней (календарь #{calendar_index})")
# def pick_date(page, calendar_index, days_ahead):
#     target = date.today() + timedelta(days=days_ahead)
#     day_num = str(target.day)

#     # открыть календарь
#     cal = page.locator('button[aria-label="Календарь"]').nth(calendar_index)
#     cal.click()

#     pattern = re.compile(f"^{day_num}$")
#     candidates = page.locator('div[role="button"]', has_text=pattern)

#     # если дата дублируется в разных месяцах — выбираем второй
#     target_day = candidates.nth(1) if candidates.count() > 1 else candidates.first

#     expect(target_day).to_be_visible(timeout=5000)
#     target_day.click()

# @allure.step("Сохраняем заказ на торги")
# def save_order(page):
#     """
#     Кликает кнопку 'Сохранить на торги',
#     ждёт ответ API, валидирует структуру,
#     извлекает order_id и перезагружает страницу.
#     """

#     pattern = re.compile(r".*/api/orders/v0/transferOrder/create.*")

#     # Ждём ответа API
#     with page.expect_response(pattern) as response_info:
#         page.locator('[data-qa="order-form-actions-save-order-button"]').click()

#     response = response_info.value

#     # Проверяем HTTP статус
#     assert response.ok, f"❌ Ошибка API: статус {response.status}"

#     # Загружаем тело ответа
#     body = response.json()

#     print("\nОтвет API:")
#     print(json.dumps(body, indent=2, ensure_ascii=False))

#     # Проверяем структуру тела
#     assert "data" in body, "❌ В ответе нет поля 'data'"
#     order_id = body["data"].get("id")
#     assert order_id, "❌ В 'data' нет 'id' заказа"

#     print("\n" + "=" * 50)
#     print(f"✅ Создан заказ ID: {order_id}")
#     print("=" * 50 + "\n")

#     # Перезагрузить страницу для получения свежего UI состояния
#     page.reload()
#     page.wait_for_load_state("load")

#     return order_id

# @allure.step("Создаем заказ из файла")
# def create_orders_from_file(page):
#     """
#     Кликает кнопку 'Создать заказы из файла',
#     ждёт ответ API, валидирует структуру,
#     извлекает order_ids и перезагружает страницу.
#     """

#     create_orders_button = page.locator('[data-qa="order-form-upload-file-create-orders-button"]')
#     create_orders_button.wait_for(state="visible", timeout=10000)
#     page.wait_for_selector('[data-qa="order-form-upload-file-create-orders-button"]:not([disabled])', timeout=15000)
#     # Проверяем что кнопка активна
#     assert create_orders_button.is_enabled(), "Кнопка создания заказов неактивна"
#     # Собираем ID заказов
#     order_ids = []
#     # Включаем перехватчик ДО нажатия кнопки
#     def collect_order_ids(response):
#         if "createFromXlsx" in response.url:
#             try:
#                 body = response.json()
#                 if "data" in body and "id" in body["data"]:
#                     order_id = body["data"]["id"]
#                     order_ids.append(order_id)
#                     print(f"✅ Заказ #{len(order_ids)}: ID = {order_id}", flush=True)
#             except:
#                 pass  # Игнорируем ошибки парсинга
#     page.on("response", collect_order_ids)
#     create_orders_button.click()
#     print("Нажата кнопка создания заказов из файла", flush=True)
#     # Ждем завершения запросов
#     print("⏳ Ожидаем создание заказов...", flush=True)
#     page.wait_for_timeout(4000)
#     # Отключаем перехватчик
#     page.remove_listener("response", collect_order_ids)
#     print(f"✅ Создано: {len(order_ids)} заказ")
#     # Проверяем что заказы создались
#     if not order_ids:
#         print("❌ Не создано ни одного заказа", flush=True)
#     page.reload()
#     return order_ids

# @allure.step("Открываем таблицу исполнителя")
# def open_executor_orders(page):
#     wait_and_click(page, '[role="menuitem"]:has-text("Исполнитель")')

# @allure.step("Открываем таблицу Заказчика")
# def open_forwarder_orders(page):
#     wait_and_click(page, '[role="menuitem"]:has-text("Заказчик")')


# @allure.step("Применяем фильтр '{label}' со значением '{value}'")
# def filter_by(page, label, value, mode="text_input"):

#     # Открываем панель фильтров
#     filters_button = page.locator("span.g-button__text", has_text="Фильтры")
#     expect(filters_button).to_be_visible(timeout=10000)
#     filters_button.click()

#     # Открываем выпадающий список выбора фильтра
#     dropdown = page.locator('[data-qa="select-popup"]')
#     option = dropdown.get_by_text(
#         label,
#         exact=True
#     )
#     option.click()
#     page.keyboard.press("Escape")

#     # Находим сам фильтр в панели
#     page.locator("div.g-label__content", has_text=label).click()

#     if mode == "text_input":

#         input_field = page.locator("textarea.g-text-area__control, input.g-text-input__control").first
#         input_field.fill(str(value))

#     elif mode == "select_dropdown":
#         # Кликаем по селекту и выбираем значение
#         button = page.locator(
#             f'button.g-select-control__button:has-text("{label}")'
#         )
#         expect(button).to_be_visible(timeout=5000)
#         button.click()

#         option = page.locator("div[role='option']", has_text=str(value)).first
#         expect(option).to_be_visible(timeout=5000)
#         option.click()
#         page.keyboard.press("Escape")

#     # Применить
#     page.get_by_text("Применить", exact=True).click()



# @allure.step("Проверяем, что заказ {order_id} найден и имеет статус '{expected_status}'")
# def assert_order_in_table(page, order_id, expected_status):

#     # 1. Находим строку с нашим order_id
#     order_link = page.locator(f'a[data-qa="order-link"]:has-text("{order_id}")')
#     page.reload()
#     expect(order_link).to_be_visible(timeout=10000)

#     # Печать
#     print("\n" + "=" * 50)
#     print(f"✅ Заказ найден в таблице: {order_id}")
#     print("=" * 50 + "\n")

#     # 2. Получаем строку таблицы, в которой находится ссылка
#     row = order_link.locator("xpath=ancestor::tr")

#     # 3. Находим статус внутри ЭТОЙ строки
#     status_cell = row.locator('[data-qa^="orders-table-order-status"]')

#     expect(status_cell).to_be_visible(timeout=5000)
#     expect(status_cell).to_have_text(expected_status)

#     print("\n" + "=" * 50)
#     print(f"✅ Статус заказа корректный: {expected_status}")
#     print("=" * 50 + "\n")

# import allure
# from playwright.sync_api import expect


# @allure.step("Проверяем тип торгов заказа {order_id}: должен быть '{expected_type}'")
# def assert_trade_type(page, order_id, expected_type):
#     # Находим ссылку на заказ
#     order_link = page.locator(f'a[data-qa="order-link"]:has-text("{order_id}")')
#     expect(order_link).to_be_visible(timeout=10000)

#     # Находим строку таблицы
#     row = order_link.locator("xpath=ancestor::tr")

#     # Внутри строки ищем элемент с типом торгов
#     trade_label = row.locator(f'.g-label_size_xs .g-label__content p:has-text("{expected_type}")')

#     expect(trade_label).to_be_visible(timeout=5000)
#     expect(trade_label).to_have_text(expected_type)

#     print("\n" + "="*50)
#     print(f"✅ Тип торгов корректный: {expected_type}")
#     print("="*50 + "\n")

# import allure
# from playwright.sync_api import expect
# import re


# @allure.step("Создаём рейс для заказа")
# def create_flight(page):

#     # 1. Кликаем "Создать рейс" в меню
#     create_flight_button = page.locator(
#         'button[data-qa="orders-table-identifier-menu-executor-create-flight-button"]'
#     )
#     expect(create_flight_button).to_be_visible(timeout=5000)
#     create_flight_button.click()

#     # 2. Выбираем водителя
#     driver_select = page.locator('button.g-select-control__button:has-text("Выберите водителя")')
#     expect(driver_select).to_be_visible(timeout=5000)
#     driver_select.click()

#     first_driver = page.locator('div[role="option"]').first
#     expect(first_driver).to_be_visible(timeout=5000)
#     first_driver.click()

#     # 3. Выбираем ТС
#     vehicle_select = page.locator('button.g-select-control__button:has-text("Выберите ТС")')
#     expect(vehicle_select).to_be_visible(timeout=5000)
#     vehicle_select.click()

#     first_vehicle = page.locator('div[role="option"]').first
#     expect(first_vehicle).to_be_visible(timeout=5000)
#     first_vehicle.click()

#     # 4. Кликаем "Создать" и ждём API flights/create/v1
#     with page.expect_response(re.compile(r".*/api/flights/create/v1")) as response_info:
#         create_button = page.get_by_role("button", name="Создать", exact=True)
#         expect(create_button).to_be_visible(timeout=5000)
#         create_button.click()

#     response = response_info.value

#     assert response.ok, f"Запрос 'create flight' вернулся с ошибкой: {response.status}"

#     # 5. Проверка структуры ответа
#     body = response.json()
#     assert "data" in body, "В ответе нет поля data"
#     flight_id = body["data"].get("id")
#     assert flight_id, "В ответе нет id рейса"

#     print("\n" + "=" * 50)
#     print(f"🚚 Рейс успешно создан! ID рейса: {flight_id}")
#     print("=" * 50 + "\n")

#     return flight_id

# @allure.step("Проверяем, что таблица пуста")
# def assert_table_empty(page):
#     rows = page.locator('a[data-qa="order-link"]')
#     assert rows.count() == 0, "Таблица должна быть пустой, но строки найдены"



# @allure.step("Ожидаем успешный запрос таблицы заказов (200 OK)")
# def wait_orders_table_reload(page):
#     with page.expect_response(re.compile(r".*/api/orders.*")) as resp:
#         # Обычно reload таблицы происходит после фильтрации
#         page.wait_for_timeout(500)
#     response = resp.value
#     assert response.ok, f"Таблица заказов ответила ошибкой: {response.status}"

# @allure.step("Проверяем, что хотя бы один заказ соответствует фильтру '{label} = {expected_value}'")
# def assert_any_row_matches(page, label, cell_selector, expected_value):

#     timeout_ms = 5000     # ждём до 5 секунд
#     interval_ms = 300     # проверяем каждые 300 мс
#     waited = 0

#     # Пытаемся дождаться появления строк
#     while waited < timeout_ms:
#         cells = page.locator(cell_selector)
#         count = cells.count()
#         if count > 0:
#             break
#         page.wait_for_timeout(interval_ms)
#         waited += interval_ms

#     # После цикла всё ещё нет строк?
#     assert count > 0, (
#         f"После фильтрации таблица пуста — "
#         f"ожидали хотя бы одну строку (ждали {timeout_ms} мс) "
#         f"cell_selector='{cell_selector}'"
#     )

#     # Проверяем ячейки
#     for i in range(count):
#         text = cells.nth(i).inner_text().strip()
#         if expected_value in text:
#             print(f"✅ Найдено совпадение в строке {i}")
#             return

#     raise AssertionError(
#         f"❌ Ни одна строка таблицы не содержит '{expected_value}' "
#         f"в колонке '{label}' ({cell_selector})"
#     )


# # Исполнитель Executor
# @allure.step("Получаем заказ {order_id} из getFlatForExecutor после фильтра")
# def get_executor_order_after_filter(page, order_id: str) -> dict:
#     with page.expect_response(
#         lambda r: (
#             "transferOrder/getFlatForExecutor" in r.url
#             and r.status == 200
#         ),
#         timeout=30000
#     ) as response_info:
#         # триггер УЖЕ произошёл (фильтр применён),
#         # поэтому просто ждём ответ
#         pass

#     body = response_info.value.json()
#     orders = body.get("data", {}).get("orders", [])

#     allure.attach(
#         "\n".join(o.get("id") for o in orders),
#         name="order_ids_after_filter",
#         attachment_type=allure.attachment_type.TEXT
#     )

#     order = next(
#         (o for o in orders if o.get("id") == order_id),
#         None
#     )

#     assert order, f"Заказ {order_id} не найден после фильтра"

#     return order

# # Заказчик Forwarder
# @allure.step("Получаем заказ {order_id} из getFlatForСustomer после фильтра")
# def get_forwarder_order_after_filter(page, order_id: str) -> dict:
#     with page.expect_response(
#         lambda r: (
#             "transferOrder/getFlatForCustomer" in r.url
#             and r.status == 200
#         ),
#         timeout=30000
#     ) as response_info:
#         # триггер УЖЕ произошёл (фильтр применён),
#         # поэтому просто ждём ответ
#         pass

#     body = response_info.value.json()
#     orders = body.get("data", {}).get("orders", [])

#     allure.attach(
#         "\n".join(o.get("id") for o in orders),
#         name="order_ids_after_filter",
#         attachment_type=allure.attachment_type.TEXT
#     )

#     order = next(
#         (o for o in orders if o.get("id") == order_id),
#         None
#     )

#     # assert order, f"Заказ {order_id} не найден после фильтра"

#     return order







# @allure.step(
#     "Применяем фильтр '{label}' с диапазоном дат: {date_from} — {date_to}"
# )
# def set_date_range_filter(page, label, date_from, date_to):
#     # 1. Открываем панель фильтров
#     page.locator("span.g-button__text", has_text="Фильтры").click()

#     # 2. Выбираем фильтр в списке
#     page.locator('[data-qa="select-popup"]') \
#         .get_by_text(label, exact=True) \
#         .click()
#     page.keyboard.press("Escape")

#     # 3. Активируем фильтр
#     page.locator("div.g-label__content", has_text=label).first.click()

#     # 4. ИЩЕМ ИМЕННО g-date-date-picker (ты его дал)
#     date_pickers = page.locator("div.g-date-date-picker")
#     expect(date_pickers).to_have_count(2, timeout=5000)

#     from_picker = date_pickers.nth(0)
#     to_picker = date_pickers.nth(1)

#     from_input = from_picker.locator(
#         "input.g-text-input__control_type_input"
#     )
#     to_input = to_picker.locator(
#         "input.g-text-input__control_type_input"
#     )

#     # 5. FROM
#     from_input.fill("")
#     from_input.type(date_from, delay=30)
#     page.keyboard.press("Tab")

#     # 6. TO
#     to_input.fill("")
#     to_input.type(date_to, delay=30)
#     page.keyboard.press("Tab")

#     # 7. Применяем
#     page.get_by_text("Применить", exact=True).click()



# @allure.step(
#     "Проверяем, что хотя бы одна строка содержит дату '{expected_date}'"
# )
# def assert_any_row_date_matches(page, cell_selector: str, expected_date: str):
#     """
#     expected_date: строка вида '12.12'
#     """

#     cells = page.locator(cell_selector)
#     count = cells.count()

#     assert count > 0, "Таблица пуста — нет строк для проверки даты"

#     for i in range(count):
#         try:
#             text = cells.nth(i).inner_text()
#             # нормализуем пробелы
#             text = re.sub(r"\s+", " ", text)

#             if expected_date in text:
#                 print(f"✅ Найдено совпадение даты '{expected_date}' в строке {i}")
#                 return
#         except Exception:
#             pass

#     raise AssertionError(
#         f"❌ Ни в одной строке таблицы не найдено даты '{expected_date}'"
#     )

# def __fill_custom_input(locator, text):
#     """Функция для заполнения кастомных input элементов"""
#     locator.click()
#     input_element = locator.locator('input')
#     input_element.fill("")
#     input_element.type(text, delay=100)

# @allure.step("Заполняем поле {selector} значением {text}")
# def write_input(page, selector, text):
#     cargo_container = page.locator(selector)
#     __fill_custom_input(cargo_container, text)
