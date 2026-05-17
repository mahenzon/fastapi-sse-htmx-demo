import asyncio
import random
from operator import attrgetter
from uuid import uuid4

from orders.dtos import OrderCreate
from orders.entity import STATUSES
from orders.entity import Order
from orders.entity import OrderID
from orders.entity import OrderStatus


class OrdersStorage:
    def __init__(self) -> None:
        self._orders = dict[OrderID, Order]()
        self._progression_tasks = dict[OrderID, asyncio.Task[None]]()

    @classmethod
    def _new_id(cls) -> OrderID:
        # return secrets.token_urlsafe(6)  # noqa: ERA001
        return uuid4().hex[:6]

    def create(self, order_create: OrderCreate) -> Order:
        order = Order(
            id=self._new_id(),
            status=OrderStatus.PENDING,
            **order_create.model_dump(),
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

    def start_progression_task(self, order_id: OrderID) -> None:
        existing_task = self._progression_tasks.get(order_id)
        if existing_task is not None and existing_task.done():
            return

        self._progression_tasks[order_id] = asyncio.create_task(self._advance(order_id))

    async def _advance(self, order_id: OrderID) -> None:
        order = self._orders.get(order_id)
        if order is None:
            return

        start_index = STATUSES.index(order.status) + 1
        new_statues = STATUSES[start_index:]
        for status in new_statues:
            await self._advance_order_status(order_id, status)

    async def _advance_order_status(
        self,
        order_id: OrderID,
        status: OrderStatus,
    ) -> None:
        sleep_time = random.randint(3, 10)
        await asyncio.sleep(sleep_time)
        order = self._orders.get(order_id)
        if order is None:
            return
        order.status = status


storage = OrdersStorage()
