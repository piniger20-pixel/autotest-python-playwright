import allure
from playwright.sync_api import Page, expect
from helpers.ui import wait_and_click, fill_custom_input, fill_textarea, select_from_select_list, pick_from_popup_menu, set_address_with_suggest, pick_date_by_dataqa_offset

@allure.step("Принять предложение по заказу #'{value}' из таблицы исполнителя")
def accept_offer_1x1_from_table_order (page: Page, value ):
    # Сначала ждем появления строки с заказом
    order_row = page.locator(f'tr:has-text("{value}")').first
    expect(order_row).to_be_visible(timeout=15000)
    print(f"✅ Найдена строка с заказом {value}")
    
    # Ищем кнопку "Поставить" в строке с увеличенным таймаутом
    bet_button = order_row.locator('button:has-text("Поставить")').first
    
    try:
        expect(bet_button).to_be_visible(timeout=15000)
        bet_button.click()
        print(f"✅ Нажата кнопка 'Поставить' для заказа {value}")
    except Exception as e:
        print(f"⚠️ Не удалось найти кнопку 'Поставить': {e}")
        # Попробуем альтернативный селектор - кнопка может быть в другом месте
        bet_button_alt = page.locator(f'tr:has-text("{value}") button').filter(has_text="Поставить").first
        expect(bet_button_alt).to_be_visible(timeout=10000)
        bet_button_alt.click()
        print(f"✅ Нажата кнопка 'Поставить' (альтернативный селектор) для заказа {value}")
    
    page.wait_for_timeout(1000)  # Ждем появления модального окна
    accept_button1 = page.get_by_role("button", name="Принять условия").first
    expect(accept_button1).to_be_visible(timeout=10000)
    accept_button1.click()
    # Ждем появления модального окна и ищем кнопку внутри футера модалки
    page.wait_for_timeout(2000)
    page.wait_for_selector("div._footer_3rynv_29", timeout=10000)
    accept_button2 = page.locator("div._footer_3rynv_29 button.g-button_view_action:has-text('Принять условия')")
    expect(accept_button2).to_be_visible(timeout=10000)
    accept_button2.click(force=True)
    
    # Ждем закрытия модального окна после принятия предложения
    page.wait_for_selector("div._footer_3rynv_29", state="hidden", timeout=10000)
    # Дополнительное ожидание для обработки на бэкенде
    page.wait_for_timeout(2000)
    print(f"✅ Предложение по заказу {value} принято")