import allure
from playwright.sync_api import Page

from utils.steps import order_form_steps as form
from utils.steps import orders_api_steps as api
import utils.common_steps as steps



@allure.step(
    "Создаём заказ на торги: шаблон '{template_name}', "
    "погрузка +{pickup_date_offset} дн., разгрузка +{delivery_date_offset} дн."
)
def create_order_on_auction(
    page,
    template_name: str,
    pickup_date_offset: int,
    delivery_date_offset: int,
    pickup_calendar_index: int = 0,
    delivery_calendar_index: int = 1,
) -> str:
    """
    Business-шаг:
    1. Открыть форму создания заказа
    2. Выбрать шаблон
    3. Выбрать дату погрузки
    4. Выбрать дату разгрузки
    5. Сохранить заказ
    """

    # 1. Открываем форму
    steps.open_order_form(page)

    # 2. Выбираем шаблон
    steps.select_template(page, template_name)

    # 3. Дата погрузки
    steps.pick_date(
        page,
        calendar_index=pickup_calendar_index,
        days_ahead=pickup_date_offset,
    )

    # 4. Дата разгрузки
    steps.pick_date(
        page,
        calendar_index=delivery_calendar_index,
        days_ahead=delivery_date_offset,
    )

    # 5. Сохраняем заказ
    order_id = steps.save_order(page)

    return order_id

import allure
from playwright.sync_api import Page

from utils.steps import order_form_steps as form
from utils.steps import orders_api_steps as api


@allure.step("Business: создать заказ с несколькими грузами и отправить на Торги")
def create_order_with_multiple_shipments_and_send_to_auction(page: Page) -> str:
    form.open_order_form(page)
    form.clear_order_form(page)

    form.fill_my_org(page, org_name="Test qa org")
    form.fill_cargo_owner_by_inn(page, inn="6452135389", company_menu_text="ВЕЗЕТ ВАМ")

    form.fill_transport_block(page, weight="10", volume="45", pallets="18", body_type="Борт")

    # Груз 1 (2 грузоместа)
    form.fill_shipment0_two_packages(page)
    form.fill_load_unload_for_shipment0(page)
    form.set_dates_for_shipment0(page, load_days=5, unload_days=7)

    # Груз 2 (1 грузоместо)
    form.add_shipment1_one_package(page)
    form.fill_load_unload_for_shipment1(page)
    form.set_dates_for_shipment1(page, load_days=3, unload_days=4)

    # Дублировать груз 2
    form.duplicate_shipment1(page)

    # Таб “Торги” + настройки
    form.open_distribution_to_auction(page)
    form.select_executors_group(page, group_label_qa="order-form-distribution-group-label-5")
    form.fill_auction_block(page, minutes="10", amount="61200", step="100", buy_now="40000",
                            hide_bids=True, decrease_only=True)

    # Отправить на торги (API create)
    order_id = api.save_order_to_auction(page)
    return order_id


@allure.step("Business: Создаём заказ из Excel и переходим к торгам")
def create_order_from_excel_and_open_auction(page: Page, file_path, email: str):
    """
    Бизнес-шаг: Авторизация, создание заказа из Excel, переход к таблице исполнителя.

    Args:
        page: Playwright page object
        file_path: Путь к Excel файлу
        email: Email для авторизации

    Returns:
        list: Список ID созданных заказов
    """
    steps.login(page, email)
    steps.open_order_form(page)
    steps.select_upload_order_from_file(page)
    steps.upload_file_on_order_form(page, file_path)
    order_ids = steps.create_orders_from_file(page)

    steps.open_executor_orders(page)
    page.wait_for_timeout(1000)
    steps.close_filters(page)
    steps.filter_by(page, "ID заказа", order_ids[0])
    page.wait_for_timeout(3000)

    return order_ids


@allure.step("Business: Создаём заказ из Excel и переходим к заказу заказчика")
def create_order_from_excel_and_open_forwarder_orders(page: Page, file_path, email: str):
    """
    Бизнес-шаг: Авторизация, создание заказа из Excel, переход к таблице заказчика

    Args:
        page: Playwright page object
        file_path: Путь к Excel файлу
        email: Email для авторизации

    Returns:
        list: Список ID созданных заказов
    """
    steps.login(page, email)
    steps.open_order_form(page)
    steps.select_upload_order_from_file(page)
    steps.upload_file_on_order_form(page, file_path)
    order_ids = steps.create_orders_from_file(page)

    steps.open_forwarder_orders(page)
    page.wait_for_timeout(1000)
    steps.close_filters(page)
    steps.filter_by(page, "ID заказа", order_ids[0])
    page.wait_for_timeout(3000)

    return order_ids

@allure.step("Business: Проверяем механики торгов и открываем окно ставки")
def verify_auction_mechanics_and_open_bet(page: Page, expected_mechanics: set, amount_no_vat: str, amount_with_vat: str, vat_rate: str, org_name: str):
    """
    Бизнес-шаг: Проверка статуса, механик торгов, открытие окна ставки с проверкой НДС и выбор организации.

    Args:
        page: Playwright page object
        expected_mechanics: Множество ожидаемых механик торгов
        amount_no_vat: Сумма без НДС
        amount_with_vat: Сумма с НДС
        vat_rate: Ставка НДС
        org_name: Название организации для выбора
    """
    steps.assert_order_status_in_first_row(page, "Торги")
    steps.assert_trade_mechanics_in_table(page, expected_mechanics)
    steps.open_bet_window_from_executor_table(page)
    steps.assert_vat_display_in_bet_window(page, amount_no_vat, amount_with_vat, vat_rate)
    steps.open_bet_form(page)
    steps.select_organization_for_bet(page, org_name)


@allure.step("Business: Проверяем все механики валидации торгов")
def validate_all_auction_mechanics(page: Page):
    """
    Бизнес-шаг: Проверка всех механик валидации торгов (не выше заявленной, шаг торгов).
    """
    # Проверка "Не выше заявленной стоимости"
    with allure.step("Проверяем механику 'Не выше заявленной стоимости'"):
        steps.enter_bet_amount(page, "20000")
        print("✅ Ставка 20000, превышающая заявленную стоимость введена")

        expected_errors = [
            "Ваша ставка не должна превышать заявленную стоимость 10 000 ₽",
            "Ваша ставка c НДС не должна превышать заявленную стоимость 12 000 ₽ с НДС"
        ]
        steps.assert_bet_validation_errors(page, expected_errors)
        steps.assert_bet_button_disabled(page)

    # Проверка "Шаг торгов"
    with allure.step("Проверяем механику 'Шаг торгов'"):
        steps.enter_bet_amount(page, "5555")
        print("✅ Ставка 5555, не соответствующая шагу торгов введена")

        expected_errors = ["Соблюдайте шаг торгов: 100 ₽, возможны суммы 5 500 ₽ или 5 600 ₽"]
        steps.assert_bet_validation_errors(page, expected_errors)
        steps.assert_bet_button_disabled(page)


@allure.step("Business: Делаем ставку с НДС и проверяем результат")
def make_and_verify_bet_with_vat(page: Page, amount: str, amount_display: str, amount_with_vat: str, vat_amount: str, vat_rate: str):
    """
    Бизнес-шаг: Создание ставки с НДС и проверка её отображения как лучшей.

    Args:
        page: Playwright page object
        amount: Сумма ставки для ввода
        amount_display: Сумма для отображения (с пробелами)
        amount_with_vat: Сумма с НДС для отображения
        vat_amount: Сумма НДС
        vat_rate: Ставка НДС
    """
    steps.enter_bet_amount(page, amount)
    steps.submit_bet(page, amount)
    steps.assert_best_bet_with_vat(page, amount_display, amount_with_vat, vat_amount, vat_rate)


@allure.step("Business: Проверяем механику 'Только на понижение' и делаем ставку без НДС")
def validate_decrease_and_make_bet_without_vat(page: Page, org_name: str, invalid_amount: str, valid_amount: str, amount_display: str):
    """
    Бизнес-шаг: Выбор организации без НДС, проверка механики "Только на понижение" и создание валидной ставки.

    Args:
        page: Playwright page object
        org_name: Название организации не плательщика НДС
        invalid_amount: Невалидная сумма (не на понижение)
        valid_amount: Валидная сумма ставки
        amount_display: Сумма для отображения (с пробелами)
    """
    steps.open_bet_form(page)
    page.wait_for_timeout(500)
    steps.select_organization_for_bet(page, org_name)

    # Проверка механики "Только на понижение"
    steps.enter_bet_amount(page, invalid_amount)
    steps.submit_bet(page, invalid_amount)
    steps.assert_bet_not_decrease_error(page)

    # Делаем валидную ставку
    steps.enter_bet_amount(page, valid_amount)
    steps.submit_bet(page, valid_amount)
    steps.assert_best_bet_without_vat(page, amount_display)


@allure.step("Business: Завершаем торги выбором победителя")
def complete_auction_with_winner(page: Page, order_id: str):
    """
    Бизнес-шаг: Переход в таблицу заказчика, выбор и подтверждение победителя торгов.

    Args:
        page: Playwright page object
        order_id: ID заказа

    Returns:
        str: Статус торгов после завершения
    """
    page.reload()
    page.wait_for_load_state('load')
    steps.close_filters(page)

    steps.open_forwarder_orders(page)
    page.wait_for_timeout(1000)
    steps.close_filters(page)
    steps.filter_by(page, "ID заказа", order_id)

    steps.open_auction_window_from_customer_table(page)
    steps.select_auction_winner(page)
    status = steps.confirm_auction_winner(page)

    page.reload()
    page.wait_for_load_state('load')
    steps.close_filters(page)

    return status


@allure.step("Business: Создаём заказы из Excel и проверяем их в таблице Заказчика")
def create_orders_from_excel_and_verify_in_table(page: Page, file_path, email: str) -> list:
    """
    Бизнес-шаг: Полный цикл создания заказов из Excel и проверки их отображения.

    1. Авторизация
    2. Открытие формы создания заказа
    3. Загрузка Excel файла
    4. Создание заказов
    5. Переход в таблицу Заказчика
    6. Фильтрация по ID заказов
    7. Проверка отображения всех заказов

    Args:
        page: Playwright page object
        file_path: Путь к Excel файлу
        email: Email для авторизации

    Returns:
        list: Список ID созданных заказов
    """
    # Авторизация и создание заказов
    steps.login(page, email)
    steps.open_order_form(page)
    steps.select_upload_order_from_file(page)
    steps.upload_file_on_order_form(page, file_path)
    order_ids = steps.create_orders_from_file(page)

    if not order_ids:
        import pytest
        pytest.fail("Нет созданных заказов для проверки")

    print("\n" + "✅ " + "="*44 + " ✅")
    print(f"✅ Создано заказов: {len(order_ids)}")
    print("✅ " + "="*44 + " ✅\n")

    # Переход в таблицу и проверка
    steps.open_forwarder_orders(page)
    page.wait_for_timeout(1000)
    steps.close_filters(page)

    # Фильтрация по всем ID заказов
    steps.filter_by_multiple_order_ids(page, order_ids)

    # Проверка отображения всех заказов
    steps.assert_multiple_orders_in_table(page, order_ids)

    steps.close_filters(page)

    return order_ids


