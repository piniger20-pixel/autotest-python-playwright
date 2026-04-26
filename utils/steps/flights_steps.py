import allure
import re
from playwright.sync_api import Page, expect

@allure.step("Создаём рейс для заказа через меню заказа")
def create_flight(page) -> str:
    create_flight_button = page.locator(
        'button[data-qa="orders-table-identifier-menu-executor-create-flight-button"]'
    )
    expect(create_flight_button).to_be_visible(timeout=5000)
    
    # Ждем что кнопка станет активной (не disabled)
    page.wait_for_timeout(1000)
    
    # Используем force=True чтобы обойти перекрывающие элементы
    create_flight_button.click(force=True)
    
    # Ждем открытия модального окна
    page.wait_for_timeout(1000)

    driver_select = page.locator('button.g-select-control__button:has-text("Выберите водителя")')
    expect(driver_select).to_be_visible(timeout=10000)
    driver_select.click()
    first_driver = page.locator('div[role="option"]').first
    expect(first_driver).to_be_visible(timeout=5000)
    first_driver.click()

    vehicle_select = page.locator('button.g-select-control__button:has-text("Выберите ТС")')
    expect(vehicle_select).to_be_visible(timeout=5000)
    vehicle_select.click()
    first_vehicle = page.locator('div[role="option"]').first
    expect(first_vehicle).to_be_visible(timeout=5000)
    first_vehicle.click()

    with page.expect_response(re.compile(r".*/api/flights/create/v1")) as response_info:
        # Используем более специфичный селектор - кнопка "Создать" в контексте формы рейса
        # Ищем кнопку внутри сайдбара/модального окна рейса (последняя кнопка "Создать" на странице)
        create_button = page.locator('button:has-text("Создать")').last
        expect(create_button).to_be_visible(timeout=5000)
        create_button.click()

    response = response_info.value
    assert response.ok, f"Запрос 'create flight' вернулся с ошибкой: {response.status}"

    body = response.json()
    assert "data" in body, "В ответе нет поля data"
    flight_id = body["data"].get("id")
    assert flight_id, "В ответе нет id рейса"

    print("\n" + "=" * 50)
    print(f"🚚 Рейс успешно создан! ID рейса: {flight_id}")
    print("=" * 50 + "\n")

    return flight_id

@allure.step("Создаём рейс для заказа через управление рейсом")
def create_flight_from_bottom_menu(page) -> str:
    # Ждем стабилизации UI после выбора заказов
    page.wait_for_timeout(1000)
    
    manage_flight_button = page.locator('button:has-text("Управление рейсом")')
    # Увеличиваем timeout и добавляем retry логику
    try:
        manage_flight_button.wait_for(state="visible", timeout=15000)
    except Exception as e:
        print(f"⚠️ Кнопка 'Управление рейсом' не появилась, попытка обновления страницы...")
        page.wait_for_timeout(2000)
        manage_flight_button.wait_for(state="visible", timeout=15000)
    
    manage_flight_button.click()
    driver_select = page.locator('button.g-select-control__button:has-text("Выберите водителя")')
    expect(driver_select).to_be_visible(timeout=5000)
    driver_select.click()
    first_driver = page.locator('div[role="option"]').first
    expect(first_driver).to_be_visible(timeout=5000)
    first_driver.click()

    vehicle_select = page.locator('button.g-select-control__button:has-text("Выберите ТС")')
    expect(vehicle_select).to_be_visible(timeout=5000)
    vehicle_select.click()
    first_vehicle = page.locator('div[role="option"]').first
    expect(first_vehicle).to_be_visible(timeout=5000)
    first_vehicle.click()

    with page.expect_response(re.compile(r".*/api/flights/create/v1")) as response_info:
        # Используем более специфичный селектор - кнопка "Создать" в контексте формы рейса
        # Ищем кнопку внутри сайдбара/модального окна рейса (последняя кнопка "Создать" на странице)
        create_button = page.locator('button:has-text("Создать")').last
        expect(create_button).to_be_visible(timeout=5000)
        create_button.click()

    response = response_info.value
    assert response.ok, f"Запрос 'create flight' вернулся с ошибкой: {response.status}"
    body = response.json()
    assert "data" in body, "В ответе нет поля data"
    flight_id = body["data"].get("id")
    assert flight_id, "В ответе нет id рейса"
    print("\n" + "=" * 50)
    print(f"🚚 Рейс успешно создан! ID рейса: {flight_id}")
    print("=" * 50 + "\n")

    return flight_id

