import re
from dataclasses import dataclass


E164_PATTERN = re.compile(r"^\+[1-9]\d{6,14}$")

# WAEMU/CEMAC country prefixes for validation context
WAEMU_PREFIXES = {
    "+225",  # Côte d'Ivoire
    "+221",  # Sénégal
    "+223",  # Mali
    "+226",  # Burkina Faso
    "+229",  # Bénin
    "+245",  # Guinée-Bissau
    "+227",  # Niger
    "+228",  # Togo
    "+237",  # Cameroun
    "+235",  # Tchad
    "+236",  # République Centrafricaine
    "+242",  # Congo
    "+241",  # Gabon
    "+240",  # Guinée Équatoriale
    "+233",  # Ghana
}


@dataclass(frozen=True)
class PhoneNumber:
    """
    E.164 validated phone number.
    WAEMU mobile money operators require strict E.164 format
    for MSISDN routing — malformed numbers cause silent
    provider failures with no callback.
    """
    value: str

    def __post_init__(self) -> None:
        if not E164_PATTERN.match(self.value):
            raise ValueError(
                f"Invalid E.164 phone number: {self.value}. "
                "Must start with + and contain 7-15 digits."
            )

    def __str__(self) -> str:
        return self.value