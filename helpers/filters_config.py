FILTERS = [
    {
        "label": "ID заказа",
        "type": "text_input",
        "value": lambda order: order["id"],
        "cell_selector": 'a[data-qa="order-link"]',
    },
    {
        "label": "Тип торгов",
        "type": "select_dropdown",
        "value": lambda order: "1x1",
        "cell_selector": '.g-label_size_xs .g-label__content p',
    },
    {
        "label": "Статус",
        "type": "select_dropdown",
        "value": lambda order: "Торги",
        "cell_selector": '[data-qa^="orders-table-order-status"]',
    },
    {
        "label": "Номер торгов",
        "type": "text_input",
        "value": lambda order: order["demandId"],
        "cell_selector": '[data-qa^="orders-table-order-name-0-MAIN_LEVEL"]',
    },
    {
        "label": "ИНН",
        "type": "text_input",
        "value": lambda order: order["forwarder"]["forwarderTin"],
        "cell_selector": "td.gt-table__cell_id_createDateColumn",
    },
    {
        "label": "Заказчики",
        "type": "select_dropdown",
        "value": lambda order: order["forwarder"]["forwarderName"],
        "cell_selector": "td.gt-table__cell_id_customerInfoColumn",
    },
#     {
#         # заказ должен быть в работе чтобы проверить исполнителя
#         "label": "Исполнители",
#         "type": "select_dropdown",
#         "value": lambda order: order["matcher"]["possibleExecutorsIDs"][0]["name"],
#         "cell_selector": "td.gt-table__cell_id_executorColumn",
#     },
#     {
#         баг в работе MAGACG-5519
#         "label": "Комментарий к кузову",
#         "type": "text_input",
#         "value": lambda order: order["bodyTypeComment"],
#         "cell_selector": "td.gt-table__cell_id_executorColumn",
#    },
    {
        "label": "Статус торгов",
        "type": "select_dropdown",
        "value": lambda order: "Торги",
        "cell_selector": "td.gt-table__cell_id_auctionStatusColumn",
        "expected_in_cell": "Идут", 
    },
        {
        "label": "Грузовладелец",
        "type": "select_dropdown",
        "value": lambda order: order["customer"]["customerName"],
        # "cell_selector": "td._firstLevelCell_19ym0_127. _firstLevelCell_19ym0_127     ",
        "cell_selector": "td.gt-table__cell_id_cargoOwnerColumn",
    },
        {
        "label": "Отправитель",
        "type": "select_dropdown",
        "value": lambda order: order["shipments"][0]["npShipment"]["name"],
        "cell_selector": "td.gt-table__cell_id_shipmentCustomerColumn",
    },
        {
        "label": "Получатель",
        "type": "select_dropdown",
        "value": lambda order: order["shipments"][0]["npUnshipment"]["name"],
        "cell_selector": "td.gt-table__cell_id_unshipmentCustomerColumn",
    },
# ПОЧИНИ этот КУСОК ОН НЕ РАБОТАЕТ, А ДОЛЖЕН !!! 
#      {
#        "label": "Дата создания",
#        "type": "date_range",
#        "value": {
#                  "from": "12.12.2025 10:00",
#                  "to": "13.12.2025 18:00"},
#        "expected_in_cell": "12.12",
#        "cell_selector": "td.gt-table__cell_id_createDateColumn",
#   },
# ПОЧИНИ этот КУСОК ОН НЕ РАБОТАЕТ, А ДОЛЖЕН !!!
    #   {
    #     "label": "Дата последнего изменения",
    #     "type": "date_range",
    #     "value": {
    #               "from": "17.12.2025 16:00",
    #               "to": "18.12.2025 23:30"},
    #     "expected_in_cell": "17.12",
    #     "cell_selector": "td.gt-table__cell_id_lastUpdateDateColumn",
    # },

# ПОЧИНИ этот КУСОК ОН НЕ РАБОТАЕТ, А ДОЛЖЕН !!!
    #     "label": "Дата начала первой погрузки",
    #     "type": "date_range",
    #     "value": {
    #               "from": "17.12.2025",
    #               "to": "17.12.2025"},
    #     "expected_in_cell": "17.12",
    #     "cell_selector": "td.gt-table__cell_id_lastUpdateDateColumn",
    # },
    {
        "label": "Логист заказчика",
        "type": "select_dropdown",
        "value": lambda order: order["fwdResponsibleLogistician"]["name"],
        "cell_selector": "td.gt-table__cell_id_customerLogisticianColumn",
    },
    #     {
    #     # Заказ должен быть в работе 
    #     "label": "Логист исполнителя",
    #     "type": "select_dropdown",
    #     "value": lambda order: order["execResponsibleLogistician"]["name"],
    #     "cell_selector": "td.gt-table__cell_id_executorsLogisticianColumn",
    # },
    #     {
    #     # По заказу должен быть рейс
    #     "label": "Ответственный логист за рейс",
    #     "type": "select_dropdown",
    #     "value": lambda order: order["responsibleLogistician"]["name"],
    #     "cell_selector": "td.gt-table__cell_id_responsibleLogisticianColumn",
    # },
    {
        "label": "Особые условия",
        "type": "text_input",
        "value": lambda order: order["distribution"]["comment"],
        "cell_selector": "td.gt-table__cell_id_transferOrderAdditionalConditionsColumn",
    },
]