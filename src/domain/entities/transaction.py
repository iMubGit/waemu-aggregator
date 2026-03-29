from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4
from src.domain.value_objects.enums import TransactionState, Provider
from src.domain.value_objects.money import Money
from src.domain.value_objects.phone_number import PhoneNumber
from src.domain.value_objects.idempotency_key import IdempotencyKey
from src.domain.state_machine import transition_transaction


@dataclass
class Transaction:
    transaction_id: str
    merchant_id: str
    provider: Provider
    amount: Money
    beneficiary_phone: PhoneNumber
    idempotency_key: IdempotencyKey
    country_code: str
    state: TransactionState = TransactionState.INITIATED
    external_ref: str | None = None
    bulk_payout_id: str | None = None  # set if part of a bulk payout batch
    initiated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    settled_at: datetime | None = None

    @classmethod
    def create(
        cls,
        merchant_id: str,
        provider: Provider,
        amount: Money,
        beneficiary_phone: PhoneNumber,
        idempotency_key: IdempotencyKey,
        country_code: str,
        bulk_payout_id: str | None = None,
    ) -> "Transaction":
        return cls(
            transaction_id=str(uuid4()),
            merchant_id=merchant_id,
            provider=provider,
            amount=amount,
            beneficiary_phone=beneficiary_phone,
            idempotency_key=idempotency_key,
            country_code=country_code,
            bulk_payout_id=bulk_payout_id,
        )

    def transition_to(self, target: TransactionState) -> None:
        self.state = transition_transaction(self.state, target)
        self.updated_at = datetime.now(timezone.utc)
        if target == TransactionState.SETTLED:
            self.settled_at = datetime.now(timezone.utc)