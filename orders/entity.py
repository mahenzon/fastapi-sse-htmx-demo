from dataclasses import dataclass
from dataclasses import field
from datetime import UTC
from datetime import datetime
from enum import StrEnum


class OrderStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"


@dataclass
class Order:
    id: str
    name: str
    status: str
    created_at: str = field(
        default_factory=lambda: datetime.now(UTC),
    )
