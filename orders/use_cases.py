from orders.dtos import OrderCreate
from orders.entity import Order
from orders.entity import OrderID
from orders.storage import storage


class CreateOrderUC:
    def __call__(
        self,
        order_create: OrderCreate,
    ) -> Order:
        return storage.create(order_create)


class GetOrderUC:
    def __call__(
        self,
        order_id: OrderID,
    ) -> Order | None:
        return storage.get(order_id)


class GetAllOrdersUC:
    def __call__(self) -> list[Order]:
        return storage.get_all()