@allure.step("Business: Создаём два заказа из Excel и принимаем предложения")
def create_two_orders_and_accept_offers(page: Page, file_path) -> list:
    """
    Бизнес-шаг: Создание двух заказов из Excel и принятие предложений по обоим.

    Args:
        page: Playwright page object
        file_path: Путь к Excel файлу

    Returns:
        list: Список ID созданных заказов
    """
    steps.login(page)
    steps.open_order_form(page)
    steps.select_upload_order_from_file(page)
    steps.upload_file_on_order_form(page, file_path)
    order_ids = steps.create_orders_from_file(page)

    print(f"\n🔍 Отладка: Получены ID заказов из Excel:")
    for i, order_id in enumerate(order_ids):
        print(f"   order_ids[{i}] = {order_id}")

    steps.open_executor_orders(page)
    page.wait_for_timeout(4000)
    steps.close_filters(page)

    # Фильтруем и принимаем предложения по обоим заказам
    steps.filter_by(page, "ID заказа", order_ids[0])
    page.wait_for_timeout(3000)
    steps.filter_by(page, "ID заказа", order_ids[1])
    page.wait_for_timeout(3000)

    # Принимаем предложение для первого заказа
    steps.accept_offer_1x1_from_table_order(page, order_ids[0])
    # Дополнительная пауза перед принятием второго предложения
    page.wait_for_timeout(3000)

    # Перезагружаем страницу и восстанавливаем фильтры для второго заказа
    page.reload()
    page.wait_for_load_state('load')
    page.wait_for_timeout(3000)
    steps.close_filters(page)
    
    # Фильтруем только второй заказ для принятия предложения
    steps.filter_by(page, "ID заказа", order_ids[1])
    page.wait_for_timeout(3000)
    
    # Принимаем предложение для второго заказа
    steps.accept_offer_1x1_from_table_order(page, order_ids[1])

    page.reload()
    # Используем 'load' вместо 'networkidle' для избежания таймаутов
    page.wait_for_load_state('load')
    page.wait_for_timeout(3000)

    # Ждем пока оба заказа перейдут в статус "В работе"
    steps.close_filters(page)

    # Проверяем первый заказ
    steps.filter_by(page, "ID заказа", order_ids[0])
    page.wait_for_timeout(2000)
    steps.wait_for_order_status_change(page, "В работе", max_attempts=20, wait_seconds=6)
    steps.close_filters(page)

    # Проверяем второй заказ
    steps.filter_by(page, "ID заказа", order_ids[1])
    page.wait_for_timeout(2000)
    steps.wait_for_order_status_change(page, "В работе", max_attempts=20, wait_seconds=6)
    steps.close_filters(page)

    # Фильтруем оба заказа для последующего выбора чекбоксами
    steps.filter_by(page, "ID заказа", order_ids[0])
    page.wait_for_timeout(2000)
    steps.filter_by(page, "ID заказа", order_ids[1])
    page.wait_for_timeout(2000)

    print(f"\n🔍 Отладка: Возвращаем order_ids: {order_ids}\n")

    return order_ids


@allure.step("Business: Создаём рейс с первым заказом и проверяем его")
def create_flight_with_first_order_and_verify(page: Page, order_ids: list) -> str:
    """
    Бизнес-шаг: Создание рейса с первым заказом и проверка его наличия в таблице.

    Args:
        page: Playwright page object
        order_ids: Список ID заказов

    Returns:
        str: ID созданного рейса
    """
    # Фильтруем по первому заказу чтобы гарантировать правильный выбор
    steps.close_filters(page)
    steps.filter_by(page, "ID заказа", order_ids[0])
    page.wait_for_timeout(2000)

    print(f"\n🔍 Создаем рейс с первым заказом: {order_ids[0]}")

    # Выбираем первый заказ (теперь он единственный в отфильтрованной таблице)
    steps.select_order_checkbox(page, 0)

    # Создаем рейс
    flight_id = steps.create_flight_from_bottom_menu(page)

    # Переходим на вкладку "В Рейсе"
    steps.switch_to_tab(page, "В Рейсе")
    page.wait_for_timeout(2000)
    steps.close_filters(page)

    # Фильтруем по номеру рейса
    steps.filter_by(page, "Номер рейса", flight_id)

    # Проверяем рейс в таблице
    steps.assert_flight_in_table(page, flight_id)

    # Проверяем что первый заказ в рейсе
    steps.assert_order_in_flight(page, flight_id, order_ids[0])

    return flight_id


@allure.step("Business: Добавляем второй заказ к существующему рейсу")
def add_second_order_to_flight(page: Page, flight_id: str, order_ids: list):
    """
    Бизнес-шаг: Добавление второго заказа к существующему рейсу.

    Args:
        page: Playwright page object
        flight_id: ID рейса
        order_ids: Список ID заказов
    """
    steps.close_filters(page)

    # Переходим на вкладку "Все"
    steps.switch_to_tab(page, "Все")
    page.wait_for_timeout(2000)
    steps.close_filters(page)

    # Фильтруем по второму заказу
    steps.filter_by(page, "ID заказа", order_ids[1])
    page.wait_for_timeout(2000)

    # Выбираем второй заказ (теперь он первый в отфильтрованной таблице)
    steps.select_order_checkbox(page, 0)

    # Открываем сайдбар создания рейса
    steps.open_flight_saidbar_trgouht_bottom_menu(page)

    # Добавляем заказ к рейсу
    steps.add_order_to_ready_flight(page, flight_id, 5000)
    steps.type_saveflight_button(page)

    # Ждем сохранения изменений (увеличено время)
    page.wait_for_timeout(5000)


@allure.step("Business: Проверяем рейс со стороны заказчика")
def verify_flight_from_forwarder_side(page: Page, flight_id: str, order_ids: list):
    """
    Бизнес-шаг: Проверка рейса со стороны заказчика.

    Args:
        page: Playwright page object
        flight_id: ID рейса
        order_ids: Список ID заказов
    """
    steps.close_filters(page)
    steps.open_forwarder_orders(page)

    # Переходим на вкладку "В Рейсе"
    steps.switch_to_tab(page, "В Рейсе")
    page.wait_for_timeout(2000)
    steps.close_filters(page)

    # Фильтруем по номеру рейса
    steps.filter_by(page, "Номер рейса", flight_id)
    page.wait_for_timeout(3000)

    # Проверяем рейс с повторными попытками
    for attempt in range(5):
        try:
            steps.assert_flight_in_table(page, flight_id)
            break
        except:
            if attempt < 4:
                page.reload()
                page.wait_for_timeout(3000)
            else:
                raise

    # Проверяем что оба заказа в рейсе
    steps.assert_multiple_orders_in_flight(page, flight_id, order_ids)


@allure.step("Business: Проверяем грузы в деталях рейса")
def verify_shipments_in_flight_details(page: Page, flight_id: str):
    """
    Бизнес-шаг: Проверка наличия грузов в деталях рейса.

    Args:
        page: Playwright page object
        flight_id: ID рейса
    """
    # Открываем детали рейса
    steps.open_flight_details(page, flight_id)

    # Проверяем наличие грузов в маршруте
    steps.assert_shipments_in_route(page, "Заказ № 2, тест", min_count=2)

    # Закрываем детали
    steps.close_flight_details(page)


@allure.step("Business: Создаём заказ из Excel и принимаем предложение 1x1")
def create_order_from_excel_and_accept_offer(page: Page, file_path) -> str:
    """
    Бизнес-шаг: Создание заказа из Excel, переход к исполнителю и принятие предложения.

    Args:
        page: Playwright page object
        file_path: Путь к Excel файлу

    Returns:
        str: ID созданного заказа
    """
    steps.login(page)
    steps.open_order_form(page)
    steps.select_upload_order_from_file(page)
    steps.upload_file_on_order_form(page, file_path)
    order_ids = steps.create_orders_from_file(page)

    steps.open_executor_orders(page)
    page.wait_for_timeout(4000)
    steps.close_filters(page)

    steps.filter_by(page, "ID заказа", order_ids[0])
    page.wait_for_timeout(1000)

    steps.assert_order_in_table(page, order_ids[0], "Торги")
    steps.accept_offer_1x1_from_table_order(page, order_ids[0])

    page.wait_for_timeout(3000)
    page.reload()
    page.wait_for_load_state('load')
    page.wait_for_timeout(1000)

    steps.assert_order_in_table(page, order_ids[0], "В работе")

    return order_ids[0]


@allure.step("Business: Создаём рейс для заказа и проверяем его")
def create_flight_for_order_and_verify(page: Page, order_id: str) -> str:
    """
    Бизнес-шаг: Создание рейса для заказа через меню заказа.

    Args:
        page: Playwright page object
        order_id: ID заказа

    Returns:
        str: ID созданного рейса
    """
    steps.open_order_menu(page, 0)
    flight_id = steps.create_flight(page)
    steps.close_filters(page)

    return flight_id


@allure.step("Business: Отменяем заказ заказчиком и проверяем детали")
def cancel_order_by_customer_and_verify(page: Page, order_id: str):
    """
    Бизнес-шаг: Отмена заказа заказчиком с проверкой причины и комментария.

    Args:
        page: Playwright page object
        order_id: ID заказа
    """
    steps.open_forwarder_orders(page)
    steps.close_filters(page)
    steps.filter_by(page, "ID заказа", order_id)
    page.wait_for_timeout(3000)

    steps.open_order_menu(page, 0)
    steps.cancel_order_by_customer(page)

    page.reload(wait_until="domcontentloaded")
    page.wait_for_timeout(5000)

    # Проверяем детали в таблице заказчика
    steps.open_details_order(page, order_id)
    page.wait_for_timeout(1000)
    steps.open_comment_order(page)
    steps.assert_cancellation_reason_and_comment(page)
    steps.close_details_order(page)

    # Включаем архивные заказы
    steps.show_archived_orders(page)

    # Проверяем детали в таблице исполнителя
    steps.open_order_by_status_with_retry(page, "Отзыв из исполнения")
    steps.open_comment_order(page)
    steps.assert_cancellation_reason_and_comment(page)
    steps.close_details_order(page)
    steps.hide_archived_orders(page)


@allure.step("Business: Отменяем заказ исполнителем и проверяем детали в черновике заказчика и дарксайде исполнителя")
def cancel_order_by_executor_and_verify(page: Page, order_id: str):
    """
    Бизнес-шаг: Отмена заказа заказчиком с проверкой причины и комментария.

    Args:
        page: Playwright page object
        order_id: ID заказа
    """
    steps.open_executor_orders(page)
    steps.close_filters(page)
    steps.filter_by(page, "ID заказа", order_id)
    page.wait_for_timeout(3000)

    steps.open_order_menu(page, 0)
    steps.cancel_order_by_executor(page)

    page.reload(wait_until="domcontentloaded")
    page.wait_for_timeout(5000)

    # Открываем заказы заказчика и находим заказ
    steps.open_forwarder_orders(page)
    page.wait_for_timeout(2000)
    steps.close_filters(page)
    steps.filter_by(page, "ID заказа", order_id)
    
    # Проверяем детали в таблице заказчика
    steps.open_details_order(page, order_id)
    page.wait_for_timeout(2000)
    steps.open_comment_order(page)
    steps.assert_cancellation_reason_and_comment(page, reason="Ошибочно активировал", comment="тест по отмене заказа исполнителем")
    steps.close_details_order(page)
    steps.close_filters(page)

    # ВОзвращаемся на страницу исполнителя и включаем архивные заказы
    steps.open_executor_orders(page)
    steps.show_archived_orders(page)

    # Проверяем детали в таблице исполнителя
    steps.open_order_by_status_with_retry(page, "Отзыв из исполнения")
    steps.open_comment_order(page)
    steps.assert_cancellation_reason_and_comment(page, reason="Ошибочно активировал", comment="тест по отмене заказа исполнителем")
    steps.close_details_order(page)
    steps.close_filters(page)
    steps.hide_archived_orders(page)


