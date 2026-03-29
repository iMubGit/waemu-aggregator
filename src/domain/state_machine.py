from src.domain.value_objects.enums import (
    MerchantStatus,
    TransactionState,
    BulkPayoutState,
)
from src.domain.exceptions import InvalidStateTransitionError


# Valid transitions only — anything not listed here is invalid
MERCHANT_TRANSITIONS: dict[MerchantStatus, set[MerchantStatus]] = {
    MerchantStatus.PENDING_KYC: {
        MerchantStatus.VERIFIED,
        MerchantStatus.KYC_REJECTED,
    },
    MerchantStatus.VERIFIED: {
        MerchantStatus.SUSPENDED,
    },
    MerchantStatus.SUSPENDED: {
        MerchantStatus.VERIFIED,
    },
    MerchantStatus.KYC_REJECTED: set(),  # terminal — no transitions out
}

TRANSACTION_TRANSITIONS: dict[TransactionState, set[TransactionState]] = {
    TransactionState.INITIATED: {TransactionState.PENDING, TransactionState.FAILED},
    TransactionState.PENDING: {TransactionState.PROCESSING, TransactionState.FAILED},
    TransactionState.PROCESSING: {TransactionState.SETTLED, TransactionState.FAILED},
    TransactionState.SETTLED: set(),   # terminal
    TransactionState.FAILED: set(),    # terminal
}

BULK_PAYOUT_TRANSITIONS: dict[BulkPayoutState, set[BulkPayoutState]] = {
    BulkPayoutState.REQUESTED: {BulkPayoutState.VALIDATING, BulkPayoutState.FAILED},
    BulkPayoutState.VALIDATING: {BulkPayoutState.PROCESSING, BulkPayoutState.FAILED},
    BulkPayoutState.PROCESSING: {
        BulkPayoutState.COMPLETED,
        BulkPayoutState.PARTIAL_SUCCESS,
        BulkPayoutState.FAILED,
    },
    BulkPayoutState.COMPLETED: set(),       # terminal
    BulkPayoutState.PARTIAL_SUCCESS: set(), # terminal
    BulkPayoutState.FAILED: set(),          # terminal
}


def transition_merchant(current: MerchantStatus, target: MerchantStatus) -> MerchantStatus:
    if target not in MERCHANT_TRANSITIONS.get(current, set()):
        raise InvalidStateTransitionError("Merchant", current.value, target.value)
    return target


def transition_transaction(current: TransactionState, target: TransactionState) -> TransactionState:
    if target not in TRANSACTION_TRANSITIONS.get(current, set()):
        raise InvalidStateTransitionError("Transaction", current.value, target.value)
    return target


def transition_bulk_payout(current: BulkPayoutState, target: BulkPayoutState) -> BulkPayoutState:
    if target not in BULK_PAYOUT_TRANSITIONS.get(current, set()):
        raise InvalidStateTransitionError("BulkPayout", current.value, target.value)
    return target