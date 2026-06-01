from __future__ import annotations

from dataclasses import dataclass

from .models import DestinationZone, ShippingMethod


BASE_STANDARD_FEES: dict[DestinationZone, tuple[tuple[float, float], ...]] = {
    "local": ((1.0, 5.0), (5.0, 8.0), (float("inf"), 12.0)),
    "domestic": ((1.0, 8.0), (5.0, 12.0), (float("inf"), 18.0)),
    "international": ((1.0, 20.0), (5.0, 35.0), (float("inf"), 50.0)),
}

EXPRESS_SURCHARGE = {
    "local": 10.0,
    "domestic": 10.0,
    "international": 25.0,
}


@dataclass(frozen=True)
class ShippingQuote:
    destination_zone: DestinationZone
    shipping_method: ShippingMethod
    package_weight_kg: float
    subtotal: float
    fee: float
    reason: str


def _resolve_standard_fee(destination_zone: DestinationZone, package_weight_kg: float) -> float:
    for max_weight, fee in BASE_STANDARD_FEES[destination_zone]:
        if package_weight_kg <= max_weight:
            return fee
    raise RuntimeError("shipping fee tier resolution failed")


def calculate_shipping_fee(
    destination_zone: DestinationZone,
    subtotal: float,
    package_weight_kg: float,
    shipping_method: ShippingMethod = "standard",
) -> ShippingQuote:
    if destination_zone not in BASE_STANDARD_FEES:
        raise ValueError("unsupported destination zone")
    if shipping_method not in {"standard", "express"}:
        raise ValueError("unsupported shipping method")
    if subtotal < 0:
        raise ValueError("subtotal must not be negative")
    if package_weight_kg < 0:
        raise ValueError("package weight must not be negative")
    if shipping_method == "express" and package_weight_kg > 20:
        raise ValueError("express shipping is unavailable above 20 kg")

    standard_fee = _resolve_standard_fee(destination_zone, package_weight_kg)
    if shipping_method == "standard" and destination_zone in {"local", "domestic"} and subtotal >= 100:
        fee = 0.0
        reason = "standard shipping threshold reached"
    elif shipping_method == "express":
        fee = standard_fee + EXPRESS_SURCHARGE[destination_zone]
        reason = "express surcharge applied"
    else:
        fee = standard_fee
        reason = "standard shipping rate applied"

    return ShippingQuote(
        destination_zone=destination_zone,
        shipping_method=shipping_method,
        package_weight_kg=round(package_weight_kg, 2),
        subtotal=round(subtotal, 2),
        fee=round(fee, 2),
        reason=reason,
    )