@allure.step("Business: Проверяем статус рейса после отмены заказа")
def verify_flight_cancelled_after_order_cancellation(page: Page, flight_id: str, skip_forwarder_steps: bool = False):
    """
    Бизнес-шаг: Проверка что рейс перешел в статус "Отменен до начала".

    Args:
        page: Playwright page object
        flight_id: ID рейса
    """
    
    if not skip_forwarder_steps:
        steps.open_forwarder_orders(page)
        page.wait_for_timeout(2000)
        steps.close_filters(page)
        steps.open_executor_orders(page)
    steps.switch_to_tab(page, "В Рейсе")
    page.wait_for_timeout(2000)
    steps.close_filters(page)

    steps.filter_by(page, "Номер рейса", flight_id)
    steps.assert_flight_in_table(page, flight_id)

    steps.open_flight_details(page, flight_id)
    page.wait_for_timeout(2000)
    steps.assert_flight_status(page, "Отменен до начала")
    steps.close_flight_details(page)
    steps.close_filters(page)


@allure.step("Business: Подготовка - удаление старых БШУ для организации '{org_name}'")
def cleanup_old_templates(page: Page, org_name: str = "Test qa org"):
    """
    Бизнес-шаг: Переход к шаблонам, применение фильтров и удаление старых БШУ.

    Args:
        page: Playwright page object
        org_name: Название организации
    """
    steps.navigate_to_templates_page(page)
    steps.apply_template_filters(page, template_type="Базовый", org_name=org_name)
    steps.delete_all_filtered_templates(page)


@allure.step("Business: Создание БШУ по умолчанию для '{org_name}'")
def create_default_basic_template(
    page: Page,
    org_name: str,
    doc_days: str,
    payment_days: str
) -> tuple:
    """
    Бизнес-шаг: Создание и активация БШУ по умолчанию.

    Args:
        page: Playwright page object
        org_name: Название организации
        doc_days: Количество дней для документов
        payment_days: Количество дней для платежа

    Returns:
        tuple: (template_id, trans_id)
    """
    template_id, trans_id = steps.create_basic_template(
        page,
        org_name=org_name,
        doc_days=doc_days,
        payment_days=payment_days,
        set_as_default=True
    )

    if not template_id or not trans_id:
        import pytest
        pytest.fail("Не удалось создать БШУ")

    return template_id, trans_id


@allure.step("Business: Загрузка заказа из Excel с проверкой переменных шаблона")
def upload_order_and_verify_template_variables(
    page: Page,
    file_path,
    expected_trans_id: str,
    expected_doc_delay: str,
    expected_payment_delay: str
) -> bool:
    """
    Бизнес-шаг: Загрузка Excel файла и проверка переменных шаблона через API.

    Args:
        page: Playwright page object
        file_path: Путь к Excel файлу
        expected_trans_id: Ожидаемый trans_id шаблона
        expected_doc_delay: Ожидаемое значение отсрочки документов
        expected_payment_delay: Ожидаемое значение отсрочки платежа

    Returns:
        bool: True если все проверки пройдены
    """
    steps.open_order_form(page)
    steps.select_upload_order_from_file(page)

    # Переменная для хранения данных ответа
    variables_data = None

    # Обработчик для перехвата ответа
    def handle_response(response):
        nonlocal variables_data
        if "conditionsTemplate/variables/get/v0" in response.url and response.ok:
            try:
                variables_data = response.json()
            except Exception as e:
                print(f"⚠️ Не удалось получить JSON из ответа: {e}")

    # Подписываемся на события response
    page.on("response", handle_response)

    try:
        # Загружаем файл
        steps.upload_file_on_order_form(page, file_path)

        # Ждем немного для обработки ответа
        page.wait_for_timeout(2000)

        # Отписываемся от событий
        page.remove_listener("response", handle_response)

        # Проверяем что данные получены
        if not variables_data:
            print("❌ Не удалось получить данные переменных шаблона")
            return False

        # Проверяем соответствие trans_id
        check_results = {}
        check_results["trans_id совпадение"] = expected_trans_id == variables_data["data"]["templateId"]
        print(f"{'✅' if check_results['trans_id совпадение'] else '❌'} 1. trans_id: {expected_trans_id} == {variables_data['data']['templateId']}")

        # Проверки key-value
        for variable in variables_data["data"]["variables"]:
            if variable["key"] == "deadlineDocumentCalendarDay":
                check_results["deadlineDocumentCalendarDay"] = variable["value"] == expected_doc_delay
                status = "✅" if variable["value"] == expected_doc_delay else f"❌ (получено: {variable['value']})"
                print(f"{status} 2. {variable['key']} = {variable['value']}")
            elif variable["key"] == "deferredPaymentWorkDay":
                check_results["deferredPaymentWorkDay"] = variable["value"] == expected_payment_delay
                status = "✅" if variable["value"] == expected_payment_delay else f"❌ (получено: {variable['value']})"
                print(f"{status} 3. {variable['key']} = {variable['value']}")

        print(f"\n📊 Итог: {sum(check_results.values())}/{len(check_results)} проверок пройдено")

        return all(check_results.values())

    except Exception as e:
        print(f"❌ Ошибка при проверке переменных шаблона: {e}")
        page.remove_listener("response", handle_response)
        return False


@allure.step("Business: Создание заказов из Excel и переход к таблице заказчика")
def create_orders_and_navigate_to_forwarder_table(page: Page, order_id: str) -> list:
    """
    Бизнес-шаг: Создание заказов из файла и переход к таблице заказчика с фильтрацией.

    Args:
        page: Playwright page object
        order_id: ID заказа для фильтрации

    Returns:
        list: Список ID созданных заказов
    """
    order_ids = steps.create_orders_from_file(page)

    if not order_ids:
        import pytest
        pytest.fail("Не удалось создать заказы из файла")

    steps.open_forwarder_orders(page)
    page.wait_for_timeout(5000)
    steps.close_filters(page)
    page.wait_for_timeout(2000)
    steps.filter_by(page, "ID заказа", order_id)
    page.reload()
    page.wait_for_load_state('load')

    return order_ids


@allure.step("Business: Проверка БШУ в детализации заказа")
def verify_template_in_order_details_flow(page: Page) -> bool:
    """
    Бизнес-шаг: Открытие детализации заказа и проверка группировки элементов БШУ.

    Args:
        page: Playwright page object

    Returns:
        bool: True если все проверки пройдены
    """
    # Открыть детализацию
    order_link = page.locator('[data-qa="order-link"]')
    order_link.wait_for(state="visible", timeout=10000)
    order_link.click()

    # Проверить группировку элементов
    verification_results = steps.verify_template_in_order_details(page)

    # Закрыть детализацию
    page.wait_for_timeout(1000)
    page.mouse.click(10, 10)
    steps.close_filters(page)

    return verification_results["all_checks_passed"]


@allure.step("Business: Тестируем механику Автовыбор + Автопродление")
def test_autoselect_with_duration_mechanics(page: Page, order_id: str):
    """
    Бизнес-шаг: Полный цикл проверки механик Автовыбор + Автопродление.

    1. Проверка статуса и механик торгов у исполнителя
    2. Проверка таймера до ставки (< 1 минуты)
    3. Создание ставки
    4. Проверка автопродления в детализации и таблице исполнителя
    5. Проверка автопродления в таблице заказчика
    6. Ожидание завершения торгов и автовыбора победителя
    7. Проверка заказа в статусе "В работе"

    Args:
        page: Playwright page object
        order_id: ID заказа
    """
    import utils.common_steps as steps
    import time

    # Проверка статуса и механик торгов
    steps.assert_order_status_in_first_row(page, "Торги")
    print("✅ Статус заказа корректный: Торги")

    expected_mechanics = {"Закрытые торги", "Автовыбор", "Автопродление"}
    steps.assert_trade_mechanics_in_table(page, expected_mechanics)

    # Проверка таймера до ставки (< 1 минуты)
    steps.assert_auction_timer_less_than_60_seconds(page, "таблице Исполнителя")

    # Создание ставки
    steps.open_bet_window_from_executor_table(page)
    steps.open_bet_form(page)
    steps.select_organization_for_bet(page, "Autotests_GP_НДС")

    with allure.step("Ставим валидную ставку с НДС"):
        steps.enter_bet_amount(page, "5000")
        steps.submit_bet(page, "5000")
        print("✅ Валидная ставка 5000 с НДС, сделана")
        page.wait_for_timeout(1000)

    # Проверка автопродления в детализации
    steps.assert_auction_timer_in_details_more_than_60_seconds(page)
    page.reload()
    page.wait_for_load_state('load')

    # Проверка автопродления в таблице исполнителя
    page.reload()
    steps.assert_auction_timer_more_than_60_seconds(page, "таблице Исполнителя")
    page.reload()
    page.wait_for_load_state('load')

    # Переход к таблице заказчика
    steps.open_forwarder_orders(page)
    page.wait_for_timeout(1000)
    steps.close_filters(page)
    steps.filter_by(page, "ID заказа", order_id)
    print(f"✅ Заказ успешно найден в таблице Заказчика {order_id}")
    page.wait_for_timeout(1000)

    # Проверка автопродления в таблице заказчика
    steps.assert_auction_timer_more_than_60_seconds(page, "таблице Заказчика")

    # Проверка механик торгов у заказчика
    steps.assert_trade_mechanics_in_table(page, expected_mechanics)

    # Проверка статусов у заказчика
    steps.assert_order_status_in_first_row(page, "Торги")
    print("✅ Статус заказа корректный: Торги")

    steps.assert_auction_status_in_customer_table(page, "Идут")

    # Ожидание завершения торгов и автовыбора победителя
    with allure.step("Ожидаем завершения торгов и автовыбора победителя"):
        print("⏳ Ожидаем завершения торгов (80 секунд) ⏳")
        time.sleep(80)

    # Ожидание смены статусов
    steps.wait_for_auction_status_change(page, "Выбор победителя", max_attempts=12, wait_seconds=10)
    steps.wait_for_auction_status_change(page, "Победитель определен", max_attempts=15, wait_seconds=10)
    steps.wait_for_order_status_change(page, "В работе", max_attempts=10, wait_seconds=5)

    steps.close_filters(page)

    # Проверка заказа в таблице исполнителя на вкладке "В работе"
    steps.open_executor_orders(page)

    with allure.step("Переходим на вкладку 'В работе'"):
        # Новый селектор после изменений фронтенда
        work_tab = page.locator('input.g-segmented-radio-group__option-control[value="orders.onExecute"]')
        work_tab.click()
        page.wait_for_load_state('load')
        print("✅ Перешли на вкладку 'В работе' у Исполнителя")

    page.wait_for_timeout(1000)
    steps.close_filters(page)
    steps.filter_by(page, "ID заказа", order_id)
    print(f"✅ Заказ успешно найден в таблице Исполнителя на вкладке 'В работе' {order_id}")
    page.wait_for_timeout(2000)
    steps.close_filters(page)
    page.wait_for_timeout(2000)


@allure.step("Business: Делаем ставку с комментарием")
def make_bet_with_comment(page: Page, amount: str, comment: str):
    """
    Бизнес-шаг: Открытие формы ставки, ввод суммы и комментария, отправка ставки.

    Args:
        page: Playwright page object
        amount: Сумма ставки
        comment: Комментарий к ставке
    """
    steps.open_bet_form(page)
    steps.enter_bet_amount(page, amount)
    steps.enter_bet_comment(page, comment)
    steps.submit_bet(page, amount)


