from enum import Enum


class MerchantStatus(str, Enum):
    PENDING_KYC = "PENDING_KYC"
    VERIFIED = "VERIFIED"
    SUSPENDED = "SUSPENDED"
    KYC_REJECTED = "KYC_REJECTED"  # terminal — no transitions out


class TransactionState(str, Enum):
    INITIATED = "INITIATED"
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SETTLED = "SETTLED"      # terminal
    FAILED = "FAILED"        # terminal


class BulkPayoutState(str, Enum):
    REQUESTED = "REQUESTED"
    VALIDATING = "VALIDATING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"        # terminal
    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"  # terminal
    FAILED = "FAILED"              # terminal


class ProviderStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"


class WebhookDeliveryStatus(str, Enum):
    PENDING = "PENDING"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"
    EXHAUSTED = "EXHAUSTED"  # dead letter threshold reached


class Provider(str, Enum):
    ORANGE_MONEY = "orange_money"
    WAVE = "wave"
    MTN_MOMO = "mtn_momo"


class Currency(str, Enum):
    XOF = "XOF"  # WAEMU zone
    XAF = "XAF"  # CEMAC zone
    GHS = "GHS"  # Ghana


class EventType(str, Enum):
    # Transaction events
    TRANSACTION_INITIATED = "transaction.initiated"
    TRANSACTION_PENDING = "transaction.pending"
    TRANSACTION_PROCESSING = "transaction.processing"
    TRANSACTION_SETTLED = "transaction.settled"
    TRANSACTION_FAILED = "transaction.failed"
    TRANSACTION_MANUAL_OVERRIDE = "transaction.manual_override"
    # Merchant events
    MERCHANT_CREATED = "merchant.created"
    MERCHANT_KYC_VERIFIED = "merchant.kyc.verified"
    MERCHANT_KYC_REJECTED = "merchant.kyc.rejected"
    MERCHANT_SUSPENDED = "merchant.suspended"
    # Bulk payout events
    BULK_PAYOUT_REQUESTED = "bulk_payout.requested"
    BULK_PAYOUT_VALIDATING = "bulk_payout.validating"
    BULK_PAYOUT_PROCESSING = "bulk_payout.processing"
    BULK_PAYOUT_COMPLETED = "bulk_payout.completed"
    BULK_PAYOUT_PARTIAL_SUCCESS = "bulk_payout.partial_success"
    BULK_PAYOUT_FAILED = "bulk_payout.failed"