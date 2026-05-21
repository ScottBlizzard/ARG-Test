from reference_impl.coupon_discount_engine import apply_coupon


def test_no_coupon_keeps_order_values():
    result = apply_coupon(80, 12, [])

    assert result.status == "accepted"
    assert result.applied_coupon is None
    assert result.subtotal == 80
    assert result.shipping_fee == 12
    assert result.reason == "no coupon applied"


def test_multiple_coupons_are_rejected():
    result = apply_coupon(100, 10, ["SAVE10", "FREESHIP"])

    assert result.status == "rejected"
    assert result.reason == "multiple coupons are not allowed"


def test_unknown_coupon_is_rejected():
    result = apply_coupon(100, 10, ["SAVE30"])

    assert result.status == "rejected"
    assert result.reason == "unknown coupon code"


def test_expired_coupon_is_rejected():
    result = apply_coupon(120, 10, ["SAVE10"], is_expired=True)

    assert result.status == "rejected"
    assert result.reason == "expired coupon"


def test_save10_boundary_below_threshold_is_rejected():
    result = apply_coupon(49, 8, ["SAVE10"])

    assert result.status == "rejected"
    assert result.reason == "subtotal below SAVE10 threshold"
    assert result.subtotal == 49
    assert result.shipping_fee == 8


def test_save10_boundary_on_threshold_is_accepted():
    result = apply_coupon(50, 8, ["SAVE10"])

    assert result.status == "accepted"
    assert result.discount_amount == 5.0
    assert result.subtotal == 45.0
    assert result.shipping_fee == 8


def test_save20_requires_premium_membership():
    result = apply_coupon(120, 10, ["SAVE20"], is_premium=False)

    assert result.status == "rejected"
    assert result.reason == "SAVE20 requires premium membership"


def test_save20_with_sale_items_is_rejected():
    result = apply_coupon(120, 10, ["SAVE20"], is_premium=True, has_sale_items=True)

    assert result.status == "rejected"
    assert result.reason == "SAVE20 cannot be used with sale items"


def test_save20_valid_case_applies_discount():
    result = apply_coupon(100, 10, ["SAVE20"], is_premium=True)

    assert result.status == "accepted"
    assert result.discount_amount == 20.0
    assert result.subtotal == 80.0
    assert result.shipping_fee == 10


def test_freeship_threshold_on_boundary_sets_shipping_to_zero():
    result = apply_coupon(30, 6, ["FREESHIP"])

    assert result.status == "accepted"
    assert result.subtotal == 30
    assert result.shipping_fee == 0.0
