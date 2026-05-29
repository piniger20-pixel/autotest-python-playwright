import allure
import re
import pytest
from playwright.sync_api import expect, Page


@allure.step("Проверяем, что заказ {order_id} найден и имеет статус '{expected_status}'")
def assert_order_in_table(page, order_id, expected_status):

    # Wait for table to load and stabilize
    page.wait_for_timeout(1000)
    
    # Retry logic to handle race conditions in headless mode
    max_attempts = 3
    order_link = None
    
    for attempt in range(max_attempts):
        # 1. Находим строку с нашим order_id
        all_order_links = page.locator(f'a[data-qa="order-link"]:has-text("{order_id}")')
        
        # Wait for at least one link to appear
        try:
            all_order_links.first.wait_for(state="attached", timeout=5000)
        except:
            if attempt < max_attempts - 1:
                print(f"⏳ Попытка {attempt + 1}/{max_attempts}: заказ еще не появился, ждем...")
                page.wait_for_timeout(2000)
                continue
            else:
                raise AssertionError(f"Заказ {order_id} не найден в таблице после {max_attempts} попыток")
        
        # Проверяем каждую ссылку на точное совпадение текста
        count = all_order_links.count()
        for i in range(count):
            link = all_order_links.nth(i)
            try:
                if link.inner_text().strip() == order_id:
                    order_link = link
                    break
            except:
                continue
        
        if order_link is not None:
            break
        
        if attempt < max_attempts - 1:
            print(f"⏳ Попытка {attempt + 1}/{max_attempts}: точное совпадение не найдено, повторяем...")
            page.wait_for_timeout(2000)
    
    assert order_link is not None, f"Заказ {order_id} не найден в таблице после {max_attempts} попыток"
    expect(order_link).to_be_visible(timeout=10000)

    # Печать
    print("\n" + "=" * 50)
    print(f"✅ Заказ найден в таблице: {order_id}")
    print("=" * 50 + "\n")

    # 2. Получаем строку таблицы, в которой находится ссылка
    row = order_link.locator("xpath=ancestor::tr")

    # 3. Находим статус внутри ЭТОЙ строки
    status_cell = row.locator('[data-qa^="orders-table-order-status"]')

    expect(status_cell).to_be_visible(timeout=5000)
    expect(status_cell).to_have_text(expected_status)

    print("\n" + "=" * 50)
    print(f"✅ Статус заказа корректный: {expected_status}")
    print("=" * 50 + "\n")


@allure.step("Проверяем тип торгов заказа {order_id}: должен быть '{expected_type}'")
def assert_trade_type(page, order_id, expected_type):
    # Wait for table to stabilize
    page.wait_for_timeout(500)
    
    # Retry logic to handle race conditions
    max_attempts = 3
    order_link = None
    
    for attempt in range(max_attempts):
        all_order_links = page.locator(f'a[data-qa="order-link"]:has-text("{order_id}")')
        
        try:
            all_order_links.first.wait_for(state="attached", timeout=3000)
        except:
            if attempt < max_attempts - 1:
                page.wait_for_timeout(1000)
                continue
            else:
                raise AssertionError(f"Заказ {order_id} не найден в таблице")
        
        count = all_order_links.count()
        for i in range(count):
            link = all_order_links.nth(i)
            try:
                if link.inner_text().strip() == order_id:
                    order_link = link
                    break
            except:
                continue
        
        if order_link is not None:
            break
            
        if attempt < max_attempts - 1:
            page.wait_for_timeout(1000)
    
    assert order_link is not None, f"Заказ {order_id} не найден в таблице"
    expect(order_link).to_be_visible(timeout=10000)

    # Находим строку таблицы
    row = order_link.locator("xpath=ancestor::tr")

    # Внутри строки ищем элемент с типом торгов
    trade_label = row.locator(f'.g-label_size_xs .g-label__content p:has-text("{expected_type}")')

    expect(trade_label).to_be_visible(timeout=5000)
    expect(trade_label).to_have_text(expected_type)

    print("\n" + "="*50)
    print(f"✅ Тип торгов корректный: {expected_type}")
    print("="*50 + "\n")