@allure.step("Business: Заменяем ставку с новым комментарием")
def replace_bet_with_comment(page: Page, amount: str, comment: str) -> str:
    """
    Бизнес-шаг: Замена ставки с новой суммой и комментарием.

    Args:
        page: Playwright page object
        amount: Новая сумма ставки
        comment: Новый комментарий

    Returns:
        str: ID созданной ставки
    """
    steps.open_replace_bet_form(page)
    steps.enter_bet_amount(page, amount)
    steps.enter_bet_comment(page, comment)
    bet_id = steps.replace_bet(page, amount)
    return bet_id


@allure.step("Business: Отклоняем ставку заказчиком с комментарием")
def reject_bet_with_comment(page: Page, comment: str):
    """
    Бизнес-шаг: Отклонение ставки заказчиком с комментарием.

    Args:
        page: Playwright page object
        comment: Комментарий к отклонению
    """
    steps.reject_bet_by_customer(page)
    steps.enter_rejection_comment(page, comment)
    steps.confirm_bet_rejection(page)


@allure.step("Business: Проверяем комментарий заказчика в окне ставок")
def verify_customer_comment_in_bet_window(page: Page, expected_comment: str):
    """
    Бизнес-шаг: Открытие окна ставок, проверка комментария заказчика и закрытие.

    Args:
        page: Playwright page object
        expected_comment: Ожидаемый комментарий
    """
    steps.open_bet_window_from_executor_table(page)
    steps.assert_customer_rejection_comment(page, expected_comment)
    steps.close_bet_details(page)


@allure.step("Business: Создаём заказ из Excel в черновики и отправляем на торги")
def create_draft_order_and_send_to_auction(page: Page, file_path, email: str) -> str:
    """
    Бизнес-шаг: Создание заказа из Excel в черновики, переход к заказчику и отправка на торги.

    1. Авторизация
    2. Создание заказа из Excel
    3. Переход к таблице заказчика
    4. Фильтрация по ID заказа
    5. Открытие заказа на редактирование
    6. Настройка торгов
    7. Отправка на торги

    Args:
        page: Playwright page object
        file_path: Путь к Excel файлу
        email: Email для авторизации

    Returns:
        str: ID созданного заказа
    """
    # Авторизация и создание заказа
    steps.login(page, email)
    steps.open_order_form(page)
    steps.select_upload_order_from_file(page)
    steps.upload_file_on_order_form(page, file_path)
    order_ids = steps.create_orders_from_file(page)

    # Переход к таблице заказчика
    steps.open_forwarder_orders(page)
    page.wait_for_timeout(3000)
    steps.close_filters(page)
    page.wait_for_timeout(3000)
    steps.filter_by(page, "ID заказа", order_ids[0])
    page.wait_for_timeout(3000)

    # Открытие заказа на редактирование
    steps.open_details_order(page, order_ids[0])
    steps.open_order_for_editing(page, order_ids[0])

    # Настройка торгов
    steps.switch_to_auction_tab(page)
    steps.activate_auction_duration(page)
    steps.set_auction_duration_hours(page, "1")

    # Отправка на торги
    order_id = steps.submit_order_to_auction(page)
    steps.close_details_order(page)

    # Перезагрузка и проверка
    page.reload()
    page.wait_for_timeout(2000)
    steps.assert_trade_type(page, order_id, "Выкупить сейчас")
    steps.close_filters(page)

    return order_id


@allure.step("Business: Выкупаем заказ исполнителем через кнопку 'Выкупить сейчас'")
def buy_order_as_executor(page: Page, order_id: str, org_name: str) -> str:
    """
    Бизнес-шаг: Переход к исполнителю, открытие окна ставки и выкуп заказа.

    1. Переход к таблице исполнителя
    2. Фильтрация по ID заказа
    3. Открытие окна ставки
    4. Нажатие кнопки "Выкупить"
    5. Выбор организации
    6. Выкуп заказа

    Args:
        page: Playwright page object
        order_id: ID заказа
        org_name: Название организации для выкупа

    Returns:
        str: Статус матчера после выкупа
    """
    # Переход к исполнителю
    steps.open_executor_orders(page)
    page.wait_for_timeout(3000)
    steps.close_filters(page)
    page.wait_for_timeout(2000)
    steps.filter_by(page, "ID заказа", order_id)
    page.wait_for_timeout(3000)

    # Открытие окна ставки
    steps.open_bet_window_from_executor_table(page)
    # Выкуп заказа
    steps.click_buy_now_button(page)
    steps.select_organization_for_bet(page, org_name)
    status = steps.buy_order_now(page)

    # Перезагрузка
    page.reload()
    page.wait_for_timeout(6000)
    steps.close_filters(page)

    return status



@allure.step("Business: Создаём рейс для заказа и отменяем его до начала")
def create_flight_and_cancel_before_start(page: Page, order_id: str) -> str:
    """
    Бизнес-шаг: Создание рейса для заказа и отмена до начала выполнения.

    1. Открытие меню заказа
    2. Создание рейса
    3. Переход на вкладку "В Рейсе"
    4. Фильтрация по номеру рейса
    5. Открытие деталей рейса
    6. Проверка статуса "Не начат"
    7. Отмена рейса
    8. Проверка статуса "Отменен до начала"

    Args:
        page: Playwright page object
        order_id: ID заказа

    Returns:
        str: ID созданного рейса
    """
    # Создаём рейс
    steps.open_order_menu(page, 0)
    flight_id = steps.create_flight(page)

    # Переходим на вкладку "В Рейсе"
    steps.switch_to_tab(page, "В Рейсе")
    page.wait_for_timeout(2000)
    steps.close_filters(page)

    # Фильтруем по номеру рейса
    steps.filter_by(page, "Номер рейса", flight_id)

    # Проверяем рейс в таблице
    steps.assert_flight_in_table(page, flight_id)

    # Открываем детали рейса
    steps.open_flight_details(page, flight_id)
    page.wait_for_timeout(2000)

    # Проверяем статус "Не начат"
    steps.assert_flight_status(page, "Не начат")

    # Отменяем рейс
    steps.cancel_flight(page)

    # Проверяем статус "Отменен до начала"
    steps.assert_flight_status(page, "Отменен до начала")

    return flight_id


@allure.step("Business: Создаём рейс, начинаем выполнение и отменяем")
def create_flight_start_and_cancel(page: Page, order_id: str) -> str:
    """
    Бизнес-шаг: Создание рейса, начало выполнения и отмена после погрузки.

    1. Переход к таблице исполнителя
    2. Закрытие фильтров
    3. Фильтрация по ID заказа
    4. Открытие меню заказа
    5. Создание рейса
    6. Переход на вкладку "В Рейсе"
    7. Фильтрация по номеру рейса
    8. Открытие деталей рейса
    9. Изменение статуса на "В пути"
    10. Проверка статуса "В пути"
    11. Отмена рейса
    12. Проверка статуса "Отказ"

    Args:
        page: Playwright page object
        order_id: ID заказа

    Returns:
        str: ID созданного рейса
    """
    # Переходим к таблице исполнителя
    steps.open_executor_orders(page)
    page.wait_for_timeout(2000)
    steps.close_filters(page)

    # Фильтруем по ID заказа для точного выбора
    steps.filter_by(page, "ID заказа", order_id)
    page.wait_for_timeout(1000)

    # Создаём рейс
    steps.open_order_menu(page, 0)
    flight_id = steps.create_flight(page)

    # Закрываем фильтры и переходим на вкладку "В Рейсе"
    page.wait_for_timeout(2000)
    steps.close_filters(page)
    steps.switch_to_tab(page, "В Рейсе")
    page.wait_for_timeout(2000)
    steps.close_filters(page)

    # Фильтруем по номеру рейса
    steps.filter_by(page, "Номер рейса", flight_id)

    # Проверяем рейс в таблице
    steps.assert_flight_in_table(page, flight_id)

    # Открываем детали рейса
    steps.open_flight_details(page, flight_id)
    page.wait_for_timeout(2000)

    # Меняем статус на "В пути"
    steps.change_flight_point_status_to_arrived(page)

    # Проверяем статус "В пути"
    steps.assert_flight_status(page, "В пути")

    # Отменяем рейс
    steps.cancel_flight(page)

    # Проверяем статус "Отказ"
    steps.assert_flight_status(page, "Отказ")

    # Закрываем детали
    steps.close_flight_details(page)
    steps.close_filters(page)

    return flight_id


@allure.step("Business: Создаём рейс с двумя заказами, удаляем груз и завершаем рейс")
def create_flight_with_two_orders_delete_shipment_and_complete(
    page: Page,
    order_ids: list
) -> str:
    """
    Бизнес-шаг: Создание рейса с двумя заказами, удаление одного груза и завершение рейса.

    1. Фильтрация по обоим заказам
    2. Выбор двух заказов через чекбоксы
    3. Создание рейса через нижнее меню
    4. Переход на вкладку "В Рейсе"
    5. Фильтрация по номеру рейса
    6. Проверка наличия обоих заказов в рейсе
    7. Открытие деталей рейса
    8. Удаление одного груза
    9. Сохранение изменений
    10. Завершение рейса
    11. Сохранение изменений

    Args:
        page: Playwright page object
        order_ids: Список ID заказов (должно быть 2)

    Returns:
        str: ID созданного рейса
    """
    # Фильтруем оба заказа одновременно используя специальную функцию
    steps.filter_by_multiple_order_ids(page, order_ids)
    
    # Выбираем оба заказа через чекбоксы
    steps.select_order_checkbox(page, 0)
    steps.select_order_checkbox(page, 1)

    # Создаём рейс через нижнее меню
    flight_id = steps.create_flight_from_bottom_menu(page)

    # Переходим на вкладку "В Рейсе"
    steps.switch_to_tab(page, "В Рейсе")
    page.wait_for_timeout(2000)
    steps.close_filters(page)

    # Фильтруем по номеру рейса
    steps.filter_by(page, "Номер рейса", flight_id)

    # Проверяем рейс в таблице
    steps.assert_flight_in_table(page, flight_id)

    # Проверяем что оба заказа в рейсе
    steps.assert_multiple_orders_in_flight(page, flight_id, order_ids)

    # Открываем детали рейса
    steps.open_flight_details(page, flight_id)
    page.wait_for_timeout(2000)

    # Удаляем груз
    steps.delete_flights_cargo(page)

    # Проверяем что появилась кнопка "Восстановить"
    from playwright.sync_api import expect
    expect(page.get_by_text("Восстановить")).to_be_visible(timeout=10000)

    # Сохраняем изменения
    steps.type_saveflight_button(page)

    # Открываем детали рейса снова
    steps.open_flight_details(page, flight_id)
    page.wait_for_timeout(2000)

    # Завершаем рейс
    steps.complete_flight_button(page)

    # Сохраняем изменения
    steps.type_saveflight_button(page)

    page.wait_for_timeout(1000)
    steps.close_filters(page)

    return flight_id


