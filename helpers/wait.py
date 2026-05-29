from playwright.sync_api import expect

def wait_visible(page, locator, timeout=5000):
    el = page.locator(locator)
    expect(el).to_be_visible(timeout=timeout)
    return el