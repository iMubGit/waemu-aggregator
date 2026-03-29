from decimal import Decimal, InvalidOperation
from dataclasses import dataclass
from src.domain.value_objects.enums import Currency


@dataclass(frozen=True)
class Money:
    """
    Immutable monetary value. Always Decimal — never float.
    Float arithmetic produces rounding errors unacceptable in
    BCEAO-regulated settlement reporting.
    """
    amount: Decimal
    currency: Currency

    def __post_init__(self) -> None:
        if not isinstance(self.amount, Decimal):
            raise TypeError(
                f"Money.amount must be Decimal, got {type(self.amount).__name__}. "
                "Never use float for monetary values."
            )
        if self.amount < Decimal("0"):
            raise ValueError("Money.amount cannot be negative")

    @classmethod
    def of(cls, amount: str | Decimal, currency: Currency) -> "Money":
        try:
            return cls(amount=Decimal(str(amount)), currency=currency)
        except InvalidOperation as e:
            raise ValueError(f"Invalid monetary amount: {amount}") from e

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError(
                f"Cannot add {self.currency} and {other.currency}"
            )
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def __str__(self) -> str:
        return f"{self.amount} {self.currency.value}"