@allure.step("Business: Завершаем рейс и проверяем заказ в статусе 'Завершен'")
def complete_flight_and_verify_order_finished(page: Page, order_id: str, flight_id: str):
    """
    Бизнес-шаг: Завершение рейса и проверка заказа в таблице "Завершенные".

    1. Открытие деталей рейса
    2. Завершение рейса
    3. Сохранение изменений
    4. Переход на вкладку "Завершенные"
    5. Фильтрация по ID заказа
    6. Ожидание появления заказа
    7. Проверка статуса "Завершен"

    Args:
        page: Playwright page object
        order_id: ID заказа
        flight_id: ID рейса
    """
    import utils.common_steps as steps
    import pytest

    # Фильтруем по номеру рейса
    steps.filter_by(page, "Номер рейса", flight_id)
    page.wait_for_timeout(1000)

    # Открываем детали рейса
    steps.open_flight_details(page, flight_id)
    page.wait_for_timeout(2000)

    # Завершаем рейс
    steps.complete_flight_button(page)
    page.wait_for_timeout(2000)

    # Сохраняем изменения
    steps.type_saveflight_button(page)
    page.wait_for_timeout(1000)
    steps.close_filters(page)

    # Переходим на вкладку "Завершенные"
    steps.switch_to_tab(page, "Завершенные")
    page.wait_for_timeout(1000)
    steps.close_filters(page)

    # Фильтруем по номеру рейса
    steps.filter_by(page, "Номер рейса", flight_id)
    page.wait_for_timeout(2000)

    # Ждем появления рейса в таблице с повторными попытками
    for attempt in range(5):
        try:
            steps.assert_flight_in_table(page, flight_id)
            break
        except:
            if attempt < 4:
                page.reload()
                page.wait_for_load_state('load')
                page.wait_for_timeout(2000)
                steps.close_filters(page)
                steps.filter_by(page, "Номер рейса", flight_id)
                page.wait_for_timeout(2000)
            else:
                raise

    # Открываем детали рейса для проверки статуса
    steps.open_flight_details(page, flight_id)
    page.wait_for_timeout(1000)

    # Проверяем статус "Завершен"
    steps.assert_flight_status(page, "Завершен")

    # Закрываем детали рейса
    steps.close_flight_details(page)
    steps.close_filters(page)


@allure.step("Business: Создаём рейс для заказа и проверяем его в таблице 'В Рейсе'")
def create_flight_and_verify_in_table(page: Page, order_id: str) -> str:
    """
    Бизнес-шаг: Создание рейса для заказа и проверка его наличия в таблице.

    1. Ожидание стабилизации UI
    2. Открытие меню заказа (заказ уже отфильтрован)
    3. Создание рейса
    4. Переход на вкладку "В Рейсе"
    5. Фильтрация по номеру рейса
    6. Проверка наличия рейса в таблице

    Args:
        page: Playwright page object
        order_id: ID заказа

    Returns:
        str: ID созданного рейса
    """
    import utils.common_steps as steps

    # Дополнительное ожидание для стабилизации UI после reload
    page.wait_for_timeout(1000)

    # Открываем меню заказа и создаем рейс
    steps.open_order_menu(page, 0)
    flight_id = steps.create_flight(page)

    # Закрываем фильтры
    steps.close_filters(page)
    page.wait_for_timeout(1000)

    # Переходим на вкладку "В Рейсе"
    steps.switch_to_tab(page, "В Рейсе")
    page.wait_for_timeout(1000)
    steps.close_filters(page)

    return flight_id


@allure.step("Business: Создаём нового водителя и проверяем его в системе")
def create_driver_and_verify(page: Page, org_name: str, fio: str, phone: str, inn: str,
                            passport_number: str, passport_issue: str,
                            department_code: str, issue_date: str, license_number: str):
    """
    Бизнес-шаг: Полный цикл создания водителя и проверки его в системе.

    1. Переход в раздел управления водителями
    2. Открытие формы создания водителя
    3. Заполнение всех обязательных полей
    4. Сохранение водителя
    5. Поиск созданного водителя в списке

    Args:
        page: Playwright page object
        org_name: Название организации
        fio: ФИО водителя
        phone: Телефон водителя
        inn: ИНН водителя
        passport_number: Номер паспорта
        passport_issue: Кем выдан паспорт
        department_code: Код подразделения
        issue_date: Дата выдачи паспорта
        license_number: Номер водительского удостоверения
    """
    # Переход в раздел управления водителями
    steps.open_my_organization(page)
    steps.open_drivers_section(page)
    steps.open_create_driver_form(page)

    # Заполнение формы водителя
    steps.select_owner_organization(page, org_name)
    steps.select_organization(page, org_name)
    steps.fill_driver_fio(page, fio)
    steps.fill_driver_phone(page, phone)
    steps.fill_driver_inn(page, inn)
    steps.fill_driver_passport(page, passport_number, passport_issue, department_code, issue_date)
    steps.fill_driver_license(page, license_number)

    # Сохранение водителя
    steps.save_driver(page)

    # Ожидание перехода к списку водителей
    page.wait_for_url("**/drivers", timeout=10000)

    # Поиск и проверка созданного водителя
    steps.clear_driver_search(page)
    steps.search_driver_by_name(page, fio)
    steps.assert_driver_in_list(page, fio)

    page.wait_for_timeout(2000)

@allure.step("Business: Создаём заказ на 'Закрытые торги +' с полным заполнением")
def create_order_on_closed_trades_plus(page: Page) -> str:
    """
    Бизнес-шаг: Создание заказа на 'Закрытые торги +' с полным заполнением всех полей.

    1. Открыть форму создания заказа
    2. Очистить форму
    3. Заполнить блок "Моя организация" с комментарием
    4. Заполнить блок "Владелец груза" с телефоном и комментарием
    5. Заполнить блок "Перевозка" с комментариями
    6. Заполнить груз 1 с одним грузоместом
    7. Заполнить погрузку/разгрузку для груза 1
    8. Установить даты погрузки и разгрузки
    9. Добавить исполнителей
    10. Заполнить блок "Торги" для "Закрытые торги +"
    11. Сохранить заказ

    Returns:
        str: ID созданного заказа
    """
    from utils.steps import order_form_steps as form

    # 1. Открыть форму создания заказа
    steps.open_order_form(page)

    # 2. Очистить форму
    form.clear_order_form(page)

    # 3. Блок "Моя организация"
    form.fill_my_org_with_comment(
        page,
        org_name="Test qa org",
        comment="(!) Моя организация, Комментарий"
    )

    # 4. Блок "Владелец груза"
    form.fill_cargo_owner_with_phone_and_comment(
        page,
        inn="9718101499",
        company_menu_text="ЯНДЕКС.ЛАВКА",
        phone="+74957397000",
        comment="Владелец груза, Комментарий"
    )

    # 5. Блок "Перевозка"
    form.fill_transport_block_with_comments(
        page,
        weight="10",
        volume="45",
        pallets="18",
        cargo_number="(!) Номер заказа в вашей системе",
        category=["Табачная продукция"],
        body_types=["Допельшток", "Кран", "Площадка без бортов"],
        category_comment="Перевозка, Комментарий к категории товара",
        body_comment="Перевозка, Комментарий к типу кузова",
        transshipment_types=["Верхняя", "Боковая", "Полная растентовка"],
        temperature_regimes=["от 2 до 6", "от 5 до 25", "от -18 до -18"],
        cargo_comment="Исполнитель НЕ видит этот комментарий"
    )

    # 6. Груз 1: 1 грузоместо
    form.fill_shipment0_single_package(page)

    # 7. Погрузка/Разгрузка для груза 1
    form.fill_load_unload_for_shipment0_with_addresses(
        page,
        load_phone="+79110985678",
        load_address="Орёл, Московская улица, 67",
        load_address_suggest="Орёл, Московская улица, 67",
        load_contact_name="ФИО Погрузка",
        load_contact_phone="+7(900)111-22-33",
        unload_inn="7704340310",
        unload_company="ЯНДЕКС.ТАКСИ",
        unload_phone="+79226668877",
        unload_address="Калуга, улица Кирова, 31",
        unload_address_suggest="Калуга, улица Кирова, 31",
        unload_contact_name="ФИО Разгрузка",
        unload_contact_phone="+79179001234"
    )

    # 8. Даты погрузки и разгрузки
    form.set_dates_for_shipment0(page, load_days=3, unload_days=4)

    # 9. Добавить исполнителей
    executors = [
        {"inn": "1111111111", "name": "1111111111"},
        {"inn": "test qa", "name": "test qa"},
        {"inn": "фронт", "name": "999999999"}
    ]
    form.add_executors_by_inn_and_name(page, executors)

    # 10. Особые условия для исполнителей
    form.add_special_conditions_for_executors(page, "(!) Особые условия")

    # 11. Блок "Торги" для "Закрытые торги +"
    form.fill_auction_block_closed_trades_plus(
        page,
        minutes="10",
        amount="61200",
        hide_bids=True,
        decrease_only=True
    )

    # 12. Сохранить заказ
    order_id = steps.save_order(page)

    return order_id


@allure.step("Business: Проверяем заказ в таблице заказчика с механикой 'Закрытые торги +'")
def verify_order_in_forwarder_table_with_closed_trades_plus(page: Page, order_id: str):
    """
    Бизнес-шаг: Переход к таблице заказчика и проверка заказа с механикой 'Закрытые торги +'.

    1. Перейти в таблицу заказчика
    2. Закрыть фильтры
    3. Отфильтровать по ID заказа
    4. Проверить статус "Торги"
    5. Проверить механику "Закрытые торги +"

    Args:
        page: Playwright page object
        order_id: ID заказа для проверки
    """
    # 1. Перейти в таблицу заказчика
    steps.open_forwarder_orders(page)
    page.wait_for_timeout(500)

    # 2. Закрыть фильтры
    steps.close_filters(page)
    page.wait_for_timeout(1000)

    # 3. Отфильтровать по ID заказа
    steps.filter_by(page, "ID заказа", order_id)
    page.wait_for_timeout(1000)

    # 4. Проверить статус "Торги"
    steps.assert_order_status_in_first_row(page, "Торги")

    # 5. Проверить механику "Закрытые торги +"
    expected_mechanics = {"Закрытые торги +"}
    steps.assert_trade_mechanics_in_table(page, expected_mechanics)

    steps.close_filters(page)


@allure.step("Business: Создаём заказ на открытые торги")
def create_order_on_open_auction(page: Page) -> str:
    """
    Бизнес-шаг: Создание заказа на открытые торги с полным заполнением.

    1. Открыть форму создания заказа
    2. Очистить форму
    3. Заполнить блок "Моя организация"
    4. Заполнить блок "Владелец груза"
    5. Заполнить блок "Перевозка" с типом транспорта "Автовоз"
    6. Заполнить груз с адресами погрузки и разгрузки
    7. Активировать открытые торги
    8. Установить продолжительность торгов
    9. Сохранить заказ

    Returns:
        str: ID созданного заказа
    """
    from utils.steps import order_form_steps as form

    # 1. Открыть форму создания заказа
    steps.open_order_form(page)

    # 2. Очистить форму
    form.clear_order_form(page)

    # 3. Блок "Моя организация"
    form.fill_my_org(page, org_name="Test qa org")

    # 4. Блок "Владелец груза"
    form.fill_cargo_owner_by_inn(page, inn="1234567890", company_menu_text="тестовая компания")

    # 5. Блок "Перевозка" - выбираем тип транспорта "Автовоз"
    steps.select_transport_type(page, "Автовоз")

    # 6. Заполняем груз с адресами погрузки и разгрузки
    steps.fill_shipment_with_addresses(
        page,
        load_address="Москва, Красная площадь, 1",
        load_address_suggest="Москва, Красная площадь, 1",
        unload_address="Москва, Красная площадь, 1",
        unload_address_suggest="Москва, Красная площадь, 1",
        load_days=7,
        unload_days=9
    )

    # 7. Активируем открытые торги
    steps.enable_open_auction(page)

    # 8. Устанавливаем продолжительность торгов
    steps.set_auction_duration_hours(page, "1")

    # 9. Сохраняем заказ
    order_id = steps.save_order(page)

    return order_id


