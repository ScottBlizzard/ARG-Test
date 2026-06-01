from __future__ import annotations

import re

from .models import PickupContact, ValidationResult


PICKUP_STATION_PATTERN = re.compile(r"^PS-\d{6}$")
PHONE_PATTERN = re.compile(r"^\+\d{8,15}$")
PICKUP_CODE_PATTERN = re.compile(r"^[A-Za-z0-9]{6}$")


def validate_pickup_contact(contact: PickupContact) -> ValidationResult:
    errors: list[str] = []

    recipient_name = contact.recipient_name.strip()
    if not 1 <= len(recipient_name) <= 40:
        errors.append("recipient_name length must be between 1 and 40")

    if not PHONE_PATTERN.fullmatch(contact.recipient_phone.strip()):
        errors.append("recipient_phone must be in E.164 format")

    if not PICKUP_STATION_PATTERN.fullmatch(contact.pickup_station_id.strip()):
        errors.append("pickup_station_id must match PS- followed by 6 digits")

    note = (contact.note or "").strip()
    if len(note) > 120:
        errors.append("note must not exceed 120 characters")

    pickup_code = (contact.pickup_code or "").strip()
    if contact.contactless_pickup:
        if not PICKUP_CODE_PATTERN.fullmatch(pickup_code):
            errors.append("contactless pickup requires a 6-character alphanumeric pickup code")
    elif pickup_code and not PICKUP_CODE_PATTERN.fullmatch(pickup_code):
        errors.append("pickup_code must be exactly 6 alphanumeric characters when provided")

    return ValidationResult(is_valid=not errors, errors=tuple(errors))
