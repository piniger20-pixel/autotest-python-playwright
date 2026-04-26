import pytest
import allure
from playwright.sync_api import Playwright, Page, expect
from urllib.parse import urlparse
from config import APP_URL, HEADLESS, EXPECT_TIMEOUT, STAGE, get_employee_email_for_worker, get_organization_for_email, EMPLOYEE_EMAIL
from pages.auth.login_page import LoginPage
import os
# Настройка масштаба браузера (75% по умолчанию)
ZOOM_LEVEL = os.getenv("BROWSER_ZOOM", "1.0")

@pytest.fixture
def chromium_page(playwright: Playwright, request) -> Page:  # type: ignore
    """
    Фикстура для Playwright-страницы с поддержкой параллелизации.
    Поддерживает как последовательный, так и параллельный запуск.
    """
    expect.set_options(timeout=EXPECT_TIMEOUT)
    
    # Получаем worker_id и email
    worker_id = getattr(request.config, 'workerinput', {}).get('workerid', 'master')
    
    if worker_id == 'master':
        email = EMPLOYEE_EMAIL
    else:
        email = get_employee_email_for_worker(worker_id)
    
    organization = get_organization_for_email(email)
    
    # Логируем информацию
    print(f"\n{'='*80}")
    print(f"🌐 Создание браузера для теста")
    print(f"👤 Worker ID: {worker_id}")
    print(f"📧 Email: {email}")
    print(f"🏢 Организация: {organization}")
    print(f"🎯 Stage: {STAGE}")
    print(f"🔍 Zoom: {int(float(ZOOM_LEVEL) * 100)}%")
    print(f"{'='*80}\n")
    
    # Добавляем в Allure
    allure.dynamic.parameter("Worker ID (chromium)", worker_id)
    allure.dynamic.parameter("Email (chromium)", email)
    allure.dynamic.parameter("Stage", STAGE)
    allure.dynamic.parameter("Browser Zoom", f"{int(float(ZOOM_LEVEL) * 100)}%")

    browser = playwright.chromium.launch(
        headless=HEADLESS,
        args = [
        "--window-size=1920,1080",
        f"--force-device-scale-factor={ZOOM_LEVEL}"
    ]
    )
    playwright.selectors.set_test_id_attribute("data-qa")

    context = browser.new_context(
        base_url=f"{APP_URL}/",
        ignore_https_errors=True,
        no_viewport=True
    )
    
    # Устанавливаем stage cookie перед созданием страницы
    domain = urlparse(APP_URL).netloc
    context.add_cookies([
        {
            'name': "stage",
            'value': STAGE,
            'path': '/',
            'domain': domain,
        }
    ])
    print(f"✅ Worker {worker_id}: Установлен cookie stage = {STAGE} (domain: {domain})")

    page = context.new_page()
    yield page
    browser.close()


@pytest.fixture
def login_page(chromium_page: Page) -> LoginPage:
    return LoginPage(page=chromium_page)