@allure.step("Проверяем, что таблица пуста")
def assert_table_empty(page):
    rows = page.locator('a[data-qa="order-link"]')
    assert rows.count() == 0, "Таблица должна быть пустой, но строки найдены"


@allure.step("Проверяем, что хотя бы один заказ соответствует фильтру '{label} = {expected_value}'")
def assert_any_row_matches(page, label, cell_selector, expected_value):

    timeout_ms = 5000     # ждём до 5 секунд
    interval_ms = 300     # проверяем каждые 300 мс
    waited = 0

    # Пытаемся дождаться появления строк
    while waited < timeout_ms:
        cells = page.locator(cell_selector)
        count = cells.count()
        if count > 0:
            break
        page.wait_for_timeout(interval_ms)
        waited += interval_ms

    # После цикла всё ещё нет строк?
    assert count > 0, (
        f"После фильтрации таблица пуста — "
        f"ожидали хотя бы одну строку (ждали {timeout_ms} мс) "
        f"cell_selector='{cell_selector}'"
    )

    # Проверяем ячейки
    for i in range(count):
        text = cells.nth(i).inner_text().strip()
        if expected_value in text:
            print(f"✅ Найдено совпадение в строке {i}")
            return

    raise AssertionError(
        f"❌ Ни одна строка таблицы не содержит '{expected_value}' "
        f"в колонке '{label}' ({cell_selector})"
    )


@allure.step(
    "Проверяем, что хотя бы одна строка содержит дату '{expected_date}'"
)
def assert_any_row_date_matches(page, cell_selector: str, expected_date: str):
    """
    expected_date: строка вида '12.12'
    """

    cells = page.locator(cell_selector)
    count = cells.count()

    assert count > 0, "Таблица пуста — нет строк для проверки даты"

    for i in range(count):
        try:
            text = cells.nth(i).inner_text()
            # нормализуем пробелы
            text = re.sub(r"\s+", " ", text)

            if expected_date in text:
                print(f"✅ Найдено совпадение даты '{expected_date}' в строке {i}")
                return
        except Exception:
            pass

    raise AssertionError(
        f"❌ Ни в одной строке таблицы не найдено даты '{expected_date}'"
    )


@allure.step("Проверяем статус заказа в первой строке таблицы: '{expected_status}'")
def assert_order_status_in_first_row(page: Page, expected_status: str):
    """
    Проверяет статус заказа в первой строке таблицы.
    
    Args:
        page: Playwright page object
        expected_status: Ожидаемый статус заказа
    """
    status_cell = page.locator('[data-qa^="orders-table-order-status"]').first
    expect(status_cell).to_be_visible(timeout=10000)
    expect(status_cell).to_have_text(expected_status)
    print(f"✅ Статус заказа в первой строке: {expected_status}")


@allure.step("Проверяем отображение всех заказов в таблице")
def assert_multiple_orders_in_table(page: Page, order_ids: list):
    """
    Проверяет наличие всех заказов из списка в таблице.
    
    Args:
        page: Playwright page object
        order_ids: Список ID заказов для проверки
    """
    page.wait_for_selector('#wrapper > div > div[class*="_wrapper_"] > table > tbody', timeout=10000)
    
    found_orders = []
    missing_orders = []
    
    for order_id in order_ids:
        # Ищем заказ в таблице
        order_cell = page.locator(f'#wrapper > div > div[class*="_wrapper_"] > table > tbody td:has-text("{order_id}")')
        if order_cell.count() > 0:
            found_orders.append(order_id)
            print(f"✅ Заказ {order_id} найден в таблице")
        else:
            missing_orders.append(order_id)
            print(f"❌ Заказ {order_id} НЕ найден в таблице")

    # Итоговый отчет
    print(f"\n📊 ИТОГ ПРОВЕРКИ:")
    print(f"✅ Найдено: {len(found_orders)} заказов")
    print(f"❌ Отсутствует: {len(missing_orders)} заказов")

    if found_orders:
        print(f"📋 Найденные заказы: {found_orders}")
    if missing_orders:
        print(f"🚨 Пропущенные заказы: {missing_orders}")
        pytest.fail(f"Не все заказы отображаются в таблице. Пропущено: {len(missing_orders)} из {len(order_ids)}")
    else:
        print("🎉 ВСЕ ЗАКАЗЫ УСПЕШНО ОТОБРАЖАЮТСЯ В ТАБЛИЦЕ!")


