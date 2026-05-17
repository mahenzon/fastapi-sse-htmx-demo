from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse
from starlette import status

from misc.templating import templates
from orders.dependencies import create_order_uc
from orders.dependencies import get_all_orders_uc
from orders.dependencies import get_order_uc
from orders.dtos import OrderCreate
from orders.dtos import OrderRead
from orders.entity import Order
from orders.entity import OrderID
from orders.entity import OrderStatus
from orders.use_cases import CreateOrderUC
from orders.use_cases import GetAllOrdersUC
from orders.use_cases import GetOrderUC

router = APIRouter(
    tags=["Orders"],
    prefix="/orders",
)


@router.post(
    "/",
    response_model=OrderRead,
)
def create_order(
    order_create: Annotated[
        OrderCreate,
        Form(),
    ],
    create: Annotated[
        CreateOrderUC,
        Depends(create_order_uc),
    ],
) -> Order:
    return create(order_create)


@router.get(
    "/{order_id}",
    response_model=OrderRead,
    name="order_detail",
)
def read_order(
    request: Request,
    order_id: OrderID,
    get: Annotated[
        GetOrderUC,
        Depends(get_order_uc),
    ],
) -> Order:
    order = get(order_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {order_id!r} not found!",
        )
    if "text/html" not in request.headers.get("Accept", ""):
        return order

    context = {
        "order": order,
        "order_statuses": [str(value) for value in OrderStatus],
    }

    return templates.TemplateResponse(
        request=request,
        name="orders/details.html",
        context=context,
    )


@router.get(
    "/",
    response_model=list[OrderRead],
    name="orders_list",
    # Define both media types under the 200 Status Code to build the Swagger dropdown
    responses={
        status.HTTP_200_OK: {
            "description": (
                "Returns a list of orders. Formats available: JSON array or HTML page."
            ),
            "content": {
                "application/json": {},
                "text/html": {
                    "schema": {
                        "type": "string",
                        "example": (
                            "<!DOCTYPE html><html><body>"
                            "<h1>Orders List</h1>...</body></html>"
                        ),
                    },
                },
            },
        },
    },
)
def get_orders(
    request: Request,
    get_all: Annotated[
        GetAllOrdersUC,
        Depends(get_all_orders_uc),
    ],
) -> HTMLResponse | list[Order]:
    orders = get_all()

    if "text/html" not in request.headers.get("Accept", ""):
        return orders

    return templates.TemplateResponse(
        request=request,
        name="orders/list.html",
        context={
            "orders": orders,
        },
    )
