import allure
import re
from playwright.sync_api import Page, expect


@allure.step("Проверяем механики торгов в таблице")
def assert_trade_mechanics_in_table(page: Page, expected_mechanics: set, max_attempts: int = 3):
    """
    Проверяет наличие механик торгов в таблице заказов с повторными попытками.
    
    Args:
        page: Playwright page object
        expected_mechanics: Множество ожидаемых механик торгов
        max_attempts: Максимальное количество попыток (по умолчанию 3)
    """
    for attempt in range(max_attempts):
        found_values = set()
        
        # Ждем стабилизации страницы перед проверкой
        if attempt > 0:
            print(f"🔄 Попытка {attempt + 1}/{max_attempts} проверки механик торгов")
            page.reload()
            page.wait_for_load_state('load')
            page.wait_for_timeout(3000)
        else:
            # Даже в первой попытке ждем стабилизации UI
            page.wait_for_load_state('load')
            page.wait_for_timeout(2000)
        
        # Пытаемся найти все ожидаемые механики
        for expected_value in expected_mechanics:
            try:
                element = page.locator(f".g-label__content p:has-text('{expected_value}')")
                element.first.wait_for(state="visible", timeout=10000)
                found_values.add(expected_value)
                print(f"✅ Найдена механика: '{expected_value}'")
            except Exception as e:
                print(f"⚠️ Не найдена механика: '{expected_value}'. Ошибка: {e}")
        
        # Если все механики найдены - успех
        if found_values == expected_mechanics:
            print(f"✅ Все типы торгов найдены и соответствуют ожидаемым: {found_values}")
            return
        
        # Если не последняя попытка - логируем и продолжаем
        if attempt < max_attempts - 1:
            missing = expected_mechanics - found_values
            print(f"⚠️ Попытка {attempt + 1} не удалась. Отсутствуют: {missing}")
    
    # Если после всех попыток не все механики найдены - ошибка
    assert found_values == expected_mechanics, \
        f"Набор типов торгов не соответствует ожидаемому после {max_attempts} попыток. " \
        f"Ожидалось: {expected_mechanics}. Найдено: {found_values}. " \
        f"Отсутствуют: {expected_mechanics - found_values}. Лишние: {found_values - expected_mechanics}"


@allure.step("Открываем окно ставки из таблицы исполнителя")
def open_bet_window_from_executor_table(page: Page):
    """Нажимает на активную кнопку 'Поставить' в таблице от исполнителя"""
    bet_button = page.locator('[data-qa="orders-table-my-active-bets-bet-button"]:not([disabled])')
    bet_button.wait_for(state="visible", timeout=10000)
    bet_button.click()


@allure.step("Проверяем отображение НДС в окне ставок")
def assert_vat_display_in_bet_window(page: Page, amount_without_vat: str, amount_with_vat: str, vat_rate: str):
    """
    Проверяет корректное отображение сумм с НДС и без НДС в окне ставок.
    
    Args:
        page: Playwright page object
        amount_without_vat: Сумма без НДС (например, "10 000")
        amount_with_vat: Сумма с НДС (например, "12 000")
        vat_rate: Ставка НДС (например, "20%")
    """
    expect(page.locator('span.g-text_variant_header-2')).to_have_text(amount_without_vat)
    expect(page.locator('span.g-text_variant_subheader-3')).to_have_text("₽")
    expect(page.locator(f'span.g-text_variant_body-2:has-text("с НДС {vat_rate}")')).to_have_text(f"{amount_with_vat} с НДС {vat_rate}")
    print(f"✅ НДС в окне ставок отображается ВЕРНО:")
    print(f"   📊 Без НДС: {amount_without_vat}₽")
    print(f"   📊 С НДС: {amount_with_vat} с НДС {vat_rate}")


@allure.step("Открываем форму создания ставки")
def open_bet_form(page: Page):
    """Нажимает на кнопку 'Поставить ставку'"""
    bet_button = page.locator('button[type="button"]:has-text("Поставить ставку")')
    bet_button.wait_for(state="visible", timeout=10000)
    expect(bet_button).to_have_text("Поставить ставку")
    bet_button.click()


@allure.step("Выбираем организацию для ставки: '{org_name}'")
def select_organization_for_bet(page: Page, org_name: str):
    """
    Выбирает организацию для ставки.
    
    Args:
        page: Playwright page object
        org_name: Название организации
    """
    org_button = page.locator('div.g-modal__content-aligner button.g-select-control__button:not([disabled])')
    org_button.wait_for(state="visible", timeout=10000)
    org_button.click()
    page.wait_for_selector('[role="listbox"]', timeout=5000)
    option = page.locator('.g-select-list__option-default-label', has_text=org_name)
    option.wait_for(state="visible", timeout=3000)
    option.click()
    print(f"✅ Организация '{org_name}' выбрана")


