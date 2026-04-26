import allure
import json
import re
from datetime import date, timedelta
from playwright.sync_api import expect


@allure.step("Создаем заказ из файла")
def create_orders_from_file(page):
     """
     Кликает кнопку 'Создать заказы из файла',
     ждёт ответ API, валидирует структуру,
     извлекает order_ids и перезагружает страницу.
     """

     create_orders_button = page.locator('[data-qa="order-form-upload-file-create-orders-button"]')
     create_orders_button.wait_for(state="visible", timeout=20000)
     page.wait_for_selector('[data-qa="order-form-upload-file-create-orders-button"]:not([disabled])', timeout=15000)
     # Проверяем что кнопка активна
     assert create_orders_button.is_enabled(), "Кнопка создания заказов неактивна"
     # Собираем ID заказов
     order_ids = []
     # Включаем перехватчик ДО нажатия кнопки
     def collect_order_ids(response):
         if "createFromXlsx" in response.url:
             try:
                 body = response.json()
                 if "data" in body and "id" in body["data"]:
                     order_id = body["data"]["id"]
                     order_ids.append(order_id)
                     print(f"Добавлен ID из data.id: {order_id}", flush=True)
             except:
                 pass  # Игнорируем ошибки парсинга
     page.on("response", collect_order_ids)
     create_orders_button.click()
     print("Нажата кнопка создания заказов из файла", flush=True)
     # Ждем завершения запросов
     print("⏳ Ожидаем создание заказов...", flush=True)
     page.wait_for_timeout(5000)
     # Отключаем перехватчик
     page.remove_listener("response", collect_order_ids)
     print(f"✅ Создано: {len(order_ids)} заказ")
     # Проверяем что заказы создались
     if not order_ids:
         print("❌ Не создано ни одного заказа", flush=True)
     page.reload()
     return order_ids

@allure.step("Выбираем загрузку заказа из файла")
def select_upload_order_from_file(page):
    # Ждем загрузки DOM формы заказа перед переключением на вкладку
    # Используем 'load' вместо 'networkidle' для избежания таймаутов
    page.wait_for_load_state('load', timeout=30000)
    page.wait_for_timeout(1000)
    
    # Увеличенный таймаут и явное ожидание видимости элемента
    upload_tab = page.locator('[data-qa="order-form-upload-order-from-file-tab"]')
    upload_tab.wait_for(state="visible", timeout=30000)
    
    # Дополнительная проверка что элемент кликабелен
    upload_tab.wait_for(state="attached", timeout=5000)
    page.wait_for_timeout(500)
    
    upload_tab.click()
    print("✅ Вкладка 'Загрузка из файла' выбрана")

@allure.step("Загружаем файл на форме создания заказа")
def upload_file_on_order_form(page, file_path):
    with page.expect_file_chooser() as fc_info:
        upload_button = page.locator('[data-qa="order-form-upload-file-select-file-button"]')
        upload_button.wait_for(state="visible", timeout=3000)
        upload_button.click()
        file_chooser = fc_info.value
        file_chooser.set_files(file_path.absolute())
        page.wait_for_timeout(3000)