@allure.step("Business: Проверяем заказ в таблице заказчика с открытыми торгами")
def verify_order_in_forwarder_table_with_open_auction(page: Page, order_id: str):
    """
    Бизнес-шаг: Переход к таблице заказчика и проверка заказа с открытыми торгами.

    1. Перейти в таблицу заказчика
    2. Закрыть фильтры
    3. Отфильтровать по ID заказа
    4. Проверить статус "Торги"
    5. Проверить тип торгов "Открытые торги"

    Args:
        page: Playwright page object
        order_id: ID заказа для проверки
    """
    # 1. Перейти в таблицу заказчика
    steps.open_forwarder_orders(page)
    page.wait_for_timeout(1000)

    # 2. Закрыть фильтры
    steps.close_filters(page)
    page.wait_for_timeout(1000)

    # 3. Отфильтровать по ID заказа
    steps.filter_by(page, "ID заказа", order_id)
    page.wait_for_timeout(1000)

    # 4. Проверить статус "Торги"
    steps.assert_order_status_in_first_row(page, "Торги")

    # 5. Проверить тип торгов "Открытые торги"
    steps.assert_trade_type(page, order_id, "Открытые торги")

    steps.close_filters(page)


@allure.step("Business: Создаём заказ 'На себя как на исполнителя'")
def create_order_to_distribution_self(page: Page) -> str:
    """
    Бизнес-шаг: Создание заказа с отправкой на себя как на исполнителя.

    1. Открыть форму создания заказа
    2. Очистить форму
    3. Заполнить блок "Моя организация"
    4. Заполнить блок "Владелец груза"
    5. Заполнить блок "Перевозка"
    6. Заполнить груз с адресами погрузки и разгрузки
    7. Выбрать вкладку "Себя как на исполнителя"
    8. Сохранить заказ

    Returns:
        str: ID созданного заказа
    """
    from utils.steps import order_form_steps as form

    # 1. Открыть форму создания заказа
    steps.open_order_form(page)

    # 2. Очистить форму
    form.clear_order_form(page)

    # 3. Блок "Моя организация"
    form.fill_my_org(page, org_name="Test qa org")

    # 4. Блок "Владелец груза"
    form.fill_cargo_owner_by_inn(page, inn="6452135389", company_menu_text="ВЕЗЕТ ВАМ")

    # 5. Блок "Перевозка" - выбираем тип транспорта "Борт"
    steps.select_transport_type(page, "Борт")

    # 6. Заполняем груз с адресами погрузки и разгрузки
    # Используем существующую функцию, которая правильно обрабатывает выбор компании для разгрузки
    form.fill_load_unload_for_shipment0(page)

    # Устанавливаем даты погрузки и разгрузки
    form.set_dates_for_shipment0(page, load_days=7, unload_days=9)

    # 7. Выбираем вкладку "Себя как на исполнителя"
    steps.select_distribution_self_tab(page)

    # 8. Сохраняем заказ
    order_id = steps.save_order(page)

    return order_id


@allure.step("Business: Проверяем заказ в таблице заказчика со статусом 'В работе'")
def verify_order_in_forwarder_table_in_work(page: Page, order_id: str):
    """
    Бизнес-шаг: Переход к таблице заказчика и проверка заказа в статусе "В работе".

    1. Перейти в таблицу заказчика
    2. Закрыть фильтры
    3. Отфильтровать по ID заказа
    4. Проверить статус "В работе"

    Args:
        page: Playwright page object
        order_id: ID заказа для проверки
    """
    # 1. Перейти в таблицу заказчика
    steps.open_forwarder_orders(page)
    page.wait_for_timeout(1000)

    # 2. Закрыть фильтры
    steps.close_filters(page)
    page.wait_for_timeout(1000)

    # 3. Отфильтровать по ID заказа
    steps.filter_by(page, "ID заказа", order_id)
    page.wait_for_timeout(1000)

    # 4. Проверить статус "В работе"
    steps.assert_order_status_in_first_row(page, "В работе")

    steps.close_filters(page)


@allure.step("Business: Создаём заказ в черновик с полным заполнением всех полей")
def create_order_to_draft_full(page: Page) -> str:
    """
    Бизнес-шаг: Создание заказа в черновик с полным заполнением всех полей.

    1. Открыть форму создания заказа
    2. Очистить форму
    3. Заполнить блок "Моя организация" с комментарием
    4. Заполнить блок "Владелец груза" с телефоном и комментарием
    5. Заполнить блок "Перевозка" с комментариями
    6. Заполнить груз 1 с двумя грузоместами
    7. Заполнить погрузку/разгрузку для груза 1
    8. Установить даты погрузки и разгрузки
    9. Выбрать группу исполнителей
    10. Добавить особые условия для исполнителей
    11. Заполнить блок "Торги"
    12. Сохранить заказ в черновик

    Returns:
        str: ID созданного заказа
    """
    from utils.steps import order_form_steps as form

    # 1. Открыть форму создания заказа
    steps.open_order_form(page)

    # 2. Очистить форму
    form.clear_order_form(page)

    # 3. Блок "Моя организация"
    form.fill_my_org_with_comment(
        page,
        org_name="Test qa org",
        comment="Моя организация, Комментарий"
    )

    # 4. Блок "Владелец груза"
    form.fill_cargo_owner_with_phone_and_comment(
        page,
        inn="5403324230",
        company_menu_text="КАВЫЧКИ",
        phone="+73832279257",
        comment="(!) Владелец груза, Комментарий"
    )

    # 5. Блок "Перевозка"
    form.fill_transport_block_with_comments(
        page,
        weight="10",
        volume="45",
        pallets="18",
        cargo_number="Номер заказа в вашей системе",
        category=["Другое"],
        body_types=["Допельшток", "Кран", "Площадка без бортов"],
        category_comment="(!) Комментарий к категории товара",
        body_comment="(!) Комментарий к типу кузова",
        transshipment_types=["Верхняя", "Боковая", "Полная растентовка"],
        temperature_regimes=["от 2 до 6", "от 5 до 25", "от -18 до -18"],
        cargo_comment="(!) Исполнитель НЕ видит этот комментарий"
    )

    # 6. Груз 1: 2 грузоместа с полными данными
    form.fill_shipment0_two_packages_full(page)

    # 7. Погрузка/Разгрузка для груза 1
    form.fill_load_unload_for_shipment0_full(page)

    # 8. Даты погрузки и разгрузки
    form.set_dates_for_shipment0(page, load_days=3, unload_days=4)

    # 9. Выбрать группу исполнителей
    form.select_executors_group(page, group_label_qa="order-form-distribution-group-label-7")

    # 10. Особые условия для исполнителей
    form.add_special_conditions_for_executors(page, "Особые условия")

    # 11. Блок "Торги"
    form.fill_auction_block(
        page,
        minutes="10",
        amount="61200",
        step="100",
        buy_now="40000",
        hide_bids=True,
        decrease_only=True
    )

    # 12. Сохранить заказ
    order_id = steps.save_order(page)

    return order_id


@allure.step("Business: Создаём шаблон заказа с двумя грузами")
def create_order_template_with_two_shipments(page: Page, template_name: str):
    """
    Бизнес-шаг: Создание шаблона заказа с двумя грузами и отправкой в черновик.

    1. Открыть форму создания заказа
    2. Очистить форму
    3. Заполнить блок "Моя организация"
    4. Заполнить блок "Владелец груза"
    5. Заполнить блок "Перевозка"
    6. Заполнить груз 1 с двумя грузоместами
    7. Заполнить погрузку/разгрузку для груза 1
    8. Установить даты погрузки и разгрузки для груза 1
    9. Добавить груз 2 с одним грузоместом
    10. Заполнить погрузку/разгрузку для груза 2
    11. Установить даты погрузки и разгрузки для груза 2
    12. Выбрать вкладку "Черновик"
    13. Выбрать группу исполнителей
    14. Сохранить как шаблон

    Args:
        page: Playwright page object
        template_name: Имя шаблона
    """
    from utils.steps import order_form_steps as form

    # 1. Открыть форму создания заказа
    steps.open_order_form(page)

    # 2. Очистить форму
    form.clear_order_form(page)

    # 3. Блок "Моя организация"
    form.fill_my_org(page, org_name="Test qa org")

    # 4. Блок "Владелец груза"
    form.fill_cargo_owner_by_inn(page, inn="9718101499", company_menu_text="ЯНДЕКС.ЛАВКА")

    # 5. Блок "Перевозка"
    form.fill_transport_block(page, weight="10", volume="45", pallets="18", body_type="Допельшток")

    # 6. Груз 1: 2 грузоместа
    steps.fill_shipment_name(page, 0, "Груз 1")
    page.locator('[data-qa="order-form-shipments-items-tab-0"]').click()

    steps.fill_package_name(page, 0, 0, "Грузоместо 1-1")
    page.locator('[data-qa="order-form-shipments-package-add-button-0"]').click()
    steps.fill_package_name(page, 0, 1, "Грузоместо 1-2")

    # 7. Погрузка/Разгрузка для груза 1
    form.fill_load_unload_for_shipment0(page)

    # 8. Даты для груза 1
    form.set_dates_for_shipment0(page, load_days=3, unload_days=4)

    # 9. Груз 2: 1 грузоместо
    page.locator('[data-qa="order-form-shipments-add-shipment-button"]').click()
    page.locator('[data-qa="order-form-shipments-common-tab-1"]').click()
    steps.fill_shipment_name(page, 1, "Груз 2")
    steps.fill_package_name(page, 1, 0, "Грузоместо 2-1")

    # 10. Погрузка/Разгрузка для груза 2
    form.fill_load_unload_for_shipment1(page)

    # 11. Даты для груза 2
    form.set_dates_for_shipment1(page, load_days=5, unload_days=6)

    # 12. Выбрать вкладку "Черновик"
    steps.select_distribution_draft_tab(page)

    # 13. Выбрать группу исполнителей
    form.select_executors_group(page, group_label_qa="order-form-distribution-group-label-7")

    # 14. Сохранить как шаблон
    steps.enter_template_mode(page)
    steps.save_template(page, template_name)

    # Перезагрузка страницы
    page.reload()
    page.wait_for_timeout(2000)


@allure.step("Business: Создаём заказ из шаблона и отправляем в черновик")
def create_order_from_template_to_draft(page: Page, template_name: str) -> str:
    """
    Бизнес-шаг: Создание заказа из шаблона и отправка в черновик.

    1. Открыть форму создания заказа
    2. Очистить форму
    3. Выбрать шаблон
    4. Развернуть блок груза 1
    5. Обновить даты для груза 1
    6. Обновить даты для груза 2
    7. Сохранить заказ в черновик

    Args:
        page: Playwright page object
        template_name: Имя шаблона

    Returns:
        str: ID созданного заказа
    """
    from utils.steps import order_form_steps as form

    # 1. Открыть форму создания заказа
    steps.open_order_form(page)

    # 2. Очистить форму
    form.clear_order_form(page)

    # 3. Выбрать шаблон
    steps.select_template(page, template_name)

    # 4. Развернуть блок груза 1
    steps.expand_shipment_block(page, 0)

    # 5. Обновить даты для груза 1
    form.set_dates_for_shipment0(page, load_days=3, unload_days=4)

    # 6. Обновить даты для груза 2
    form.set_dates_for_shipment1(page, load_days=4, unload_days=5)

    # 7. Сохранить заказ
    order_id = steps.save_order(page)

    return order_id


