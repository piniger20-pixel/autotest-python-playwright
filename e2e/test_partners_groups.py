import pytest
from playwright.sync_api import Page, expect
from urllib.parse import unquote
import re
import json
from typing import Dict
import random
import allure
import logging
from faker import Faker
from config import EMPLOYEE_EMAIL, HEADLESS
from datetime import date, timedelta, datetime

log = logging.getLogger(__name__)
fake = Faker("ru_RU")

@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.critical
@pytest.mark.order_creation
@allure.feature("Orders")
@allure.story("Create group of partners")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("создание группы партнёров")
@allure.description("""
Тест проверяет:
1. Создание группы партнёров
2. Добавление новых партнёров в группу
4. Редактирование группы партнёров                    
3. Добавление группы партнёров в форме создания заказа
4. Удаление группы партнёров
""")

def test_group_of_parters(chromium_page: Page):
    page = chromium_page
   
            # Установка сессии через insecure endpoint
    with allure.step("Шаг 1: Установка сессии через insecure endpoint"):
                set_cookie_url = f"https://yamagistrali.tst.yandex.net/api/set_ya_cookie_insecure?tkn={EMPLOYEE_EMAIL}"
                page.goto(set_cookie_url)
                page.wait_for_load_state("networkidle")
                page.goto("https://yamagistrali.tst.yandex.net/")
                page.wait_for_selector("div#wrapper", timeout=15000)

    with allure.step("Шаг 2: Переход на страницу группы партнёров"):
                page.get_by_text("Моя организация").click()
                #Нажимаем на кнопку Водители
                page.get_by_text("Партнеры").click()
                
    with allure.step("Шаг 3: Открыть поп ап добавления партнёров"):
                button = page.locator(".g-button.g-button_view_action")
                button.wait_for(state="visible", timeout=10000)
                button.click()
            
    with allure.step("Шаг 3: Формирование группы партнёров"):
                # выбор организации
                org_select = page.locator("span:has-text('Организация') + div .g-select-control__button")
                org_select.wait_for(state="visible", timeout=10000)
    
                # Проверяем текущий выбранный текст
                current_text = org_select.locator('.g-select-control__option-text').text_content().strip()
                is_disabled = org_select.is_disabled()

                if is_disabled:
                    # Проверяем disabled поле
                    allowed_texts = ["Test qa org", "Test qa org,"]
                    assert current_text in allowed_texts, f"В disabled поле '{current_text}', допустимы: {allowed_texts}"
                    print("✅ Нужная организация уже выбрана")
                else:
                    # Поле активно
                    if current_text != "Test qa org":
                        print(f"Выбираем организацию 'Test qa org' вместо '{current_text}'")
                        # Если текст не совпадает: кликаем и выбираем организацию
                        org_select.click()
                        page.locator('[role="option"]:has-text("Test qa org")').wait_for(state="visible", timeout=5000)
                        page.locator('[role="option"]:has-text("Test qa org")').click()
                        print("Организация 'Test qa org' выбрана")
                    else:
                        print("✅ Организация 'Test qa org' уже выбрана")
                #if current_text != "Test qa org":
                    #page.wait_for_timeout(5000) 
                #else:
                # Если уже выбрана нужная организация, просто проверяем
                    #expect(org_select.locator('.g-select-control__option-text')).to_have_text("Test qa org")
                # выбраем страну
                country_select = page.locator("span:has-text('Страна') + div .g-select-control__button")
                country_select.wait_for(state="visible", timeout=10000)
                country_select.click()
                page.locator('text="Беларусь"').click()
                # Вводим название для группы
                name_input = page.locator('input[placeholder="Придумайте название"]')
                name_input.wait_for(state="visible", timeout=10000)
                random_name = fake.catch_phrase() 
                name_input.clear()
                name_input.fill(random_name)
    with allure.step("Шаг 4: Поиск и добавление партнёра по названию и ИНН"):
                # Поиск партнёра по названию
                search_input = page.locator('._modal__searchNewPartners_1iu8n_124 input')
                search_input.wait_for(state="visible", timeout=10000)
                search_input.fill("тест Авто Исполнитель")
                page.locator('.drop-wrapper').wait_for(state="visible", timeout=10000)
                # Ждем появления списка партнеров
                partners_list = page.locator('.drop-wrapper')
                partners_list.wait_for(state="visible", timeout=10000)
                # Нажимаем кнопку "Добавить"
                add_button = partners_list.locator('.g-button.g-button_view_normal.g-button_size_m.g-button_pin_round-round')
                #add_button.wait_for(state="visible", timeout=10000)
                page.wait_for_timeout(2000)
                add_button.click()
                page.wait_for_timeout(1000)
                page.mouse.click(10, 10)
                # Проверить оргу в таблице партнёров и активировать, если неактивна
                # Находим индекс элемента с текстом "тест Авто Исполнитель"
                all_partners = page.locator('._partnersList_1iu8n_149 > div')
                target_index = -1

                for i in range(all_partners.count()):
                    text = all_partners.nth(i).text_content().strip()
                    if "тест Авто Исполнитель" in text:
                        target_index = i
                        print(f"Найден партнер на позиции {i}: '{text}'")
                        break

                if target_index != -1:
                    # Используем найденный индекс для чекбокса
                    checkbox = page.locator(f'div:nth-child({target_index + 1}) > .g-control-label > .g-control-label__indicator > .g-checkbox__control')
                    
                    if checkbox.count() > 0:
                        # Проверяем статус чекбокса
                        is_checked = checkbox.is_checked()
                        print(f"Статус чекбокса: {is_checked}")
                        
                        if not is_checked:
                            checkbox.check()
                            print("Чекбокс активирован!")
                        else:
                            print("Чекбокс уже активен")
                    else:
                        print("Чекбокс не найден по вычисленному индексу")
                else:
                    print("Партнер не найден в списке")
                # Поиск партнёра по ИНН
                search_input = page.locator('._modal__searchNewPartners_1iu8n_124 input')
                search_input.wait_for(state="visible", timeout=10000)
                search_input.fill("666777666")
                page.locator('.drop-wrapper').wait_for(state="visible", timeout=10000)
                # Ждем появления списка партнеров
                partners_list = page.locator('.drop-wrapper')
                partners_list.wait_for(state="visible", timeout=10000)
                # Нажимаем кнопку "Добавить"
                add_button = partners_list.locator('.g-button.g-button_view_normal.g-button_size_m.g-button_pin_round-round')
                page.wait_for_timeout(2000)
                add_button.click()
                page.wait_for_timeout(1000)
                page.mouse.click(10, 10)
                # Проверить оргу в таблице партнёров и активировать, если неактивна
                # Находим индекс элемента с текстом "666777666"
                all_partners = page.locator('._partnersList_1iu8n_149 > div')
                target_index = -1
                for i in range(all_partners.count()):
                    text = all_partners.nth(i).text_content().strip()
                    if "666777666" in text:
                        target_index = i
                        print(f"Найден партнер на позиции {i}: '{text}'")
                        break
                if target_index != -1:
                    # Используем найденный индекс для чекбокса
                    checkbox = page.locator(f'div:nth-child({target_index + 1}) > .g-control-label > .g-control-label__indicator > .g-checkbox__control')
                    if checkbox.count() > 0:
                        # Проверяем статус чекбокса
                        is_checked = checkbox.is_checked()
                        print(f"Статус чекбокса: {is_checked}") 
                        if not is_checked:
                            checkbox.check()
                            print("Чекбокс активирован!")
                        else:
                            print("Чекбокс уже активен")
                    else:
                        print("Чекбокс не найден по вычисленному индексу")
                else:
                    print("Партнер не найден в списке")
    with allure.step("Шаг 5: Cохранить группу партнёров"):
                try:
                    save_button = page.locator('text="Сохранить"')
                    save_button.click()
                    print("✅ Кнопка 'Сохранить' успешно нажата")
                except Exception as e:
                    print(f"❌ Ошибка при сохранении: {e}")
    with allure.step("Шаг 6: Найти созданную группу партнёров и открыть на редактирование"):
                # Выбрать тестовую организацию на странице партнёров
                org_on_main = page.locator('._controls_1iu8n_60')
                change_org_om_main = org_on_main.locator('.g-select.g-select_width_max._selector_z89or_6._component_1ozt1_16')
                change_org_om_main.click()
                select_list = page.locator('[data-qa="select-list"]')
                select_list.wait_for(state="visible", timeout=10000)
                page.locator('text="Test qa org"').click()
                # Найти созданную группу
                table_order = page.locator('.g-table.order-table')
                try:
                    row = table_order.get_by_role("row", name=random_name)
                    if row.count() > 0:
                        print(f"✅ Найдена группа партнеров: '{random_name}'")
                        # Клик на кнопку в строке
                        row.get_by_role("button").click()
                        print(f"✅ Кнопка в строке с '{random_name}' нажата")
                    else:
                        print(f"❌ Группа '{random_name}' не найдена в таблице, пробуем скроллинг")
                        
                        # РЕШЕНИЕ 2: Скроллинг и поиск в списке
                        print("Партнер не найден в видимой области, пробуем скроллинг")
                        
                        # Получаем контейнер со списком групп
                        groups_container = page.locator('.g-table.order-table, [class*="scroll"], [class*="container"], .g-table')
                        
                        # Пробуем найти партнера со скроллингом
                        max_scroll_attempts = 5
                        partner_found = False
                        
                        for attempt in range(max_scroll_attempts):
                            # Ищем снова после скролла
                            row = table_order.get_by_role("row", name=random_name)
                            if row.count() > 0 and row.first.is_visible():
                                row.first.get_by_role("button").click()
                                partner_found = True
                                print(f"✅ Партнер '{random_name}' найден после скроллинга (попытка {attempt + 1})")
                                break
                            
                            # Скроллим вниз
                            page.mouse.wheel(0, 300)
                            page.wait_for_timeout(1000)
                            print(f"↕️  Скролл вниз (попытка {attempt + 1})")
                        
                        if not partner_found:
                            print(f"❌ Партнер '{random_name}' не найден после скроллинга")
                            
                except Exception as e:
                    print(f"❌ Ошибка при поиске группы: {e}")
    with allure.step("Шаг 7: Редактирование группы: Добавить одну и удалить одну оргу в партнёрах"):
                # Находим партнера по ИНН и деактивируем чекбокс
                all_partners = page.locator('._partnersList_1iu8n_149 > div')
                target_index = -1
                for i in range(all_partners.count()):
                    text = all_partners.nth(i).text_content().strip()
                    if "666777666" in text:
                        target_index = i
                        print(f"Найден партнер на позиции {i}: '{text}'")
                        break
                if target_index != -1:
                    # Используем найденный индекс для чекбокса
                    checkbox = page.locator(f'div:nth-child({target_index + 1}) > .g-control-label > .g-control-label__indicator > .g-checkbox__control')
                    if checkbox.count() > 0:
                         # Прокручиваем к чекбоксу
                        checkbox.scroll_into_view_if_needed()
                        page.wait_for_timeout(1000)
                        # Проверяем текущее состояние
                        is_checked = checkbox.is_checked()
                        print(f"Состояние чекбокса до: {'активен' if is_checked else 'неактивен'}")
                        # Деактивируем чекбокс (uncheck)
                        checkbox.uncheck()
                        # Ждем применения изменения
                        page.wait_for_timeout(500)
                        # Проверяем что чекбокс действительно деактивирован
                        is_checked_after = checkbox.is_checked()
                        if not is_checked_after:
                            print("✅ Чекбокс успешно деактивирован!")
                        else:
                            print("❌ Чекбокс остался активным после uncheck")
                            # Пробуем кликнуть напрямую если uncheck не сработал
                            checkbox.click()
                    else:
                        print("Чекбокс не найден по вычисленному индексу")
                else:
                    print("Партнер не найден в списке")
                # Добавляем оргу в группу
                search_input = page.locator('._modal__searchNewPartners_1iu8n_124 input')
                search_input.wait_for(state="visible", timeout=10000)
                search_input.fill("7721820997")
                page.locator('.drop-wrapper').wait_for(state="visible", timeout=10000)
                # Ждем появления списка партнеров
                partners_list = page.locator('.drop-wrapper')
                partners_list.wait_for(state="visible", timeout=10000)
                # Нажимаем кнопку "Добавить"
                add_button = partners_list.locator('.g-button.g-button_view_normal.g-button_size_m.g-button_pin_round-round')
                page.wait_for_timeout(2000)
                add_button.click()
                page.wait_for_timeout(1000)
                page.mouse.click(10, 10)
                # Проверить оргу в таблице партнёров и активировать, если неактивна
                # Находим индекс элемента с текстом "7721820997"
                all_partners = page.locator('._partnersList_1iu8n_149 > div')
                target_index = -1
                for i in range(all_partners.count()):
                    text = all_partners.nth(i).text_content().strip()
                    if "7721820997" in text:
                        target_index = i
                        print(f"Найден партнер на позиции {i}: '{text}'")
                        break
                if target_index != -1:
                    # Используем найденный индекс для чекбокса
                    checkbox = page.locator(f'div:nth-child({target_index + 1}) > .g-control-label > .g-control-label__indicator > .g-checkbox__control')
                    if checkbox.count() > 0:
                        # Проверяем статус чекбокса
                        is_checked = checkbox.is_checked()
                        print(f"Статус чекбокса: {is_checked}") 
                        if not is_checked:
                            checkbox.check()
                            print("Чекбокс активирован!")
                        else:
                            print("Чекбокс уже активен")
                    else:
                        print("Чекбокс не найден по вычисленному индексу")
                else:
                    print("Партнер не найден в списке")
    with allure.step("Шаг 8: Cохранить отредактированную группу партнёров"):
                try:
                    save_button = page.locator('text="Сохранить"')
                    save_button.click()
                    print("✅ Кнопка 'Сохранить' успешно нажата")
                except Exception as e:
                    print(f"❌ Ошибка при сохранении: {e}")
                    
    with allure.step("Шаг 9: Нажимаем на кнопку Создать заказ"):
                order_button = page.locator('[data-qa="menu-new-form-create-button"]')
                order_button.wait_for(timeout=30000)
                order_button.click()

                # Блок "Моя организация"
    with allure.step("Шаг 10: 'Моя организация'"):
                # Выбор организации
                org_select = page.locator('[data-qa="order-form-forwarder-select"]')

                # Проверяем состояние элемента
                if org_select.is_enabled():
                    # Если поле активно: кликаем и выбираем организацию
                    org_select.click()
                     # Ждем появления выпадающего списка
                    page.wait_for_selector('.g-select-list', timeout=5000)
                    
                    # Выбираем опцию из выпадающего списка (более точный локатор)
                    page.locator('.g-select-list [role="option"]:has-text("Test qa org")').click()
                    print("✅ Организация 'Test qa org' выбрана из выпадающего списка")
                else:
                    expect(org_select.locator('.g-select-control__option-text')).to_have_text("Test qa org")
    with allure.step("Шаг 11: 'Добавить созданную группу партнёров в заказ'"):
                # 1. Перемотать к data-qa="order-form-distribution-public-switch"
                public_switch = page.locator('[data-qa="order-form-distribution-public-switch"]')
                public_switch.scroll_into_view_if_needed()

                # 2. Локатор для data-qa="order-form-distribution-group-label-*" с изменяющейся цифрой
                # Используем регулярное выражение для поиска по частичному совпадению
                group_label_pattern = re.compile(r'order-form-distribution-group-label-\d+')
                group_locator = page.locator(f'[data-qa*="order-form-distribution-group-label-"]:has-text("{random_name}")')

                # 3. Нажать на элемент с текстом из фейкера
                group_locator.click()
                

                # 4. Выводим в консоль, что группа найдена и прожата
                print(f"Группа с названием '{random_name}' найдена и прожата")
                page.wait_for_timeout(2000)
                # 5. Проверка, что добавлены два элемента с текстом "лайм ГП" и "тест Авто исполнитель"
                lime_gp_element = page.locator('[data-qa="main-button"]:has-text("Лайм_ГП")')
                test_auto_element = page.locator('[data-qa="main-button"]:has-text("тест Авто Исполнитель")')

                # 6. Проверка и вывод в консоль, что элементы обнаружены
                expect(lime_gp_element).to_be_visible()
                expect(test_auto_element).to_be_visible()
                print("✅ Элементы 'лайм ГП' и 'тест Авто исполнитель' обнаружены")

                # 7. Найти и нажать элемент: data-qa="order-form-clear-button""
                clear_button = page.locator('[data-qa="order-form-clear-button"]')
                clear_button.click()
    with allure.step("Шаг 12: 'Удалить группу партнёров'"):  
                #клик вне формы для её скрытия
                page.mouse.click(10, 10)
                 # Найти созданную группу
                table_order = page.locator('.g-table.order-table')
                try:
                    row = table_order.get_by_role("row", name=random_name)
                    if row.count() > 0:
                        # Клик на кнопку в строке
                        row.get_by_role("button").click()
                    else:            
                        # Получаем контейнер со списком групп
                        groups_container = page.locator('.g-table.order-table, [class*="scroll"], [class*="container"], .g-table')
                        
                        # Пробуем найти партнера со скроллингом
                        max_scroll_attempts = 5
                        partner_found = False
                        
                        for attempt in range(max_scroll_attempts):
                            # Ищем снова после скролла
                            row = table_order.get_by_role("row", name=random_name)
                            if row.count() > 0 and row.first.is_visible():
                                row.first.get_by_role("button").click()
                                partner_found = True
                                print(f"✅ Партнер '{random_name}' найден после скроллинга (попытка {attempt + 1})")
                                break
                            # Скроллим вниз
                            page.mouse.wheel(0, 300)
                            page.wait_for_timeout(1000)
                except Exception as e:
                    print(f"❌ Ошибка при поиске группы: {e}")
                #Удалить группу
                button = page.locator('._modal__bottom_buttons_1iu8n_107 button.g-button').first
                button.click()
                # Провериь, что такой группы больше нет в списке
                table_order = page.locator('.g-table.order-table')
                row = table_order.get_by_role("row", name=random_name)

                if row.count() > 0:
                    print(f"❌ НАЙДЕНО: Группа '{random_name}' найдена в таблице (не удалена)")
                else:
                    print(f"✅ ОК: Группа '{random_name}' удалена")