import asyncio
from collections.abc import AsyncGenerator

from fastapi import Request
from fastapi.sse import ServerSentEvent

from orders.dtos import OrderCreate
from orders.entity import Order
from orders.entity import OrderID
from orders.entity import OrderStatus
from orders.storage import storage
from orders.types import OnOrderAdance


class CreateOrderUC:
    async def __call__(
        self,
        order_create: OrderCreate,
        on_order_adance: OnOrderAdance,
    ) -> Order:
        order = storage.create(order_create)
        storage.start_progression_task(order.id, on_order_adance)
        return order


class GetOrderUC:
    async def __call__(
        self,
        order_id: OrderID,
    ) -> Order | None:
        return storage.get(order_id)


class GetAllOrdersUC:
    async def __call__(self) -> list[Order]:
        return storage.get_all()


class OrderEventsSubscriptionUC:
    def __init__(self, request: Request) -> None:
        self.request = request

    async def wait_for_event[T](self, queue: asyncio.Queue[T]) -> T | None:
        while True:
            if await self.request.is_disconnected():
                return None
            try:
                return await asyncio.wait_for(queue.get(), timeout=0.5)
            except TimeoutError:
                pass

    async def __call__(
        self,
        order_id: OrderID,
    ) -> AsyncGenerator[ServerSentEvent]:
        order = storage.get(order_id)
        if order is None:
            msg = f"Order with id {order_id} does not exist"
            raise ValueError(msg)  # TODO: domain error

        if order.status == OrderStatus.DELIVERED:
            yield ServerSentEvent(event="close")
            return

        queue = await storage.subscribe(order_id)
        # TODO: Handle request disconnect
        try:
            while True:
                if await self.request.is_disconnected():
                    yield ServerSentEvent(event="close")
                    return

                event = await self.wait_for_event(queue)
                if event is None:
                    yield ServerSentEvent(event="close")
                    return

                yield event

        finally:
            storage.unsubscribe(order_id, queue)
