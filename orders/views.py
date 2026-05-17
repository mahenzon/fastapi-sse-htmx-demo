from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import HTTPException
from starlette import status

from orders.dependencies import create_order_uc
from orders.dependencies import get_all_orders_uc
from orders.dependencies import get_order_uc
from orders.dtos import OrderCreate
from orders.dtos import OrderRead
from orders.entity import Order
from orders.entity import OrderID
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
)
def read_order(
    order_id: OrderID,
    get: Annotated[
        GetOrderUC,
        Depends(get_order_uc),
    ],
) -> Order:
    order = get(order_id)
    if order is not None:
        return order
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order {order_id!r} not found!",
    )


@router.get(
    "/",
    response_model=list[OrderRead],
)
def get_orders(
    get_all: Annotated[
        GetAllOrdersUC,
        Depends(get_all_orders_uc),
    ],
) -> list[Order]:
    return get_all()
