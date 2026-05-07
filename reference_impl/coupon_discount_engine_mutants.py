from __future__ import annotations

from .coupon_discount_engine import CouponApplicationResult, KNOWN_COUPONS, _accepted, _normalize_coupons, _rejected


def apply_coupon_mutant_multiple_coupons_allowed(
    subtotal: float,
    shipping_fee: float,
    coupons: list[str] | None = None,
    *,
    is_premium: bool = False,
    has_sale_items: bool = False,
    is_expired: bool = False,
) -> CouponApplicationResult:
    if subtotal < 0:
        raise ValueError("subtotal must not be negative")
    if shipping_fee < 0:
        raise ValueError("shipping fee must not be negative")

    normalized_coupons = _normalize_coupons(coupons)
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
        return _accepted(round(subtotal - discount_amount, 2), shipping_fee, discount_amount, coupon)

    if coupon == "SAVE20":
        if not is_premium:
            return _rejected(subtotal, shipping_fee, "SAVE20 requires premium membership", applied_coupon=coupon)
        if subtotal < 100:
            return _rejected(subtotal, shipping_fee, "subtotal below SAVE20 threshold", applied_coupon=coupon)
        discount_amount = round(subtotal * 0.20, 2)
        return _accepted(round(subtotal - discount_amount, 2), shipping_fee, discount_amount, coupon)

    if subtotal < 30:
        return _rejected(subtotal, shipping_fee, "subtotal below FREESHIP threshold", applied_coupon=coupon)
    return _accepted(subtotal, 0.0, 0.0, coupon)


def apply_coupon_mutant_save10_boundary_bug(
    subtotal: float,
    shipping_fee: float,
    coupons: list[str] | None = None,
    *,
    is_premium: bool = False,
    has_sale_items: bool = False,
    is_expired: bool = False,
) -> CouponApplicationResult:
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
        if subtotal <= 50:
            return _rejected(subtotal, shipping_fee, "subtotal below SAVE10 threshold", applied_coupon=coupon)
        discount_amount = round(subtotal * 0.10, 2)
        return _accepted(round(subtotal - discount_amount, 2), shipping_fee, discount_amount, coupon)

    if coupon == "SAVE20":
        if has_sale_items:
            return _rejected(subtotal, shipping_fee, "SAVE20 cannot be used with sale items", applied_coupon=coupon)
        if not is_premium:
            return _rejected(subtotal, shipping_fee, "SAVE20 requires premium membership", applied_coupon=coupon)
        if subtotal < 100:
            return _rejected(subtotal, shipping_fee, "subtotal below SAVE20 threshold", applied_coupon=coupon)
        discount_amount = round(subtotal * 0.20, 2)
        return _accepted(round(subtotal - discount_amount, 2), shipping_fee, discount_amount, coupon)

    if subtotal < 30:
        return _rejected(subtotal, shipping_fee, "subtotal below FREESHIP threshold", applied_coupon=coupon)
    return _accepted(subtotal, 0.0, 0.0, coupon)


def apply_coupon_mutant_save20_sale_item_bug(
    subtotal: float,
    shipping_fee: float,
    coupons: list[str] | None = None,
    *,
    is_premium: bool = False,
    has_sale_items: bool = False,
    is_expired: bool = False,
) -> CouponApplicationResult:
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
        return _accepted(round(subtotal - discount_amount, 2), shipping_fee, discount_amount, coupon)

    if coupon == "SAVE20":
        if not is_premium:
            return _rejected(subtotal, shipping_fee, "SAVE20 requires premium membership", applied_coupon=coupon)
        if subtotal < 100:
            return _rejected(subtotal, shipping_fee, "subtotal below SAVE20 threshold", applied_coupon=coupon)
        discount_amount = round(subtotal * 0.20, 2)
        return _accepted(round(subtotal - discount_amount, 2), shipping_fee, discount_amount, coupon)

    if subtotal < 30:
        return _rejected(subtotal, shipping_fee, "subtotal below FREESHIP threshold", applied_coupon=coupon)
    return _accepted(subtotal, 0.0, 0.0, coupon)


def apply_coupon_mutant_freeship_boundary_bug(
    subtotal: float,
    shipping_fee: float,
    coupons: list[str] | None = None,
    *,
    is_premium: bool = False,
    has_sale_items: bool = False,
    is_expired: bool = False,
) -> CouponApplicationResult:
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
        return _accepted(round(subtotal - discount_amount, 2), shipping_fee, discount_amount, coupon)

    if coupon == "SAVE20":
        if has_sale_items:
            return _rejected(subtotal, shipping_fee, "SAVE20 cannot be used with sale items", applied_coupon=coupon)
        if not is_premium:
            return _rejected(subtotal, shipping_fee, "SAVE20 requires premium membership", applied_coupon=coupon)
        if subtotal < 100:
            return _rejected(subtotal, shipping_fee, "subtotal below SAVE20 threshold", applied_coupon=coupon)
        discount_amount = round(subtotal * 0.20, 2)
        return _accepted(round(subtotal - discount_amount, 2), shipping_fee, discount_amount, coupon)

    if subtotal <= 30:
        return _rejected(subtotal, shipping_fee, "subtotal below FREESHIP threshold", applied_coupon=coupon)
    return _accepted(subtotal, 0.0, 0.0, coupon)


COUPON_MUTANTS = {
    "multiple_coupons_allowed": {
        "description": "Mutant ignores the one-coupon-only rule and silently uses the first coupon.",
        "callable": apply_coupon_mutant_multiple_coupons_allowed,
    },
    "save10_boundary_bug": {
        "description": "Mutant rejects SAVE10 exactly at subtotal 50.",
        "callable": apply_coupon_mutant_save10_boundary_bug,
    },
    "save20_sale_item_bug": {
        "description": "Mutant ignores the SAVE20 sale-item restriction.",
        "callable": apply_coupon_mutant_save20_sale_item_bug,
    },
    "freeship_boundary_bug": {
        "description": "Mutant rejects FREESHIP exactly at subtotal 30.",
        "callable": apply_coupon_mutant_freeship_boundary_bug,
    },
}