@allure.step("Проверяем наличие статусов заказов в таблице")
def assert_order_statuses_present(page: Page, expected_statuses: list):
    """
    Проверяет наличие всех ожидаемых статусов в таблице заказов.
    
    Args:
        page: Playwright page object
        expected_statuses: Список ожидаемых статусов для проверки
    """
    # Ждём появления всех статусов
    for status in expected_statuses:
        try:
            page.wait_for_selector(f'text="{status}"', timeout=15000)
            print(f"✅ Статус '{status}' появился на странице")
        except:
            page.screenshot(path=f"debug_status_{status}_timeout.png")
            print(f"⚠️ Статус '{status}' не появился вовремя")
    
    # Собираем все статусы из таблицы
    status_elements = page.locator('.gt-table__cell_id_orderStatusColumn')
    statuses = status_elements.all_text_contents()
    statuses = [s.strip() for s in statuses if s.strip()]
    
    print(f"📊 Найденные статусы: {statuses}")
    
    # Проверяем наличие каждого ожидаемого статуса
    for expected_status in expected_statuses:
        assert expected_status in statuses, \
            f"❌ Нет статуса '{expected_status}'. Найдены: {statuses}"
        print(f"✅ Статус '{expected_status}' найден в таблице")


@allure.step("Ожидаем появления заказа {order_id} в таблице с повторными попытками")
def wait_for_order_in_table(page: Page, order_id: str, max_attempts: int = 12, wait_seconds: int = 5) -> bool:
    """
    Ожидает появления заказа в таблице с повторными попытками и перезагрузкой страницы.
    
    Args:
        page: Playwright page object
        order_id: ID заказа для поиска
        max_attempts: Максимальное количество попыток
        wait_seconds: Время ожидания между попытками в секундах
    
    Returns:
        bool: True если заказ найден, False если не найден
    """
    for attempt in range(max_attempts):
        try:
            all_order_links = page.locator(f'a[data-qa="order-link"]:has-text("{order_id}")')
            count = all_order_links.count()
            for i in range(count):
                link = all_order_links.nth(i)
                if link.inner_text().strip() == order_id and link.is_visible(timeout=3000):
                    print(f"✅ Заказ найден в таблице: {order_id}")
                    return True
        except:
            print(f"⏳ Заказ {order_id} еще не появился, попытка {attempt + 1}/{max_attempts}")
        
        if attempt < max_attempts - 1:
            print("🔄 Обновляем страницу...")
            page.reload()
            page.wait_for_timeout(wait_seconds * 1000)
    
    return False


@allure.step("Проверяем статус заказа в первой строке: '{expected_status}'")
def assert_order_status_by_index(page: Page, index: int, expected_status: str):
    """
    Проверяет статус заказа по индексу строки в таблице.
    
    Args:
        page: Playwright page object
        index: Индекс строки (0-based)
        expected_status: Ожидаемый статус заказа
    """
    status_cell = page.locator(f'[data-qa="orders-table-order-status-{index}"]')
    expect(status_cell).to_be_visible(timeout=10000)
    expect(status_cell).to_have_text(expected_status, timeout=5000)
    print(f"✅ Статус заказа в строке {index}: {expected_status}")