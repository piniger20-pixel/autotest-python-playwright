# utils/common_steps.py
# ФАСАД: оставляем внешний интерфейс стабильным для тестов

from utils.steps.auth_steps import login

from utils.steps.cancel_order_steps import (
    cancel_order_by_customer,
    cancel_order_by_executor,
    click_cancel_auction_menu_item,
    click_not_actual_reason_button,
    select_other_reason,
    enter_cancellation_comment,
    confirm_cancel_auction
)

from utils.steps.navigation_steps import (
    open_order_form,
    open_executor_orders,
    open_forwarder_orders,
    open_details_order,
    close_details_order,
    open_comment_order,
    show_archived_orders,
    hide_archived_orders
)

from utils.steps.filters_steps import (
    reset_filters,
    close_filters,
    filter_by,
    set_date_range_filter,
    filter_by_multiple_order_ids,
)

from utils.steps.order_form_steps import (
    select_template,
    pick_date,
    save_order,
    save_order_after_edit,
    select_task_list,
    select_transport_type,
    fill_shipment_with_addresses,
    enable_open_auction,
    set_auction_duration_hours,
    select_distribution_self_tab,
    select_distribution_draft_tab,
    enter_template_mode,
    save_template,
    expand_shipment_block,
    fill_shipment_name,
    fill_package_name,
)

from utils.steps.orders_table_asserts import (
    assert_order_in_table,
    assert_trade_type,
    assert_table_empty,
    assert_any_row_matches,
    assert_any_row_date_matches,
    assert_order_status_in_first_row,
    assert_multiple_orders_in_table,
    assert_order_statuses_present,
    wait_for_order_in_table,
    assert_order_status_by_index,
)

from utils.steps.orders_api_steps import (
    get_executor_order_after_filter,
    get_forwarder_order_after_filter,
    wait_orders_table_reload,
)

from utils.steps.flights_steps import (
    create_flight,
    create_flight_from_bottom_menu,
    delete_flights_cargo,
    type_saveflight_button,
    complete_flight_button,
    open_flight_saidbar_trgouht_bottom_menu,
    add_order_to_ready_flight,
    cancel_flight,
    change_flight_point_status_to_arrived
)

from utils.steps.flights_asserts import (
    assert_flight_in_table,
    assert_order_in_flight,
    assert_multiple_orders_in_flight,
    assert_shipments_in_route,
    open_flight_details,
    close_flight_details,
    assert_flight_status,
)

from utils.steps.order_details_asserts import (
    assert_text_in_order_details,
    assert_cancellation_reason_and_comment,
    open_order_by_status_with_retry,
    assert_order_status_draft_with_retry,
)

from utils.steps.table_steps import (
    select_order_checkbox,
    switch_to_tab,
    open_order_menu,
    disable_table_optimization,
)

from utils.steps.excel_create_orders_steps import (
    create_orders_from_file,
    select_upload_order_from_file,
    upload_file_on_order_form,
)

from utils.steps.order_1x1_steps import accept_offer_1x1_from_table_order

from utils.steps.organization_steps import switch_state_of_organization

from utils.steps.simple_tasks_steps import cancel_simple_task

from utils.steps.drivers_steps import (
    open_my_organization,
    open_drivers_section,
    open_create_driver_form,
    select_owner_organization,
    select_organization,
    fill_driver_fio,
    fill_driver_phone,
    fill_driver_inn,
    fill_driver_passport,
    fill_driver_license,
    save_driver,
    clear_driver_search,
    search_driver_by_name,
    assert_driver_in_list
)

from utils.steps.templates_steps import (
    navigate_to_templates_page,
    apply_template_filters,
    delete_all_filtered_templates,
    create_basic_template,
    verify_template_variables,
    verify_template_in_order_form,
    verify_template_in_order_details,
    delete_template_by_id,
    create_template_with_two_shipments,
    select_template_by_date,
)

from utils.steps.matcher_steps import (
    assert_trade_mechanics_in_table,
    open_bet_window_from_executor_table,
    assert_vat_display_in_bet_window,
    open_bet_form,
    select_organization_for_bet,
    enter_bet_amount,
    assert_bet_validation_errors,
    assert_bet_button_disabled,
    submit_bet,
    assert_best_bet_with_vat,
    assert_best_bet_without_vat,
    assert_bet_not_decrease_error,
    open_auction_window_from_customer_table,
    select_auction_winner,
    confirm_auction_winner,
    cancel_bet_by_executor,
    enter_bet_comment,
    open_replace_bet_form,
    replace_bet,
    reject_bet_by_customer,
    enter_rejection_comment,
    confirm_bet_rejection,
    assert_customer_rejection_comment,
    close_bet_details,
    close_order_details_window,
)

from utils.steps.auction_timer_steps import (
    assert_auction_timer_less_than_60_seconds,
    assert_auction_timer_more_than_60_seconds,
    assert_auction_timer_in_details_more_than_60_seconds,
)

from utils.steps.auction_status_steps import (
    wait_for_auction_status_change,
    wait_for_order_status_change,
    assert_auction_status_in_customer_table,
)

from utils.steps.draft_order_steps import (
    open_order_for_editing,
    switch_to_auction_tab,
    activate_auction_duration,
    set_auction_duration_hours,
    submit_order_to_auction,
    click_buy_now_button,
    buy_order_now,
)

from utils.steps.requirements_steps import (
    enable_requirements_flag,
    open_requirements_table,
    switch_to_drafts_tab,
    expand_requirement_cargo_block,
    expand_specific_requirement_cargo,
    expand_cargo_details,
    assert_requirement_status,
    open_requirement_details,
    assert_requirement_cargo_match_status,
    assert_requirement_cargo_linked_to_order,
    find_requirement_by_id,
    extract_requirement_id_from_response,
    assert_requirement_link_in_order_details,
    perform_action_on_requirement,
    assert_requirement_status_in_details,
)

from utils.steps.lite_order_steps import (
    open_lite_order_form,
    fill_lite_departure_address,
    fill_lite_destination_address,
    fill_lite_cargo_weight,
    toggle_lite_switch,
    fill_lite_cargo_comment,
    fill_lite_price,
    submit_lite_order,
    assert_lite_order_search_status,
)

from utils.steps.lite_bets_steps import (
    get_demand_id_for_order,
    create_bet_via_api,
    assert_lite_order_has_offers_status,
    open_lite_order_details,
    assert_lite_offers_block,
    select_lite_offer,
    assert_lite_carrier_block,
)

# если нужно оставить тут же
from helpers.ui import wait_and_click  # опционально


