from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4
from src.domain.value_objects.enums import MerchantStatus, Provider
from src.domain.state_machine import transition_merchant
from src.domain.exceptions import MerchantNotVerifiedError


@dataclass
class Merchant:
    merchant_id: str
    name: str
    country_code: str
    allowed_providers: list[Provider]
    settlement_account: str
    status: MerchantStatus = MerchantStatus.PENDING_KYC
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def create(
        cls,
        name: str,
        country_code: str,
        allowed_providers: list[Provider],
        settlement_account: str,
    ) -> "Merchant":
        return cls(
            merchant_id=str(uuid4()),
            name=name,
            country_code=country_code,
            allowed_providers=allowed_providers,
            settlement_account=settlement_account,
        )

    def transition_to(self, target: MerchantStatus) -> None:
        """
        All status changes go through the state machine.
        No direct assignment to self.status anywhere in the codebase.
        """
        self.status = transition_merchant(self.status, target)
        self.updated_at = datetime.now(timezone.utc)

    def assert_verified(self) -> None:
        """
        Called by initiate_payment use case before any payment is processed.
        Domain-layer enforcement — not middleware, not a decorator.
        """
        if self.status != MerchantStatus.VERIFIED:
            raise MerchantNotVerifiedError(self.merchant_id)