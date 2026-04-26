# config.py
import os
from dotenv import load_dotenv, find_dotenv

# Сохраняем переменные окружения из командной строки ДО загрузки .env
CLI_STAGE = os.environ.get("STAGE")

# Загружаем переменные из .env файла
load_dotenv(find_dotenv())

APP_URL = os.getenv("APP_URL")

HEADLESS = os.getenv("HEADLESS", "False").lower() in ('true', '1', 'yes', 'on')
EXPECT_TIMEOUT = float(os.getenv("EXPECT_TIMEOUT"))

# Стейдж для тестирования: приоритет у командной строки, затем .env, затем дефолт
STAGE = CLI_STAGE or os.getenv("STAGE", "latest")

# Отладочная информация о стейдже
print(f"🔍 DEBUG: CLI_STAGE = {CLI_STAGE}")
print(f"🔍 DEBUG: STAGE from .env = {os.getenv('STAGE')}")
print(f"🔍 DEBUG: Final STAGE = {STAGE}")


# Пул email для параллельных воркеров
EMPLOYEE_EMAILS = [
    "email_test_oleinik.jenka@yandex.ru",
    "email_test_maxnaty23@yandex.ru",
    "email_test_katehok17@yandex.ru",
    "email_test_yndx-pinigin-s@yandex.ru",
    "email_test_ramazanov24679@yandex.ru",
    "email_test_yakovmike@yandex.ru",
    "email_test_yndx-zankevich@yandex.ru"
]

# Организация подбирается в зависимости от email сотрудника
ORG_BY_EMAIL = {
    "email_test_oleinik.jenka@yandex.ru": "Autotests_Гибрид_НДС_20%",
    "email_test_maxnaty23@yandex.ru": "Test qa org",
    "email_test_katehok17@yandex.ru": "Test qa org",
    "email_test_yndx-pinigin-s@yandex.ru": "Autotests_Гибрид_НДС_20%",
    "email_test_ramazanov24679@yandex.ru": "Test qa org",
    "email_test_yakovmike@yandex.ru": "Test qa org",
    "email_test_yndx-zankevich@yandex.ru": "Test qa org"
}


def get_employee_email_for_worker(worker_id):
    """
    Возвращает email для конкретного воркера.
    worker_id может быть: 'master', 'gw0', 'gw1', 'gw2', 'gw3', ...
    """
    if worker_id == "master":
        # Последовательный запуск - используем первый email или из .env
        return os.getenv("EMPLOYEE_EMAIL", EMPLOYEE_EMAILS[0])
    
    # Извлекаем номер воркера из 'gw0', 'gw1', и т.д.
    worker_num = int(worker_id.replace('gw', ''))
    # Циклически распределяем email по воркерам
    email_index = worker_num % len(EMPLOYEE_EMAILS)
    return EMPLOYEE_EMAILS[email_index]


def get_organization_for_email(email):
    """Возвращает организацию для email"""
    org = ORG_BY_EMAIL.get(email)
    if not org:
        raise ValueError(f"для e-mail {email} нет организации в ORG_BY_EMAIL")
    return org


# Для обратной совместимости (когда не используется параллелизация)
EMPLOYEE_EMAIL = os.getenv("EMPLOYEE_EMAIL", EMPLOYEE_EMAILS[0])
ORGANIZATION_NAME = ORG_BY_EMAIL.get(EMPLOYEE_EMAIL)

if not EMPLOYEE_EMAIL:
    raise ValueError("EMPLOYEE_EMAIL is not set. Укажи его в .env или используй параллельный запуск")
if not ORGANIZATION_NAME:
    raise ValueError(f"для e-mail {EMPLOYEE_EMAIL} нет организации в ORG_BY_EMAIL")
