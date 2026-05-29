import allure
import utils.common_steps as steps
from playwright.sync_api import Page

@allure.step("Установка фильтра поиска заказа по ID")
def order_by_id(page: Page, order_id: str):
    steps.close_filters(page)
    
    # Set up response listener BEFORE applying the filter
    with page.expect_response(
        lambda r: ("transferOrder/getFlatForCustomer" in r.url and r.status == 200),
        timeout=30000
    ) as response_info:
        # Now apply the filter, which will trigger the API call
        steps.filter_by(page, "ID заказа", order_id, mode="text_input")
    
    # Get the captured response
    response = response_info.value
    
    # Get order data from the captured API response
    order = steps.get_forwarder_order_after_filter(page, order_id, response=response)
    
    return order