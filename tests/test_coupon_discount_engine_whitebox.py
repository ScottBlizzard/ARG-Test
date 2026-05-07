import pytest

from reference_impl.coupon_discount_engine import apply_coupon


def test_negative_subtotal_raises_value_error():
    with pytest.raises(ValueError, match="subtotal must not be negative"):
        apply_coupon(-1, 10, ["SAVE10"])


def test_negative_shipping_fee_raises_value_error():
    with pytest.raises(ValueError, match="shipping fee must not be negative"):
        apply_coupon(50, -1, ["SAVE10"])


def test_save20_below_threshold_keeps_original_values():
    result = apply_coupon(99, 9, ["SAVE20"], is_premium=True)

    assert result.status == "rejected"
    assert result.reason == "subtotal below SAVE20 threshold"
    assert result.subtotal == 99
    assert result.shipping_fee == 9


def test_freeship_below_threshold_is_rejected():
    result = apply_coupon(29, 6, ["FREESHIP"])

    assert result.status == "rejected"
    assert result.reason == "subtotal below FREESHIP threshold"
    assert result.shipping_fee == 6


def test_coupon_normalization_accepts_mixed_case_and_spacing():
    result = apply_coupon(60, 8, ["  save10  "])

    assert result.status == "accepted"
    assert result.applied_coupon == "SAVE10"
    assert result.subtotal == 54.0