@allure.step("Вводим сумму ставки: {amount}")
def enter_bet_amount(page: Page, amount: str):
    """Вводит сумму ставки в поле ввода"""
    input_field = page.locator('input.g-text-input__control_type_input').first
    input_field.wait_for(state="visible", timeout=5000)
    input_field.clear()
    input_field.fill(amount)
    page.wait_for_timeout(500)


@allure.step("Проверяем ошибки валидации ставки")
def assert_bet_validation_errors(page: Page, expected_errors: list):
    """
    Проверяет наличие ошибок валидации ставки.
    
    Args:
        page: Playwright page object
        expected_errors: Список ожидаемых текстов ошибок
    """
    errors = page.locator('[data-qa="control-error-message-qa"]')
    expect(errors).to_have_count(len(expected_errors))
    for i, expected_text in enumerate(expected_errors):
        expect(errors.nth(i)).to_have_text(expected_text)
    print(f"✅ Ошибки валидации корректно подсвечиваются: {len(expected_errors)} шт.")


@allure.step("Проверяем, что кнопка 'Сделать ставку' заблокирована")
def assert_bet_button_disabled(page: Page):
    """Проверяет, что кнопка 'Сделать ставку' неактивна"""
    bet_button = page.locator('button.g-button_disabled:has-text("Сделать ставку")')
    expect(bet_button).to_be_visible()
    expect(bet_button).to_be_disabled()
    print("✅ Кнопка 'Сделать ставку' заблокирована при невалидной ставке")


@allure.step("Подтверждаем ставку")
def submit_bet(page: Page, amount: str):
    """
    Подтверждает ставку.
    
    Args:
        page: Playwright page object
        amount: Сумма ставки для логирования
    """
    bet_button = page.locator('button:has-text("Сделать ставку")')
    bet_button.click()
    print(f"✅ Ставка {amount} сделана")
    page.wait_for_timeout(1000)


@allure.step("Проверяем лучшую ставку с НДС")
def assert_best_bet_with_vat(page: Page, amount_without_vat: str, amount_with_vat: str, vat_amount: str, vat_rate: str):
    """
    Проверяет отображение лучшей ставки с НДС.
    
    Args:
        page: Playwright page object
        amount_without_vat: Сумма без НДС
        amount_with_vat: Сумма с НДС
        vat_amount: Сумма НДС
        vat_rate: Ставка НДС
    """
    best_section = page.locator('div._isBest_1l23f_13')
    expect(best_section.locator(f'span:has-text("{amount_without_vat} ₽")')).to_be_visible()
    expect(best_section.locator('span:has-text("Без НДС")')).to_be_visible()
    expect(best_section.locator('div.g-label_theme_success:has-text("Лучшая")')).to_be_visible()
    expect(best_section.locator(f'span:has-text("{amount_with_vat} ₽")')).to_be_visible()
    expect(best_section.locator(f'span:has-text("С НДС {vat_rate}")')).to_be_visible()
    expect(best_section.locator(f'span:has-text("{vat_amount} ₽")')).to_be_visible()
    print(f"✅ Лучшая ставка: {amount_without_vat} ₽ → {amount_with_vat} ₽ с НДС ({vat_amount} ₽ НДС)")


@allure.step("Проверяем лучшую ставку без НДС")
def assert_best_bet_without_vat(page: Page, amount: str):
    """
    Проверяет отображение лучшей ставки без НДС.
    
    Args:
        page: Playwright page object
        amount: Сумма ставки
    """
    best_section = page.locator('div._isBest_1l23f_13')
    expect(best_section.locator(f'span:has-text("{amount} ₽")')).to_be_visible()
    expect(best_section.locator('span:has-text("Без НДС")')).to_be_visible()
    expect(best_section.locator('div.g-label_theme_success:has-text("Лучшая")')).to_be_visible()
    print(f"✅ Лучшая ставка: {amount} ₽")


