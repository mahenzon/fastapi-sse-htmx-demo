from fastapi import Request

from orders.use_cases import CreateOrderUC
from orders.use_cases import GetAllOrdersUC
from orders.use_cases import GetOrderUC
from orders.use_cases import OrderEventsSubscriptionUC


def create_order_uc() -> CreateOrderUC:
    return CreateOrderUC()


def get_order_uc() -> GetOrderUC:
    return GetOrderUC()


def get_all_orders_uc() -> GetAllOrdersUC:
    return GetAllOrdersUC()


def order_events_subscription_uc(
    request: Request,
) -> OrderEventsSubscriptionUC:
    return OrderEventsSubscriptionUC(request=request)
