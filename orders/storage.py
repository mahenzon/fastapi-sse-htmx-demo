from operator import attrgetter
from typing import TYPE_CHECKING
from uuid import uuid4

from orders.entity import Order
from orders.entity import OrderID
from orders.entity import OrderStatus

if TYPE_CHECKING:
    from orders.dtos import OrderCreate


class OrdersStorage:
    def __init__(self) -> None:
        self._orders = dict[OrderID, Order]()

    @classmethod
    def _new_id(cls) -> OrderID:
        # return secrets.token_urlsafe(6)  # noqa: ERA001
        return uuid4().hex[:6]

    def create(self, order: OrderCreate) -> Order:
        order = Order(
            id=self._new_id(),
            status=OrderStatus.PENDING,
            **order.model_dump(),
        )
        self._orders[order.id] = order
        return order

    def get(self, order_id: OrderID) -> Order | None:
        return self._orders.get(order_id)

    def get_all(self) -> list[Order]:
        return sorted(
            self._orders.values(),
            key=attrgetter("created_at"),
            reverse=True,
        )
