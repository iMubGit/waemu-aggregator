from dataclasses import dataclass


class DomainException(Exception):
    """Base for all domain exceptions. Carries bilingual messages."""

    def __init__(self, message_en: str, message_fr: str) -> None:
        self.message_en = message_en
        self.message_fr = message_fr
        super().__init__(message_en)


class InvalidStateTransitionError(DomainException):
    def __init__(self, entity: str, from_state: str, to_state: str) -> None:
        super().__init__(
            message_en=f"Invalid transition for {entity}: {from_state} → {to_state}",
            message_fr=f"Transition invalide pour {entity}: {from_state} → {to_state}",
        )


class MerchantNotVerifiedError(DomainException):
    def __init__(self, merchant_id: str) -> None:
        super().__init__(
            message_en=f"Merchant {merchant_id} is not verified and cannot initiate payments",
            message_fr=f"Le marchand {merchant_id} n'est pas vérifié et ne peut pas initier de paiements",
        )


class UnsupportedMarketError(DomainException):
    def __init__(self, country_code: str) -> None:
        super().__init__(
            message_en=f"Country {country_code} is not supported in the routing table",
            message_fr=f"Le pays {country_code} n'est pas supporté dans la table de routage",
        )


class ProviderResponseParseError(DomainException):
    def __init__(self, provider: str, reason: str) -> None:
        super().__init__(
            message_en=f"Failed to parse response from {provider}: {reason}",
            message_fr=f"Échec de l'analyse de la réponse de {provider}: {reason}",
        )


class ProviderDegradedError(DomainException):
    def __init__(self, provider: str, country_code: str) -> None:
        super().__init__(
            message_en=f"Provider {provider} is degraded for market {country_code} and no fallback is available",
            message_fr=f"Le fournisseur {provider} est dégradé pour le marché {country_code} et aucun repli n'est disponible",
        )


class IdempotencyConflictError(DomainException):
    def __init__(self, key: str) -> None:
        super().__init__(
            message_en=f"Idempotency key {key} already exists",
            message_fr=f"La clé d'idempotence {key} existe déjà",
        )


class ManualOverrideError(DomainException):
    def __init__(self, transaction_id: str, reason: str) -> None:
        super().__init__(
            message_en=f"Manual override failed for transaction {transaction_id}: {reason}",
            message_fr=f"La substitution manuelle a échoué pour la transaction {transaction_id}: {reason}",
        )