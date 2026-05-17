from orders.dtos import OrderCreate
from orders.entity import Order
from orders.entity import OrderID
from orders.storage import storage


class CreateOrderUC:
    async def __call__(
        self,
        order_create: OrderCreate,
    ) -> Order:
        order = storage.create(order_create)
        storage.start_progression_task(order.id)
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
