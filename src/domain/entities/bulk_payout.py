from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4
from src.domain.value_objects.enums import BulkPayoutState, Currency
from src.domain.value_objects.phone_number import PhoneNumber
from src.domain.state_machine import transition_bulk_payout


@dataclass
class BulkPayoutRow:
    """Single beneficiary row within a bulk payout batch."""
    row_id: str
    bulk_payout_id: str
    beneficiary_phone: PhoneNumber
    amount: Decimal
    currency: Currency
    reference: str
    transaction_id: str | None = None  # set after transaction is created
    outcome: str | None = None         # SETTLED, FAILED, PENDING


@dataclass
class BulkPayout:
    bulk_payout_id: str
    merchant_id: str
    state: BulkPayoutState = BulkPayoutState.REQUESTED
    rows: list[BulkPayoutRow] = field(default_factory=list)
    total_rows: int = 0
    successful_rows: int = 0
    failed_rows: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def create(cls, merchant_id: str) -> "BulkPayout":
        return cls(
            bulk_payout_id=str(uuid4()),
            merchant_id=merchant_id,
        )

    def transition_to(self, target: BulkPayoutState) -> None:
        self.state = transition_bulk_payout(self.state, target)
        self.updated_at = datetime.now(timezone.utc)

    def resolve_final_state(self) -> BulkPayoutState:
        """
        Determines terminal state after all rows are processed.
        Partial success is a first-class outcome — not a failure.
        """
        if self.failed_rows == 0:
            return BulkPayoutState.COMPLETED
        elif self.successful_rows == 0:
            return BulkPayoutState.FAILED
        else:
            return BulkPayoutState.PARTIAL_SUCCESS