@allure.step("Проверяем ошибку при ставке не на понижение")
def assert_bet_not_decrease_error(page: Page):
    """Проверяет появление уведомления об ошибке при попытке сделать ставку не на понижение"""
    # Пробуем найти уведомление с разными селекторами
    page.wait_for_timeout(1000)
    
    # Вариант 1: Уведомление в виде тоста
    notification_selectors = [
        'div._notifications_muobj_1',
        'div[class*="notification"]',
        'div[class*="toast"]',
        'div[class*="alert"]',
        '[data-qa*="notification"]',
        '[data-qa*="error"]'
    ]
    
    error_found = False
    for selector in notification_selectors:
        try:
            notification = page.locator(selector)
            if notification.count() > 0 and notification.first.is_visible():
                text = notification.first.inner_text().lower()
                if "ставка" in text and ("меньше" in text or "понижение" in text):
                    print(f"✅ Уведомление об ошибке найдено с селектором: {selector}")
                    print(f"   Текст: {notification.first.inner_text()}")
                    error_found = True
                    break
        except:
            continue
    
    # Вариант 2: Inline ошибка валидации
    if not error_found:
        try:
            error_message = page.locator('[data-qa="control-error-message-qa"]')
            if error_message.count() > 0:
                text = error_message.first.inner_text().lower()
                if "ставка" in text and ("меньше" in text or "понижение" in text):
                    print(f"✅ Inline ошибка валидации найдена")
                    print(f"   Текст: {error_message.first.inner_text()}")
                    error_found = True
        except:
            pass
    
    # Вариант 3: Кнопка заблокирована
    if not error_found:
        try:
            bet_button = page.locator('button:has-text("Сделать ставку")')
            if bet_button.is_disabled():
                print("✅ Кнопка 'Сделать ставку' заблокирована (ставка не на понижение)")
                error_found = True
        except:
            pass
    
    assert error_found, "❌ Не найдено уведомление об ошибке при ставке не на понижение"
    print("✅ Проверка механики 'Только на понижение' пройдена")


@allure.step("Открываем окно торгов из таблицы заказчика")
def open_auction_window_from_customer_table(page: Page):
    """Нажимает на активную кнопку 'К торгам' в таблице от заказчика"""
    bet_button = page.locator('button:has-text("К торгам"):not([disabled])').first
    bet_button.wait_for(state="visible", timeout=10000)
    bet_button.click()


@allure.step("Выбираем победителя торгов")
def select_auction_winner(page: Page):
    """Нажимает на кнопку 'Выбрать' для выбора победившей ставки"""
    select_button = page.locator('button:has-text("Выбрать")').first
    select_button.wait_for(state="visible", timeout=10000)
    select_button.click()


@allure.step("Подтверждаем выбор победителя торгов")
def confirm_auction_winner(page: Page) -> str:
    """
    Подтверждает выбор победителя торгов и проверяет статус.
    
    Returns:
        str: Статус торгов после подтверждения
    """
    confirm_button = page.locator('button:has-text("Выбрать победителем и завершить торги")')
    expect(confirm_button).to_be_visible(timeout=5000)
    
    # Кликаем и перехватываем первый запрос
    with page.expect_response(re.compile(r".*/api/orders/v0/transferOrder/getFlatForCustomer")) as first_resp:
        confirm_button.click()
    
    # Пытаемся поймать второй запрос, если не получилось - используем первый
    try:
        with page.expect_response(re.compile(r".*/api/orders/v0/transferOrder/getFlatForCustomer"), timeout=5000) as second_resp:
            page.wait_for_timeout(100)
        response = second_resp.value
    except:
        response = first_resp.value
    
    assert response.ok
    status = response.json()["data"]["orders"][0]["matcher"]["matcherStatus"]
    assert status == "complete_with_winner", f"Статус: {status}"
    print(f"✅ Ставка принята Заказчиком! Статус: {status}")
    
    return status


@allure.step("Отменяем ставку исполнителем")
def cancel_bet_by_executor(page: Page):
    """Отменяет ставку от лица исполнителя"""
    cancel_button = page.locator('button.g-button.g-button_view_outlined-info.g-button_size_m.g-button_pin_round-round').nth(1)
    cancel_button.wait_for(state="visible", timeout=5000)
    cancel_button.click()
    page.wait_for_timeout(1000)
    
    # Подтвердить отмену ставки в поп апе
    pop_up_cancel_button = page.locator('button.g-button.g-button_view_outlined-danger.g-button_size_l.g-button_pin_round-round:has-text("Да, отклонить")')
    pop_up_cancel_button.wait_for(state="visible", timeout=5000)
    pop_up_cancel_button.click()
    print("✅ Ставка отменена исполнителем")
    page.wait_for_timeout(1000)


@allure.step("Вводим комментарий к ставке: '{comment}'")
def enter_bet_comment(page: Page, comment: str):
    """Вводит комментарий к ставке"""
    input_field_comment = page.locator('xpath=//*[contains(text(), "Комментарий")]/following::textarea[contains(@class, "g-text-area")]')
    input_field_comment.clear()
    input_field_comment.fill(comment)
    print(f"✅ Комментарий введен: {comment}")


