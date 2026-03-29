from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4
from src.domain.value_objects.enums import WebhookDeliveryStatus


@dataclass
class WebhookEndpoint:
    endpoint_id: str
    merchant_id: str
    url: str
    signing_secret: str  # HMAC-SHA256 signing secret per merchant
    active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class WebhookDelivery:
    delivery_id: str
    endpoint_id: str
    transaction_id: str
    attempt_number: int
    status: WebhookDeliveryStatus = WebhookDeliveryStatus.PENDING
    delivered_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def create(
        cls,
        endpoint_id: str,
        transaction_id: str,
        attempt_number: int = 1,
    ) -> "WebhookDelivery":
        return cls(
            delivery_id=str(uuid4()),
            endpoint_id=endpoint_id,
            transaction_id=transaction_id,
            attempt_number=attempt_number,
        )