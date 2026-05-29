import allure
from playwright.sync_api import Page
from typing import Callable, List, Optional
from pathlib import Path
from helpers.ui import wait_and_click, wait_enabled, qa_key
import logging
import time

log = logging.getLogger(__name__)

UPLOAD_TAB = 'order-form-upload-order-from-file-tab'
SELECT_FILE_BTN = 'order-form-upload-file-select-file-button'
CREATE_ORDERS_BTN = 'order-form-upload-file-create-orders-button'


@allure.step("Загружаем excel file в создании заказ'{file_path}'")
def upload_excel_file_in_create_order(
    page: Page,
    button_selector: str,
    file_path: str,
    request_url_part: str = 'api/converter/orders-xlsx-to-json',
    timeout: int = 15000,
    on_done: Optional[Callable[[], None]] = None,
) -> None:
    with page.expect_request(lambda r: request_url_part in r.url, timeout=timeout):
        with page.expect_file_chooser() as fc_info:
            wait_and_click(page, button_selector)
            fc_info.value.set_files(file_path)

    if on_done:
        on_done()


def wait_all_create_from_xlsx(
    page: Page,
    click_fn: Callable[[], None],
    url_part: str = "createFromXlsx",
    timeout: int = 30000,
) -> List[str]:
    order_ids: List[str] = []

    started = 0
    finished = 0
    in_flight = 0

    def is_target(url: str) -> bool:
        return url_part in url

    def on_request(request):
        nonlocal started, in_flight
        if is_target(request.url):
            started += 1
            in_flight += 1

    def on_request_finished(request):
        nonlocal finished, in_flight
        if is_target(request.url):
            finished += 1
            in_flight -= 1

    def on_request_failed(request):
        nonlocal finished, in_flight
        if is_target(request.url):
            finished += 1
            in_flight -= 1

    def on_response(response):
        if is_target(response.url):
            try:
                body = response.json()
                order_id = body.get("data", {}).get("id")
                if order_id:
                    order_ids.append(order_id)
            except Exception:
                pass

    page.on("request", on_request)
    page.on("requestfinished", on_request_finished)
    page.on("requestfailed", on_request_failed)
    page.on("response", on_response)

    try:
        click_fn()

        deadline = time.time() + timeout / 1000

        while started == 0:
            if time.time() > deadline:
                raise TimeoutError("Не стартовал ни один createFromXlsx")
            page.wait_for_timeout(50)

        while in_flight > 0:
            if time.time() > deadline:
                raise TimeoutError(
                    f"createFromXlsx не завершились: started={started}, finished={finished}"
                )
            page.wait_for_timeout(50)

    finally:
        page.remove_listener("request", on_request)
        page.remove_listener("requestfinished", on_request_finished)
        page.remove_listener("requestfailed", on_request_failed)
        page.remove_listener("response", on_response)

    if started != finished:
        raise AssertionError(
            f"Не все createFromXlsx завершились: started={started}, finished={finished}"
        )

    page.wait_for_timeout(50)

    return order_ids


def create_order_from_excel(
    page: Page,
    file_name: str,
    pytestconfig
) -> List[str]:
    project_root = Path(pytestconfig.rootpath)
    file_path = project_root / "tests" / "testdata" / file_name

    with allure.step("Выбираем загрузку заказа из файла"):
        wait_and_click(page, qa_key(UPLOAD_TAB), 10000)

    with allure.step("Загружаем файл"):
        upload_excel_file_in_create_order(
            page, qa_key(SELECT_FILE_BTN), file_path)

    with allure.step("Создание заказа(ов)"):
        wait_enabled(page, qa_key(CREATE_ORDERS_BTN), timeout=15000)

        order_ids = wait_all_create_from_xlsx(
            page=page,
            click_fn=lambda: wait_and_click(
                page, qa_key(CREATE_ORDERS_BTN), 10000),
            url_part="createFromXlsx",
            timeout=30000,
        )

        log.info("Нажата кнопка создания заказов из файла")

        print(f"✅ Создано: {len(order_ids)} заказ(ов)")
        assert order_ids, "❌ Не создано ни одного заказа"

        page.reload()

        return order_ids
