import allure
import re
from playwright.sync_api import Page, expect


@allure.step("Проверяем значение на таймере торгов в {location} (значение < 1 мин)")
def assert_auction_timer_less_than_60_seconds(page: Page, location: str = "таблице"):
    """
    Проверяет, что таймер торгов показывает время < 60 секунд.
    
    Args:
        page: Playwright page object
        location: Описание места проверки для логирования
    """
    cell = page.locator("td.gt-table__cell_id_auctionTimerColumn").first
    cell.scroll_into_view_if_needed()
    expect(cell).to_be_visible(timeout=30000)

    raw = (cell.inner_text() or "").strip()
    m = re.search(r"\b(\d{1,2}:\d{2}:\d{2})\b", raw)
    assert m, f"В ячейке таймера не найдено время HH:MM:SS. Текст ячейки: '{raw}'"

    time_str = m.group(1)
    h, m_, s = map(int, time_str.split(":"))
    total_seconds = h * 3600 + m_ * 60 + s

    print(f"=== Таймер в {location.upper()} ===")
    print(f"Текст ячейки: {raw!r}")
    print(f"Длительность торгов: {time_str} = {total_seconds} секунд")

    if total_seconds >= 60:
        cell.evaluate('el => el.style.cssText = "color:#ff4444;font-weight:bold;border:2px solid red;"')
        print(f"❌ ОШИБКА: время {total_seconds} сек. ≥ 60 сек.")
    else:
        print("✅ УСПЕХ: время < 60 сек.")

    assert total_seconds < 60, f"Таймер должен быть < 60 сек. (сейчас: {time_str} = {total_seconds} сек.)"


@allure.step("Проверяем что автопродление сработало в {location} (значение > 1 мин)")
def assert_auction_timer_more_than_60_seconds(page: Page, location: str = "таблице"):
    """
    Проверяет, что таймер торгов показывает время > 60 секунд (автопродление сработало).
    
    Args:
        page: Playwright page object
        location: Описание места проверки для логирования
    """
    cell = page.locator("td.gt-table__cell_id_auctionTimerColumn").first
    cell.scroll_into_view_if_needed()
    expect(cell).to_be_visible(timeout=30000)

    raw = (cell.inner_text() or "").strip()
    m = re.search(r"\b(\d{1,2}:\d{2}:\d{2})\b", raw)
    assert m, f"Не найдено время HH:MM:SS в ячейке таймера. Текст: {raw!r}"

    time_str = m.group(1)
    h, m_, s = map(int, time_str.split(":"))
    total_seconds = h * 3600 + m_ * 60 + s

    print(f"=== Таймер в {location.upper()} ===")
    print(f"Текст ячейки: {raw!r}")
    print(f"Таймер: {time_str} = {total_seconds} сек")

    if total_seconds <= 60:
        cell.evaluate('el => el.style.cssText = "color:#ff4444;font-weight:bold;border:2px solid red;"')

    assert total_seconds > 60, f"Ожидали > 60 сек после автопродления, сейчас: {time_str} ({total_seconds} сек)"


@allure.step("Проверяем что автопродление сработало в детализации Исполнителя (Значение > 1 мин)")
def assert_auction_timer_in_details_more_than_60_seconds(page: Page):
    """Проверяет таймер в детализации заказа (> 60 секунд)"""
    timer_locator = page.locator('.g-label.g-label_theme_unknown .g-label__content')
    timer_locator.wait_for(state='visible')
    timer_text = timer_locator.text_content().strip()
    print(f"=== Таймер в ДЕТАЛИЗАЦИИ Исполнителя===")
    print(f"Значение на счетчике: {timer_text}")
    
    parts = [int(p) for p in timer_text.split(':')]
    if len(parts) == 3:
        total_seconds = parts[0] * 3600 + parts[1] * 60 + parts[2]
    else:
        total_seconds = parts[0] * 60 + parts[1]
    
    print(f"Требуется: > 60 сек.")
    print(f"Результат: {'ПРОЙДЕНО' if total_seconds > 60 else 'НЕ ПРОЙДЕНО'}")
    
    if total_seconds <= 60:
        page.eval_on_selector(
            '.g-label.g-label_theme_unknown .g-label__content',
            'el => { el.style.color = "#ff4444"; el.style.fontWeight = "bold"; }'
        )
        print("Значение < 1 мин")
    
    assert total_seconds > 60, f"Таймер {timer_text} ({total_seconds} сек.) должен быть больше 60 секунд"