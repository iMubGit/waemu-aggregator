import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class IdempotencyKey:
    """
    UUID-based idempotency key enforced at DB level via unique constraint.
    Application never checks existence first — it attempts INSERT
    and catches UniqueViolation. This eliminates the TOCTOU race
    condition that would exist with an application-level check.
    """
    value: str

    def __post_init__(self) -> None:
        try:
            uuid.UUID(self.value)
        except ValueError as e:
            raise ValueError(
                f"IdempotencyKey must be a valid UUID: {self.value}"
            ) from e

    @classmethod
    def generate(cls) -> "IdempotencyKey":
        return cls(value=str(uuid.uuid4()))

    def __str__(self) -> str:
        return self.value