@allure.step("Business: Проверяем заказ в таблице заказчика")
def verify_order_in_forwarder_table(page: Page, order_id: str):
    """
    Бизнес-шаг: Переход к таблице заказчика и проверка заказа.

    1. Перейти в таблицу заказчика
    2. Закрыть фильтры
    3. Отфильтровать по ID заказа
    4. Проверить наличие заказа в таблице

    Args:
        page: Playwright page object
        order_id: ID заказа для проверки
    """
    # 1. Перейти в таблицу заказчика
    steps.open_forwarder_orders(page)
    page.wait_for_timeout(1000)

    # 2. Закрыть фильтры
    steps.close_filters(page)


@allure.step("Business: Создаём простой заказ в черновик")
def create_order_to_draft_simple(page: Page) -> str:
    """
    Бизнес-шаг: Создание простого заказа в черновик.

    1. Открыть форму создания заказа
    2. Заполнить блок "Моя организация"
    3. Заполнить блок "Владелец груза"
    4. Выбрать тип транспорта "Автовоз"
    5. Заполнить груз с адресами погрузки и разгрузки
    6. Выбрать вкладку "Черновик"
    7. Сохранить заказ

    Returns:
        str: ID созданного заказа
    """
    from utils.steps import order_form_steps as form

    # 1. Открыть форму создания заказа
    steps.open_order_form(page)

    # 2. Блок "Моя организация"
    form.fill_my_org(page, org_name="Test qa org")

    # 3. Блок "Владелец груза"
    form.fill_cargo_owner_by_inn(page, inn="1234567890", company_menu_text="тестовая компания")

    # 4. Выбрать тип транспорта "Автовоз"
    steps.select_transport_type(page, "Автовоз")

    # 5. Заполнить груз с адресами погрузки и разгрузки
    steps.fill_shipment_with_addresses(
        page,
        load_address="Москва, Красная площадь, 1",
        load_address_suggest="Москва, Красная площадь, 1",
        unload_address="Москва, Красная площадь, 1",
        unload_address_suggest="Москва, Красная площадь, 1",
        load_days=7,
        unload_days=9
    )

    # 6. Выбрать вкладку "Черновик"
    steps.select_distribution_draft_tab(page)

    # 7. Сохранить заказ
    order_id = steps.save_order(page)

    return order_id


@allure.step("Business: Проверяем создание потребности из черновика заказа")
def verify_requirement_created_from_draft_order(page: Page, order_id: str) -> str:
    """
    Бизнес-шаг: Полная проверка создания потребности из черновика заказа.

    1. Переход к таблице заказчика на вкладку "Черновики"
    2. Фильтрация по ID заказа и получение requirement_id
    3. Проверка потребности в детализации заказа
    4. Проверка потребности в таблице потребностей
    5. Проверка связи груза с заказом в детализации потребности

    Args:
        page: Playwright page object
        order_id: ID заказа

    Returns:
        str: requirement_id
    """
    # 1. Переход к таблице заказчика
    steps.open_forwarder_orders(page)
    page.wait_for_timeout(2000)

    # 2. Переключение на вкладку "Черновики" и фильтрация
    steps.switch_to_drafts_tab(page)
    steps.close_filters(page)
    page.wait_for_timeout(2000)

    # Перезагрузка для обновления данных
    page.reload()
    page.wait_for_load_state('load')
    page.wait_for_timeout(10000)

    # Фильтрация с перехватом API для получения requirement_id
    import re
    requirement_id = None
    max_attempts = 5

    for attempt in range(max_attempts):
        print(f"\n🔄 Попытка {attempt + 1}/{max_attempts} получить requirement_id...")

        # Если это не первая попытка, перезагружаем страницу
        if attempt > 0:
            page.reload()
            page.wait_for_load_state('load')
            page.wait_for_timeout(2000)
            steps.switch_to_drafts_tab(page)
            steps.close_filters(page)
            page.wait_for_timeout(1000)

        with page.expect_response(re.compile(r".*/api/orders/v0/transferOrder/getFlatForCustomer.*")) as response_info:
            steps.filter_by(page, "ID заказа", order_id)
            page.wait_for_timeout(3000)

        # Извлечение requirement_id из ответа
        response = response_info.value
        requirement_id = steps.extract_requirement_id_from_response(response)

        if requirement_id:
            print(f"✅ requirement_id получен: {requirement_id}")
            break

        print(f"⚠️ requirement_id не найден, ожидание 3 секунды перед повтором...")
        page.wait_for_timeout(3000)
        steps.close_filters(page)

    if not requirement_id:
        raise AssertionError(f"requirement_id не был получен из API после {max_attempts} попыток")

    # Проверка заказа в таблице
    order_link = page.locator(f'a[data-qa="order-link"]:has-text("{order_id}")')
    order_link.wait_for(state="visible", timeout=10000)
    print(f"✅ Заказ {order_id} найден в таблице черновиков")

    # 3. Проверка потребности в детализации заказа
    steps.open_details_order(page, order_id)
    page.wait_for_timeout(2000)
    steps.expand_requirement_cargo_block(page)
    steps.assert_requirement_link_in_order_details(page, requirement_id, order_id)

    steps.close_details_order(page)
    page.wait_for_timeout(1000)

    # 4. Проверка потребности в таблице потребностей
    steps.open_requirements_table(page)
    steps.close_filters(page)
    page.wait_for_timeout(1000)

    # Фильтрация по requirement_id с fallback
    try:
        steps.filter_by(page, "Номер потребности", requirement_id)
        print(f"✅ Фильтр 'Номер потребности' применен")
    except Exception as e:
        print(f"⚠️ Ошибка при применении фильтра: {e}")
        # Альтернативный способ
        filters_button = page.locator("span.g-button__text", has_text="Фильтры")
        filters_button.wait_for(state="visible", timeout=10000)
        filters_button.click()
        page.wait_for_timeout(500)

        dropdown = page.locator('[data-qa="select-popup"]')
        requirement_option = dropdown.locator('span.g-select-list__option-default-label', has_text="Номер потребности").first
        requirement_option.wait_for(state="visible", timeout=5000)
        requirement_option.click()

        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

        requirement_label = page.locator("div.g-label__content", has_text="Номер потребности")
        requirement_label.click()
        page.wait_for_timeout(500)

        input_field = page.locator("textarea.g-text-area__control, input.g-text-input__control").first
        input_field.fill(str(requirement_id))

        page.get_by_text("Применить", exact=True).click()
        print("✅ Фильтр применен альтернативным способом")

    page.wait_for_timeout(2000)

    # Поиск и проверка статуса
    requirement_row = steps.find_requirement_by_id(page, requirement_id)
    steps.assert_requirement_status(page, requirement_row, "Открыта")
    page.wait_for_timeout(3000)

    # 5. Проверка связи груза с заказом
    steps.open_requirement_details(page, requirement_row)

    steps.expand_requirement_cargo_block(page)
    steps.expand_specific_requirement_cargo(page, 0)
    steps.assert_requirement_cargo_match_status(page, "Совпадают", 0)
    steps.assert_requirement_cargo_linked_to_order(page, order_id, 0)

    print("\n" + "=" * 50)
    print("✅ Все проверки потребности пройдены успешно!")
    print("=" * 50)

    return requirement_id

@allure.step("Business: Проверяем изменение статусов груза потребности")
def verify_requirement_cargo_difference(page: Page, requirement_id: str) -> str:
    """
    Бизнес-шаг: Проверка несовпадений между грузами заказа и потребности.

    1. Проверка потребности в таблице потребностей
    2. Фильтрация по requirement_id с fallback
    3. Поиск и проверка статуса потребности
    4. Открытие детализации потребности
    5. Проверка статуса груза потребности

    Args:
        page: Playwright page object
        requirement_id: ID потребности

    Returns:
        str: requirement_id
    """
    # 1. Проверка потребности в таблице потребностей
    steps.open_requirements_table(page)
    steps.close_filters(page)
    page.wait_for_timeout(1000)

    # 2. Фильтрация по requirement_id с fallback
    try:
        steps.filter_by(page, "Номер потребности", requirement_id)
        print(f"✅ Фильтр 'Номер потребности' применен")
    except Exception as e:
        print(f"⚠️ Ошибка при применении фильтра: {e}")
        # Альтернативный способ
        filters_button = page.locator("span.g-button__text", has_text="Фильтры")
        filters_button.wait_for(state="visible", timeout=10000)
        filters_button.click()
        page.wait_for_timeout(500)

        dropdown = page.locator('[data-qa="select-popup"]')
        requirement_option = dropdown.locator('span.g-select-list__option-default-label', has_text="Номер потребности").first
        requirement_option.wait_for(state="visible", timeout=5000)
        requirement_option.click()

        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

        requirement_label = page.locator("div.g-label__content", has_text="Номер потребности")
        requirement_label.click()
        page.wait_for_timeout(500)

        input_field = page.locator("textarea.g-text-area__control, input.g-text-input__control").first
        input_field.fill(str(requirement_id))

        page.get_by_text("Применить", exact=True).click()
        print("✅ Фильтр применен альтернативным способом")

    page.wait_for_timeout(2000)

    # 3. Поиск и проверка статуса
    requirement_row = steps.find_requirement_by_id(page, requirement_id)

    # 4. Открытие детализации потребности
    steps.open_requirement_details(page, requirement_row)

    # 5. Проверка статуса груза потребности
    steps.expand_requirement_cargo_block(page)
    steps.expand_specific_requirement_cargo(page, 0)
    steps.assert_requirement_cargo_match_status(page, "Есть несовпадения", 0)

    print("\n" + "=" * 50)
    print("✅ Все проверки потребности пройдены успешно!")
    print("=" * 50)

    return requirement_id
    page.wait_for_timeout(1000)

    # 3. Отфильтровать по ID заказа
    steps.filter_by(page, "ID заказа", order_id)
    page.wait_for_timeout(1000)

    # 4. Проверить наличие заказа
    steps.assert_order_in_table(page, order_id, "Черновик")

    steps.close_filters(page)


@allure.step("Business: Создаём шаблон заказа с двумя грузами и сохраняем")
def create_order_template_with_two_shipments_and_save(page: Page, template_name: str):
    """
    Бизнес-шаг: Создание шаблона заказа с двумя грузами.

    1. Авторизация
    2. Создание шаблона с двумя грузами
    3. Сохранение шаблона
    4. Перезагрузка страницы

    Args:
        page: Playwright page object
        template_name: Имя шаблона для сохранения
    """
    steps.login(page)
    steps.create_template_with_two_shipments(page, template_name)


