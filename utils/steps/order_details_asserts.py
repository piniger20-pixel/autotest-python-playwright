import allure
from playwright.sync_api import Page, expect


@allure.step("Проверяем наличие текста '{text}' в детализации заказа")
def assert_text_in_order_details(page: Page, text: str):
    """Проверяет наличие текста в детализации заказа"""
    element = page.get_by_text(text)
    expect(element).to_be_visible(timeout=10000)
    print(f"✅ Текст найден: '{text}'")


@allure.step("Проверяем статус отмены заказа и комментарий")
def assert_cancellation_reason_and_comment(
    page: Page,
    reason: str = "Исполнитель не подал ТС под погрузку",
    comment: str = "тест по отмене заказа заказчиком"
):
    """Проверяет наличие причины отмены и комментария в детализации заказа"""
    # Проверяем причину
    reason_element = page.get_by_text(reason)
    expect(reason_element).to_be_visible(timeout=10000)
    print(f"✅ Причина отмены найдена: '{reason}'")
    
    # Проверяем комментарий
    comment_element = page.get_by_text(comment)
    expect(comment_element).to_be_visible(timeout=5000)
    print(f"✅ Комментарий найден: '{comment}'")


@allure.step("Открываем заказ со статусом '{status}' с повторными попытками")
def open_order_by_status_with_retry(page: Page, status: str, max_attempts: int = 3):
    """
    Открывает заказ по статусу с повторными попытками при неудаче.
    Используется для заказов, которые могут появиться с задержкой.
    """
    for attempt in range(1, max_attempts + 1):
        try:
            print(f"🔄 Попытка {attempt}/{max_attempts}")
            
            # Ищем заказ со статусом
            status_locator = page.locator(
                f'[data-qa^="orders-table-order-status-"]:has-text("{status}")'
            ).first
            expect(status_locator).to_be_visible(timeout=8000)
            
            # Находим ссылку на заказ в той же строке
            order_link = status_locator.locator(
                'xpath=ancestor::tr//a[@data-qa="order-link"]'
            ).first
            expect(order_link).to_be_visible(timeout=5000)
            order_link.click()
            
            print(f"✅ Успешно открыт заказ со статусом '{status}' на попытке {attempt}")
            return
            
        except Exception as e:
            print(f"⚠️ Попытка {attempt} не удалась: {e}")
            if attempt == max_attempts:
                print("❌ Все попытки исчерпаны")
                raise
            else:
                print("🔄 Обновляем страницу...")
                page.reload()
                page.wait_for_load_state('load')
                page.wait_for_timeout(2000)


@allure.step("Проверить статус заказа 'Черновик' с повторными попытками")
def assert_order_status_draft_with_retry(page: Page, order_id: str, max_attempts: int = 3):
    """Проверить что заказ перешел в статус 'Черновик' с несколькими попытками"""
    for attempt in range(max_attempts):
        page.reload()
        page.wait_for_load_state('load')
        page.wait_for_timeout(3000)
        
        order_link = page.locator(f'a[data-qa="order-link"]:has-text("{order_id}")')
        if order_link.count() > 0:
            row = order_link.locator("xpath=ancestor::tr")
            status_cell = row.locator('[data-qa^="orders-table-order-status"]')
            
            if status_cell.count() > 0:
                current_status = status_cell.inner_text().strip()
                print(f"📊 Текущий статус: {current_status}")
                
                if current_status == "Черновик":
                    print("✅ Заказ перешел в статус 'Черновик'")
                    return
                else:
                    print(f"⚠️ Статус не изменился: {current_status}")
        else:
            print("⚠️ Заказ не найден в таблице")
    
    import pytest
    pytest.fail(f"❌ Заказ не перешел в статус 'Черновик' после {max_attempts} попыток")