@allure.step("Открываем форму замены ставки")
def open_replace_bet_form(page: Page):
    """Нажимает на кнопку 'Заменить' для замены ставки"""
    change_bet_button = page.locator('button.g-button.g-button_view_outlined-info.g-button_size_m.g-button_pin_round-round:has-text("Заменить")')
    change_bet_button.wait_for(state="visible", timeout=5000)
    change_bet_button.click()
    page.wait_for_timeout(1000)
    print("✅ Форма замены ставки открыта")


@allure.step("Заменяем ставку на сумму {amount}")
def replace_bet(page: Page, amount: str) -> str:
    """
    Заменяет ставку на новую сумму и возвращает ID созданной ставки.
    
    Args:
        page: Playwright page object
        amount: Новая сумма ставки
    
    Returns:
        str: ID созданной ставки
    """
    # Wait for button to be ready
    bet_button = page.locator('button:has-text("Заменить ставку")')
    bet_button.wait_for(state="visible", timeout=5000)
    expect(bet_button).to_be_enabled(timeout=5000)
    page.wait_for_timeout(500)
    
    # Запускаем отслеживание и заменяем ставку
    with page.expect_response("**/api/bet/create/v0", timeout=35000) as response_info:
        bet_button.click()
        page.wait_for_timeout(500)
    
    print(f"✅ Ставка заменена на {amount}")
    
    # Получаем ответ
    response = response_info.value
    assert response.ok, f"Ошибка API при замене ставки: {response.status}"
    
    bet_data = response.json()
    bet_id = bet_data.get("data", {}).get("id")
    assert bet_id, "В ответе API нет ID ставки"
    
    print(f"✅ ID созданной ставки: {bet_id}")
    page.wait_for_timeout(1000)
    
    return bet_id


@allure.step("Отклоняем ставку заказчиком")
def reject_bet_by_customer(page: Page):
    """Отклоняет ставку от лица заказчика"""
    customer_cancel_button = page.locator('button.g-button.g-button_view_outlined-success.g-button_size_l.g-button_pin_round-round').nth(1)
    customer_cancel_button.wait_for(state="visible", timeout=5000)
    customer_cancel_button.click()
    page.wait_for_timeout(1000)


@allure.step("Вводим комментарий к отклонению ставки: '{comment}'")
def enter_rejection_comment(page: Page, comment: str):
    """Вводит комментарий при отклонении ставки заказчиком"""
    comment_cancel_input_field = page.locator('[placeholder="Напишите ответ исполнителю, если есть что добавить"]')
    comment_cancel_input_field.clear()
    comment_cancel_input_field.fill(comment)
    print(f"✅ Комментарий к отклонению введен: {comment}")


@allure.step("Подтверждаем отклонение ставки")
def confirm_bet_rejection(page: Page):
    """Подтверждает отклонение ставки в модальном окне"""
    pop_up_cancel_button = page.locator('button:has-text("Да, отклонить")')
    pop_up_cancel_button.wait_for(state="visible", timeout=5000)
    pop_up_cancel_button.click()
    print("✅ Ставка отклонена заказчиком")
    page.wait_for_timeout(1000)


@allure.step("Проверяем комментарий заказчика к отклонённой ставке")
def assert_customer_rejection_comment(page: Page, expected_comment: str):
    """
    Проверяет наличие комментария заказчика к отклонённой ставке.
    
    Args:
        page: Playwright page object
        expected_comment: Ожидаемый текст комментария
    """
    # Нажать на кликабельный элемент отклонённой ставки
    customer_comment_element = page.locator('text="Комментарий заказчика"')
    customer_comment_element.wait_for(state="visible", timeout=10000)
    customer_comment_element.click()
    print("✅ Отклоненный комментарий раскрыт")
    
    # Проверяем комментарий заказчика к отмене
    element = page.locator(f'.g-text.g-text_variant_body-1:has-text("{expected_comment}")')
    assert element.count() > 0, f"Комментарий '{expected_comment}' не найден"
    print(f"✅ Проверка пройдена: комментарий '{expected_comment}' найден")


@allure.step("Закрываем окно деталей ставки")
def close_bet_details(page: Page):
    """Закрывает окно деталей ставки кликом вне области"""
    page.mouse.click(10, 10)
    page.wait_for_timeout(1000)
    print("✅ Окно деталей ставки закрыто")


@allure.step("Закрываем окно деталей заказа")
def close_order_details_window(page: Page):
    """Закрывает окно деталей заказа через меню"""
    close_button_details = page.locator('[role="menuitem"]:has-text("Исполнитель")')
    close_button_details.wait_for(state="visible", timeout=10000)
    close_button_details.click()
    print("✅ Окно деталей заказа закрыто")