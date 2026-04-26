import allure
from playwright.sync_api import Page, expect


@allure.step("Проверяем, что рейс {flight_id} найден в таблице")
def assert_flight_in_table(page: Page, flight_id: str):
    """Проверяет наличие рейса в таблице по его ID"""
    flight_link = page.locator(f'a[href*="/flights/"]:has-text("{flight_id}")')
    expect(flight_link).to_be_visible(timeout=10000)
    print("\n" + "="*44)
    print(f"✅ Рейс найден в таблице № {flight_id}")
    print("="*44 + "\n")


@allure.step("Проверяем, что заказ {order_id} находится в рейсе {flight_id}")
def assert_order_in_flight(page: Page, flight_id: str, order_id: str):
    """Проверяет наличие заказа в рейсе"""
    order_info_cell = page.locator(
        f'tr:has-text("{flight_id}") td.gt-table__cell_id_orderInfoColumn'
    ).first
    expect(order_info_cell).to_be_visible(timeout=10000)
    cell_text = order_info_cell.text_content().strip()
    
    print(f"\n🔍 Отладка проверки заказа в рейсе:")
    print(f"   Рейс: {flight_id}")
    print(f"   Ищем заказ: {order_id}")
    print(f"   Содержимое ячейки: '{cell_text}'")
    
    assert order_id in cell_text, \
        f"❌ Заказ {order_id} не найден в рейсе {flight_id}. Содержимое ячейки: '{cell_text}'"
    print(f"✅ Заказ {order_id} найден в рейсе")


@allure.step("Проверяем, что заказы {order_ids} находятся в рейсе {flight_id}")
def assert_multiple_orders_in_flight(page: Page, flight_id: str, order_ids: list):
    """Проверяет наличие нескольких заказов в рейсе"""
    order_info_cell = page.locator(
        f'tr:has-text("{flight_id}") td.gt-table__cell_id_orderInfoColumn'
    ).first
    expect(order_info_cell).to_be_visible(timeout=10000)
    cell_text = order_info_cell.text_content().strip()
    
    print(f"\n🔍 Отладка проверки заказов в рейсе:")
    print(f"   Рейс: {flight_id}")
    print(f"   Ищем заказы: {order_ids}")
    print(f"   Содержимое ячейки: '{cell_text}'")
    
    for order_id in order_ids:
        if order_id in cell_text:
            print(f"   ✅ Заказ {order_id} найден")
        else:
            print(f"   ❌ Заказ {order_id} НЕ найден")
            assert False, f"❌ Заказ {order_id} отсутствует в рейсе. Содержимое ячейки: '{cell_text}'"
    
    print(f"✅ Все заказы ({len(order_ids)}) найдены в рейсе")


@allure.step("Проверяем наличие грузов в разделе 'Маршрут'")
def assert_shipments_in_route(page: Page, shipment_text: str, min_count: int = 2):
    """Проверяет наличие грузов в разделе Маршрут"""
    # Ждём появления элемента с текстом "Маршрут"
    page.wait_for_selector('*:has-text("Маршрут")', timeout=15000)
    print("✅ Элемент 'Маршрут' появился на странице")
    
    # Ждём появления хотя бы одного элемента с заказом
    page.wait_for_selector(f'*:has-text("{shipment_text}")', timeout=10000)
    print(f"✅ Элементы с '{shipment_text}' появились на странице")
    
    # Дополнительная пауза для полной загрузки всех элементов
    page.wait_for_timeout(2000)
    
    # Находим все элементы с "Маршрут"
    route_elements = page.locator('*:has-text("Маршрут")')
    
    # Проверяем видимость и ищем нужный
    found = False
    for i in range(route_elements.count()):
        el = route_elements.nth(i)
        if el.is_visible():
            # Проверяем видимость и подсчитываем заказы
            order_count = el.text_content().count(shipment_text)
            print(f"   Контейнер {i}: найдено погрузок/разгрузок: {order_count}")
            
            if order_count >= min_count:
                found = True
                print(f"✅ Найден видимый элемент с повторяющимися названиями (найдено: {order_count})")
                break
    
    assert found, f"❌ Нет видимого элемента с 'Маршрут' и повторяющимся '{shipment_text}' (минимум {min_count})"


@allure.step("Открываем детали рейса {flight_id}")
def open_flight_details(page: Page, flight_id: str):
    """Открывает сайдбар с деталями рейса"""
    flight_link = page.locator(f'a[href*="/flights/"]:has-text("{flight_id}")')
    expect(flight_link).to_be_visible(timeout=10000)
    flight_link.click()
    page.wait_for_timeout(2000)


@allure.step("Закрываем детали рейса")
def close_flight_details(page: Page):
    """Закрывает сайдбар с деталями рейса"""
    button_close = page.locator('.g-button.g-button_view_flat.g-button_size_l.g-button_pin_round-round').first
    button_close.click()
    page.wait_for_timeout(1000)


@allure.step("Проверяем статус рейса: '{expected_status}'")
def assert_flight_status(page: Page, expected_status: str):
    """Проверяет статус рейса в детализации"""
    flight_status_label = page.locator('[data-qa="flight-details-status-label"]')
    expect(flight_status_label).to_be_visible(timeout=10000)
    actual_text = flight_status_label.text_content().strip()
    
    assert actual_text == expected_status, (
        f"Статус рейса неверный.\n"
        f"Ожидалось: '{expected_status}'\n"
        f"Получено: '{actual_text}'"
    )
    
    print("\n" + "="*44)
    print(f"✅ Статус рейса: '{expected_status}'")
    print("="*44 + "\n")