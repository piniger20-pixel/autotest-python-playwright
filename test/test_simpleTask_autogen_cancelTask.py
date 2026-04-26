import pytest
from playwright.sync_api import Page, expect
import requests
from urllib.parse import unquote
import re
import json
from typing import Dict
import psycopg2
import psycopg2.extras
from psycopg2 import sql
import time
import random
import os
from pathlib import Path
import allure
from config import EMPLOYEE_EMAIL
import logging
import config
from helpers import ui
from helpers.wait import wait_visible
import utils.common_steps as steps
from datetime import date, timedelta
log = logging.getLogger(__name__)

@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.critical
@pytest.mark.order_flow
@allure.feature("Orders")
@allure.story("simple tasks")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("автогенерация простых задач")
@allure.description("""Автоген через список на форме-> видимость задач-> отмена задачи создателем задачи
""")

def test_simpleTask_autogen_cancelTask(chromium_page: Page):
    page = chromium_page
    base_dir = Path(__file__).parent.parent
    # Для запуска теста Нужны организации 999988887 (заказчик) и 5003106773 (исполнитель)
    file_path = base_dir / "testdata" / "excel_1x1_flight_cancel.xlsm"
    #"Шаг 0. Установка сессии через insecure endpoint"
    steps.login(page)
    #Открываем форму создания заказа
    steps.open_order_form(page)
    # Выбираем загрузку заказа из файла
    steps.select_upload_order_from_file(page)
    # Загружаем файл
    steps.upload_file_on_order_form(page, file_path)
    # Проставить список задач в форме
    steps.select_task_list(page, "Список для автотеста")
    # Создание заказа(ов)"
    order_ids = steps.create_orders_from_file(page)
    # Переходим на таблицу заказов исполнителя
    steps.open_executor_orders(page)
    page.wait_for_timeout(4000)
    steps.close_filters(page)
    steps.filter_by(page, "ID заказа", order_ids[0])
    page.wait_for_timeout(1000)
    # Принимаем предложение торгов
    steps.accept_offer_1x1_from_table_order(page, order_ids[0])
    # Обновление с ожиданием загрузки
    page.reload()
    page.wait_for_load_state('load')
    # Отключаем оргу. заказчика в паенли организаций"
    steps.switch_state_of_organization(page, "Test qa org")
    # Открыть детализацию
    steps.open_details_order(page, order_ids[0])

    with allure.step("шаг. Проверка создания автозадач"):
        success = False
        for attempt in range(1, 5):
            print(f"\n{'='*50}")
            print(f"ПОПЫТКА {attempt}/5")
            # Ждем загрузку
            time.sleep(10)
            # Проверяем кнопку
            button = page.locator('button.g-button_view_normal:has-text("задачи")')
            if button.count() > 0:
                button_text = button.inner_text().strip()
                print(f"Текст кнопки: '{button_text}'")
                if "Скрыть" in button_text:
                    print("✅ Состояние 'Скрыть' достигнуто!")
                    success = True
                    break
                else:
                    print(f"⚠️ Текст: '{button_text}'")
            # Если не нашли "Скрыть" и это не последняя попытка
            if attempt < 5:
                print("🔄 Обновляем страницу и открываем детализацию...")
                # Обновляем страницу
                page.reload(wait_until="domcontentloaded")
                time.sleep(10)
                # Открываем детализацию
                order_link = page.locator(f'tr:has-text("{order_ids[0]}") [data-qa="order-link"]')
                order_link.wait_for(state="visible", timeout=5000)
                order_link.click()
        if success:
            print("\n✅ Проверка пройдена. Продолжаем тест...")
        else:
            print("\n❌ Кнопка не перешла в состояние 'Скрыть' за 3 попытки")
            raise AssertionError("Не удалось получить состояние 'Скрыть'")
        
    with allure.step("шаг. Проверяем контейнер со списком задач для исполнителя"):
        # Находим основной контейнер - изменяем локатор
        tasks_list = page.locator('.g-box.g-flex[class*="_tasksList_"][class$="_46"]')
        expect(tasks_list).to_be_visible(timeout=5000)
        print("✅ Контейнер списка задач найден")
        # Ищем все элементы с классом _taskContainer_4oglr_52 внутри контейнера - изменяем локатор
        task_containers = tasks_list.locator('div[class*="_taskContainer_"][class$="_52"]')
        
        # Получаем количество найденных элементов
        container_count = task_containers.count()
        print(f"Найдено элементов с классом: {container_count}")
        
        # Ассерт проверка - должен быть только один элемент
        assert container_count == 1, f"Ожидался 1 контейнер задачи, найдено {container_count}"
        print("✅ Проверка пройдена: только один контейнер задачи")

        # Обновление с ожиданием загрузки
        page.reload()
        page.wait_for_load_state('load')
        # Закрыть фильтры
        page.wait_for_timeout(1000)
        steps.close_filters(page)

    # Включаем оргу. заказчика в паенли организаций
    steps.switch_state_of_organization(page, "Test qa org")
    # Переходим на таблицу заказов заказчика
    steps.open_forwarder_orders(page)
    # Закрыть фильтры
    page.wait_for_timeout(2000)
    steps.close_filters(page)
    # Отфильтровать по ИД заказа
    steps.filter_by(page, "ID заказа", order_ids[0])
    page.wait_for_timeout(3000)
    steps.open_details_order(page, order_ids[0])
    
    with allure.step("шаг 14. Проверяем контейнер со списком задач для заказчика"):
        # Ждем загрузки детализации и проверяем кнопку задач
        page.wait_for_timeout(3000)
        
        # Проверяем и раскрываем задачи если они скрыты
        button = page.locator('button.g-button_view_normal:has-text("задачи")').first
        if button.count() > 0:
            button_text = button.inner_text().strip()
            print(f"Текст кнопки задач: '{button_text}'")
            if "Показать" in button_text:
                print("🔄 Раскрываем задачи...")
                button.click()
                page.wait_for_timeout(2000)
        
        # Находим основной контейнер - изменяем локатор
        tasks_list_2 = page.locator('.g-box.g-flex[class*="_tasksList_"][class$="_46"]')
        expect(tasks_list_2).to_be_visible(timeout=15000)
        print("✅ Контейнер списка задач найден")
        
        # Ищем все элементы с классом _taskContainer_4oglr_52 внутри контейнера - изменяем локатор
        task_containers_2 = tasks_list_2.locator('div[class*="_taskContainer_"][class$="_52"]')
        
        # Получаем количество найденных элементов
        container_count_2 = task_containers_2.count()
        print(f"Найдено элементов с классом {container_count_2}")
        
        # Ассерт проверка - должен быть два элемента
        assert container_count_2 == 2, f"Ожидался 2 контейнер задачи, найдено {container_count_2}"
        print("✅ Проверка пройдена: два контейнера задач")

    steps.cancel_simple_task(page, "Ускорить")
    page.mouse.click(10, 10)
    page.wait_for_timeout(1000)

    with allure.step("шаг 16. Проверка и включение чек бокса отмённёных задач"):
        # Открыть настройки видимости задач
        setting_button = page.locator('[style*="align-items: center"]:has-text("Задачи") svg[viewBox="0 0 16 16"]').first
        setting_button.wait_for(state="visible", timeout=5000)
        setting_button.click(force=True)
        # Проверка чекбокса отменённых задач
        label = page.locator('label:has-text("Скрыть отмененные задачи")').first
        label.wait_for(state="visible", timeout=5000)

        # Находим input checkbox внутри label
        checkbox = label.locator('input[type="checkbox"]')

        # Проверяем состояние чекбокса
        is_checked = checkbox.is_checked()

        if is_checked:
            # Чекбокс активен - деактивируем его
            label.click()  # Кликаем по label, это надежнее
            print("✅ Чекбокс дезактивирован")
        else:
            print("✅ Чекбокс уже отжат")
    with allure.step("шаг 17. Проверка отменённого элемента"):
        element = page.locator(':has-text("отозвано автором"):has-text("ускорить")')
        element.first.wait_for(state="visible", timeout=5000)
        assert element.count() > 0, "Элемент не найден"
        print("✅ УСПЕХ: Найден элемент с текстами 'отозвано автором' и 'ускорить'")
        page.wait_for_timeout(1000)
        button_close = page.locator('.g-button.g-button_view_flat.g-button_size_m.g-button_pin_round-round').first
        button_close.click()
        page.wait_for_timeout(2000)
        steps.close_filters(page)

if __name__ == "__main__":
    log.setLevel(logging.DEBUG)
    test_simpleTask_autogen_cancelTask()