@allure.step("Удалить груз. Поиск по названию и статусу груза")
def delete_flights_cargo(page: Page, order_text: str = "Заказ № 2, тест", status_text: str = "Рейс не начат"):
    # Ищем строку, содержащую ОБА текста
    target_row = page.locator(f'.gt-table__body tr:has-text("{order_text}"):has-text("{status_text}")').first
    expect(target_row).to_be_visible(timeout=10000)
    print("✅ Найдена строка с обоими текстами") 
    # Внутри этой строки ищем кнопку
    delete_button = target_row.locator(
        'button.g-button.g-button_view_normal.g-button_size_m.g-button_pin_round-round'
    ).first
    expect(delete_button).to_be_visible(timeout=5000)
    delete_button.click(force=True)  # force=True на всякий случай
    print("✅ Кнопка удаления нажата")

@allure.step("Сохранить изменения в рейсе")
def type_saveflight_button(page: Page):
    save_button = page.locator('button:has-text("Сохранить")')
    expect(save_button).to_be_visible(timeout=5000)
    save_button.click()
    print("✅ Кнопка 'Сохранить' нажата")

@allure.step("Завершить рейс c перехватом статуса")
def complete_flight_button(page: Page):
    with page.expect_response(re.compile(r".*api/flights/v1/listForExecutor")) as response_info:
        complete_button = page.locator('button.g-button:has-text("Завершить рейс")').first
        expect(complete_button).to_be_visible(timeout=5000)
        page.wait_for_timeout(1000)
        complete_button.click(force=True)
        page.wait_for_timeout(1000)
        response = response_info.value

    assert response.ok, f"Запрос вернулся с ошибкой: {response.status}"
    body = response.json()
    # Проверяем структуру ответа и извлекаем ID рейса
    assert "data" in body
    flight_status = body["data"]["flights"][0]["status"]
    assert flight_status == "complete", f"Статус рейса не 'complete', а '{flight_status}'"
    print("\n" + "="*44)
    print(f"✅ Рейс успешно завершен! Статус: {flight_status}")
    print("="*44 + "\n")

@allure.step("Открыть сайдбар создания рейса, через управление рейсами")
def open_flight_saidbar_trgouht_bottom_menu(page: Page):
    manage_flight_button = page.locator('button:has-text("Управление рейсом")')
    manage_flight_button.wait_for(state="visible", timeout=10000)
    manage_flight_button.click()

@allure.step("Добавить заказ к существующему рейсу {flight_id}")
def add_order_to_ready_flight(page: Page, flight_id: str, timeout: int = 5000):
    # Открыть селектор рейсов
    new_flight_button = page.locator('text="Новый рейс"').first
    new_flight_button.wait_for(state="visible", timeout=timeout)
    new_flight_button.click()
    # Ввести {flight_id}
    filter_container = page.locator('[data-qa="select-filter-input"]').first
    flight_input = filter_container.locator('input').first
    flight_input.press_sequentially(str(flight_id), delay=200)
    print(f"✅ Ручной ввод выполнен: {flight_id}") 
    # Ждём появления подсказок
    page.wait_for_timeout(1000)
    # Выбрать нужный рейс
    flight_item = page.locator(f'.g-select-list__option-default-label:has-text("{flight_id}")')
    flight_item.wait_for(state="visible", timeout=timeout)
    flight_item.click()

@allure.step("Отменяем рейс через кнопку 'Отменить рейс'")
def cancel_flight(page: Page):
    """Нажимает кнопку отмены рейса в детализации"""
    cancel_button = page.locator('[data-qa="flight-details-cancel-flight-button"]')
    expect(cancel_button).to_be_visible(timeout=10000)
    cancel_button.click()
    page.wait_for_timeout(2000)
    print("✅ Кнопка 'Отменить рейс' нажата")

@allure.step("Меняем статус точки рейса на 'Прибыл на погрузку'")
def change_flight_point_status_to_arrived(page: Page):
    """Меняет статус точки рейса с 'Рейс не начат' на 'Прибыл на погрузку'"""
    flight_not_started_button = page.locator('text="Рейс не начат"').first
    expect(flight_not_started_button).to_be_visible(timeout=10000)
    flight_not_started_button.click()
    
    arrived_button = page.locator('text="Прибыл на погрузку"')
    expect(arrived_button).to_be_visible(timeout=10000)
    arrived_button.click()
    
    # Ждём обновления статуса рейса
    page.wait_for_timeout(2000)
    print("✅ Статус точки изменен на 'Прибыл на погрузку'")