from __future__ import annotations

from dataclasses import dataclass


KNOWN_COUPONS = {"SAVE10", "SAVE20", "FREESHIP"}


@dataclass(frozen=True)
class CouponApplicationResult:
    status: str
    applied_coupon: str | None
    subtotal: float
    shipping_fee: float
    discount_amount: float
    reason: str | None = None


def _normalize_coupons(coupons: list[str] | None) -> list[str]:
    return [coupon.strip().upper() for coupon in coupons or [] if coupon and coupon.strip()]


def _accepted(
    subtotal: float,
    shipping_fee: float,
    discount_amount: float = 0.0,
    applied_coupon: str | None = None,
    reason: str | None = None,
) -> CouponApplicationResult:
    return CouponApplicationResult(
        status="accepted",
        applied_coupon=applied_coupon,
        subtotal=round(subtotal, 2),
        shipping_fee=round(shipping_fee, 2),
        discount_amount=round(discount_amount, 2),
        reason=reason,
    )


def _rejected(
    subtotal: float,
    shipping_fee: float,
    reason: str,
    applied_coupon: str | None = None,
) -> CouponApplicationResult:
    return CouponApplicationResult(
        status="rejected",
        applied_coupon=applied_coupon,
        subtotal=round(subtotal, 2),
        shipping_fee=round(shipping_fee, 2),
        discount_amount=0.0,
        reason=reason,
    )


def apply_coupon(
    subtotal: float,
    shipping_fee: float,
    coupons: list[str] | None = None,
    *,
    is_premium: bool = False,
    has_sale_items: bool = False,
    is_expired: bool = False,
) -> CouponApplicationResult:
    """Apply a coupon according to the coupon_discount_engine requirement."""
    if subtotal < 0:
        raise ValueError("subtotal must not be negative")
    if shipping_fee < 0:
        raise ValueError("shipping fee must not be negative")

    normalized_coupons = _normalize_coupons(coupons)
    if len(normalized_coupons) > 1:
        return _rejected(subtotal, shipping_fee, "multiple coupons are not allowed")
    if not normalized_coupons:
        return _accepted(subtotal, shipping_fee, reason="no coupon applied")

    coupon = normalized_coupons[0]
    if coupon not in KNOWN_COUPONS:
        return _rejected(subtotal, shipping_fee, "unknown coupon code", applied_coupon=coupon)
    if is_expired:
        return _rejected(subtotal, shipping_fee, "expired coupon", applied_coupon=coupon)

    if coupon == "SAVE10":
        if subtotal < 50:
            return _rejected(subtotal, shipping_fee, "subtotal below SAVE10 threshold", applied_coupon=coupon)
        discount_amount = round(subtotal * 0.10, 2)
        discounted_subtotal = max(0.0, round(subtotal - discount_amount, 2))
        return _accepted(
            discounted_subtotal,
            shipping_fee,
            discount_amount=discount_amount,
            applied_coupon=coupon,
        )

    if coupon == "SAVE20":
        if has_sale_items:
            return _rejected(subtotal, shipping_fee, "SAVE20 cannot be used with sale items", applied_coupon=coupon)
        if not is_premium:
            return _rejected(subtotal, shipping_fee, "SAVE20 requires premium membership", applied_coupon=coupon)
        if subtotal < 100:
            return _rejected(subtotal, shipping_fee, "subtotal below SAVE20 threshold", applied_coupon=coupon)
        discount_amount = round(subtotal * 0.20, 2)
        discounted_subtotal = max(0.0, round(subtotal - discount_amount, 2))
        return _accepted(
            discounted_subtotal,
            shipping_fee,
            discount_amount=discount_amount,
            applied_coupon=coupon,
        )

    if subtotal < 30:
        return _rejected(subtotal, shipping_fee, "subtotal below FREESHIP threshold", applied_coupon=coupon)
    return _accepted(
        subtotal,
        0.0,
        discount_amount=0.0,
        applied_coupon=coupon,
    )