@allure.step("Business: Создаём заказ из шаблона и отправляем на торги")
def create_order_from_template_and_send_to_auction(
    page: Page,
    template_name: str,
    load_days_shipment0: int,
    unload_days_shipment0: int,
    load_days_shipment1: int,
    unload_days_shipment1: int
) -> str:
    """
    Бизнес-шаг: Создание заказа из шаблона с установкой дат и отправкой на торги.

    1. Открыть форму создания заказа
    2. Очистить форму
    3. Выбрать шаблон
    4. Развернуть блок груза 1
    5. Установить даты для груза 1
    6. Установить даты для груза 2
    7. Настроить торги
    8. Сохранить заказ

    Args:
        page: Playwright page object
        template_name: Имя шаблона
        load_days_shipment0: Дни до погрузки груза 1
        unload_days_shipment0: Дни до разгрузки груза 1
        load_days_shipment1: Дни до погрузки груза 2
        unload_days_shipment1: Дни до разгрузки груза 2

    Returns:
        str: ID созданного заказа
    """
    from utils.steps import order_form_steps as form

    # Открыть форму и выбрать шаблон
    steps.open_order_form(page)
    form.clear_order_form(page)
    steps.select_template_by_date(page, template_name)

    # Развернуть блок груза 1
    steps.expand_shipment_block(page, 0)

    # Установить даты для груза 1
    form.set_dates_for_shipment0(page, load_days=load_days_shipment0, unload_days=unload_days_shipment0)

    # Установить даты для груза 2
    form.set_dates_for_shipment1(page, load_days=load_days_shipment1, unload_days=unload_days_shipment1)

    # Настроить торги
    page.locator('[data-qa="order-form-auction-duration-tab"]').click()
    from helpers.ui import fill_custom_input
    fill_custom_input(page.locator('[data-qa="order-form-auction-duration-minutes-input"]'), "10")
    fill_custom_input(page.locator('[data-qa="order-form-auction-amount-input"]'), "61200")
    fill_custom_input(page.locator('[data-qa="order-form-auction-step-input"]'), "100")
    fill_custom_input(page.locator('[data-qa="order-form-auction-buy-now-price-input"]'), "40000")

    # Активировать тоглы
    toggle = page.locator('[data-qa="order-form-auction-hide-bids-from-carrier-switch"]')
    inp = toggle.locator('input[role="switch"]')
    if inp.get_attribute('aria-checked') == 'false':
        toggle.click()

    toggle = page.locator('[data-qa="order-form-auction-decrease-only-from-declared-price-switch"]')
    inp = toggle.locator('input[role="switch"]')
    if inp.get_attribute('aria-checked') == 'false':
        toggle.click()

    # Сохранить заказ
    order_id = steps.save_order(page)

    return order_id

@allure.step("Business: Проверяем изменение статусов потребности")
def verify_requirement_status_changes(page: Page, requirement_id: str) -> None:
    """
    Бизнес-шаг: Проверка полного цикла изменения статусов потребности.
    1. Переход в таблицу потребностей
    2. Фильтрация по номеру потребности
    3. Проверка начального статуса "Открыта"
    4. Открытие детализации потребности
    5. Перевод в статус "Завершена" и проверка
    6. Перевод в статус "Отменена" и проверка
    7. Перевод в статус "Открыта" и проверка
    Args:
        page: Playwright page object
        requirement_id: ID потребности
    """
    # 1. Переход в таблицу потребностей
    steps.open_requirements_table(page)
    steps.close_filters(page)
    page.wait_for_timeout(1000)

    # 2. Фильтрация по номеру потребности
    steps.filter_by(page, "Номер потребности", requirement_id)

    # 3. Проверка начального статуса "Открыта"
    requirement_row = steps.find_requirement_by_id(page, requirement_id)
    steps.assert_requirement_status(page, requirement_row, "Открыта")

    # 4. Открытие детализации потребности
    steps.open_requirement_details(page, requirement_row)

    # 5. Перевод в статус "Завершена" и проверка
    steps.perform_action_on_requirement(page, "cancel")
    steps.assert_requirement_status_in_details(page, "Отменена")

    # 6. Перевод в статус "Отменена" и проверка
    steps.perform_action_on_requirement(page, "reopen")
    steps.assert_requirement_status_in_details(page, "Открыта")

    # 7. Перевод в статус "Открыта" и проверка
    steps.perform_action_on_requirement(page, "complete")
    steps.assert_requirement_status_in_details(page, "Завершена")
    print("\n" + "=" * 50)
    print("✅ Все переходы статусов потребности выполнены успешно!")
    print("=" * 50)

@allure.step("Business: Дублируем груз в заказе в черновике")
def duplicate_shipment_in_draft_order(page: Page, order_id: str) -> None:
    """
    Бизнес-шаг: Дублируем груз в заказе в черновике.

    1. Переход в таблицу заказов в черновике
    2. Фильтрация по ID заказа
    3. Открытие детализации заказа
    4. Переход в режим редактирования заказа
    5. Дублирование груза в заказе
    6. Сохранение измененного заказа

    Args:
        page: Playwright page object
        order_id: ID заказа
    """
    # 1. Переход в таблицу заказов в черновике
    steps.open_forwarder_orders(page)
    page.wait_for_timeout(2000)

    # 2. Фильтрация по ID заказа
    steps.switch_to_drafts_tab(page)
    steps.close_filters(page)
    page.wait_for_timeout(1000)

    # 3. Открытие детализации заказа
    steps.filter_by(page, "ID заказа", order_id)
    page.wait_for_timeout(2000)

    steps.open_details_order(page, order_id)
    page.wait_for_timeout(2000)

    # 4. Переход в режим редактирования заказа
    page.locator("button:has-text('Редактировать')").click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)

    # 5. Дублирование груза в заказе
    page.locator(f'[data-qa="order-form-shipments-duplicate-button-0"]').first.click()
    page.wait_for_timeout(1000)

    # 6. Сохранение измененного заказа
    steps.save_order_after_edit(page)
    page.wait_for_timeout(3000)

    print("\n" + "=" * 50)
    print("✅ Все переходы статусов потребности выполнены успешно!")
    print("=" * 50)


@allure.step("Business: Отменить торги с комментарием")
def cancel_auction_with_comment(page: Page, comment_text: str = "отмена из торгов"):
    """
    Бизнес-шаг: Отмена торгов с причиной 'другое' и комментарием.
    
    1. Открыть меню заказа
    2. Выбрать 'Отменить торги'
    3. Нажать 'не актуально'
    4. Выбрать причину 'другое'
    5. Ввести комментарий
    6. Подтвердить отмену
    
    Args:
        page: Playwright page object
        comment_text: Текст комментария для отмены
    """
    from utils.steps import cancel_order_steps as cancel
    
    steps.open_order_menu(page, 0)
    cancel.click_cancel_auction_menu_item(page)
    cancel.click_not_actual_reason_button(page)
    cancel.select_other_reason(page)
    cancel.enter_cancellation_comment(page, comment_text)
    cancel.confirm_cancel_auction(page)


@allure.step("Business: Проверить отмену торгов в черновике")
def verify_auction_cancellation_in_draft(page: Page, order_id: str, comment_text: str = "отмена из торгов"):
    """
    Бизнес-шаг: Проверка отмены торгов в черновике.
    
    1. Проверить статус 'Черновик' с повторными попытками
    2. Открыть детализацию заказа
    3. Раскрыть блок комментариев
    4. Проверить комментарий (без проверки причины)
    5. Закрыть детализацию
    
    Args:
        page: Playwright page object
        order_id: ID заказа
        comment_text: Ожидаемый текст комментария
    """
    from utils.steps import order_details_asserts as asserts
    from playwright.sync_api import expect
    
    # Проверяем статус 'Черновик'
    asserts.assert_order_status_draft_with_retry(page, order_id)
    
    # Проверяем комментарий в детализации
    steps.open_details_order(page, order_id)
    page.wait_for_timeout(1000)
    steps.open_comment_order(page)
    
    # Проверяем только комментарий, игнорируя причину
    comment_element = page.get_by_text(comment_text)
    expect(comment_element).to_be_visible(timeout=10000)
    print(f"✅ Комментарий найден: '{comment_text}'")
    
    steps.close_details_order(page)


@allure.step("Business: Создание заказа через lite форму")
def create_order_via_lite_form(
    page: Page,
    departure_address: str = "Москва ул свободы 89",
    destination_address: str = "Тюмень",
    weight: str = "10",
    comment: str = "Самая лучшая цена",
    price: str = "10000"
) -> str:
    """
    Бизнес-шаг: Создание заказа через упрощенную lite форму.
    
    1. Открыть lite форму создания заказа
    2. Заполнить адрес отправления с выбором саджеста
    3. Заполнить адрес назначения с выбором саджеста
    4. Заполнить вес груза
    5. Переключить тоггл
    6. Заполнить комментарий к грузу
    7. Заполнить стоимость
    8. Создать заказ
    9. Проверить статус "Поиск"
    
    Args:
        page: Playwright page object
        departure_address: Адрес отправления (по умолчанию "Москва ул свободы 89")
        destination_address: Адрес назначения (по умолчанию "Тюмень")
        weight: Вес груза в тоннах (по умолчанию "10")
        comment: Комментарий к грузу (по умолчанию "Самая лучшая цена")
        price: Стоимость (по умолчанию "10000")
    
    Returns:
        str: ID созданного заказа
    """
    # Открываем lite форму
    steps.open_lite_order_form(page)
    
    # Заполняем адреса
    steps.fill_lite_departure_address(page, departure_address)
    steps.fill_lite_destination_address(page, destination_address)
    
    # Заполняем параметры груза
    steps.fill_lite_cargo_weight(page, weight)
    steps.toggle_lite_switch(page)
    steps.fill_lite_cargo_comment(page, comment)
    
    # Заполняем стоимость
    steps.fill_lite_price(page, price)
    
    # Создаем заказ
    order_id = steps.submit_lite_order(page)
    
    # Проверяем статус
    steps.assert_lite_order_search_status(page)
    
    print("\n" + "=" * 50)
    print(f"✅ Заказ {order_id} успешно создан через lite форму")
    print("✅ Статус: Поиск")
    print("=" * 50 + "\n")
    
    return order_id


@allure.step("Business: Создать ставку на заказ через lite форму и выбрать предложение")
def create_bet_and_select_offer_for_lite_order(
    page: Page,
    order_id: str,
    executor_id: str = "3",
    price: str = "1000"
) -> str:
    """
    Бизнес-шаг: Полный цикл создания ставки и выбора предложения для lite заказа.
    
    1. Получение demandId через API
    2. Создание ставки через API
    3. Обновление страницы
    4. Проверка статуса "Есть предложения"
    5. Открытие детализации заказа
    6. Проверка блока "Предложения"
    7. Выбор предложения
    8. Проверка блока "Перевозчик"
    
    Args:
        page: Playwright page object
        order_id: ID заказа
        executor_id: ID исполнителя (по умолчанию "3")
        price: Цена ставки (по умолчанию "1000")
        
    Returns:
        str: ID созданной ставки
    """
    # Получаем demandId через API
    demand_id = steps.get_demand_id_for_order(page, order_id)
    
    # Создаем ставку через API
    bet_id = steps.create_bet_via_api(page, demand_id, executor_id, price)
    
    # Обновляем страницу
    page.reload()
    page.wait_for_load_state('load')
    page.wait_for_timeout(3000)
    print("✅ Страница обновлена")
    
    # Проверяем статус "Есть предложения"
    steps.assert_lite_order_has_offers_status(page)
    
    # Открываем детализацию заказа
    steps.open_lite_order_details(page)
    
    # Проверяем блок "Предложения"
    steps.assert_lite_offers_block(page)
    
    # Выбираем предложение
    steps.select_lite_offer(page)
    
    # Проверяем блок "Перевозчик"
    steps.assert_lite_carrier_block(page)
    
    print(f"\n{'='*50}")
    print(f"✅ Ставка создана и выбрана")
    print(f"✅ Bet ID: {bet_id}")
    print(f"✅ Demand ID: {demand_id}")
    print(f"✅ Перевозчик назначен")
    print(f"{'='*50}\n")
    
    return bet_id
