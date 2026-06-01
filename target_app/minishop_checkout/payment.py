from __future__ import annotations

import re
from datetime import datetime

from .models import PaymentCardInput, ValidationResult


CARDHOLDER_PATTERN = re.compile(r"^[A-Za-z][A-Za-z '\\-]{0,38}[A-Za-z]$|^[A-Za-z]{2}$")


def validate_payment_card(
    payment_card: PaymentCardInput,
    *,
    current_year: int | None = None,
    current_month: int | None = None,
) -> ValidationResult:
    now = datetime.utcnow()
    effective_year = current_year if current_year is not None else now.year
    effective_month = current_month if current_month is not None else now.month
    errors: list[str] = []

    cardholder_name = payment_card.cardholder_name.strip()
    if len(cardholder_name) < 2 or len(cardholder_name) > 40 or not CARDHOLDER_PATTERN.fullmatch(cardholder_name):
        errors.append("cardholder_name must be 2 to 40 valid name characters")

    if "*" in payment_card.card_number:
        errors.append("masked card numbers are not accepted as primary input")

    card_digits = payment_card.card_number.replace(" ", "")
    if not card_digits.isdigit() or not 13 <= len(card_digits) <= 19:
        errors.append("card_number must contain 13 to 19 digits after spaces are removed")

    if not 1 <= payment_card.expiry_month <= 12:
        errors.append("expiry_month must be between 1 and 12")

    if not effective_year <= payment_card.expiry_year <= effective_year + 15:
        errors.append("expiry_year must be within the supported future window")

    if (
        1 <= payment_card.expiry_month <= 12
        and effective_year <= payment_card.expiry_year <= effective_year + 15
        and (
            payment_card.expiry_year < effective_year
            or (
                payment_card.expiry_year == effective_year
                and payment_card.expiry_month < effective_month
            )
        )
    ):
        errors.append("expiry date must not be earlier than the current month")

    brand = payment_card.card_brand.lower()
    expected_cvv_length = 4 if brand == "amex" else 3
    if brand not in {"visa", "mastercard", "amex"}:
        errors.append("card_brand must be visa, mastercard, or amex")
    elif not payment_card.cvv.isdigit() or len(payment_card.cvv) != expected_cvv_length:
        errors.append(f"{payment_card.card_brand} requires a {expected_cvv_length}-digit cvv")

    return ValidationResult(is_valid=not errors, errors=tuple(errors))
