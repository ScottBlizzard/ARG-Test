from target_app.minishop_checkout import (
    CartItem,
    CheckoutRequest,
    CustomerProfile,
    MiniShopCheckoutService,
    PaymentCardInput,
    PickupContact,
    ShippingRequest,
    calculate_shipping_fee,
    validate_payment_card,
    validate_pickup_contact,
)


def test_shipping_fee_is_free_for_domestic_standard_orders_at_threshold():
    quote = calculate_shipping_fee("domestic", subtotal=100, package_weight_kg=3.5, shipping_method="standard")

    assert quote.fee == 0.0
    assert quote.reason == "standard shipping threshold reached"


def test_payment_validation_rejects_masked_card_number():
    result = validate_payment_card(
        PaymentCardInput(
            cardholder_name="Alice Smith",
            card_number="4111 **** **** 1111",
            expiry_month=12,
            expiry_year=2030,
            cvv="123",
            card_brand="visa",
        ),
        current_year=2026,
        current_month=1,
    )

    assert not result.is_valid
    assert "masked card numbers are not accepted as primary input" in result.errors


def test_pickup_validation_requires_code_for_contactless_pickup():
    result = validate_pickup_contact(
        PickupContact(
            recipient_name="Bob",
            recipient_phone="+8613812345678",
            pickup_station_id="PS-123456",
            contactless_pickup=True,
            pickup_code="",
        )
    )

    assert not result.is_valid
    assert "contactless pickup requires a 6-character alphanumeric pickup code" in result.errors


def test_checkout_preview_applies_coupon_and_computes_tax():
    service = MiniShopCheckoutService()
    request = CheckoutRequest(
        customer=CustomerProfile(customer_id="cust-001", is_premium=True),
        items=(
            CartItem(sku="SKU-1", unit_price=60.0, quantity=1),
            CartItem(sku="SKU-2", unit_price=50.0, quantity=1),
        ),
        shipping=ShippingRequest(
            destination_zone="domestic",
            shipping_method="standard",
            package_weight_kg=2.0,
            country_code="US",
        ),
        coupons=("SAVE20",),
    )

    summary = service.preview_order(request, current_year=2026, current_month=1)

    assert summary.coupon_status == "accepted"
    assert summary.applied_coupon == "SAVE20"
    assert summary.discount_amount == 22.0
    assert summary.discounted_subtotal == 88.0
    assert summary.shipping_fee == 0.0
    assert summary.tax_amount == 7.04
    assert summary.order_total == 95.04


def test_checkout_preview_reports_invalid_payment_without_breaking_order_math():
    service = MiniShopCheckoutService()
    request = CheckoutRequest(
        customer=CustomerProfile(customer_id="cust-002", is_premium=False),
        items=(CartItem(sku="SKU-3", unit_price=80.0, quantity=1),),
        shipping=ShippingRequest(
            destination_zone="local",
            shipping_method="standard",
            package_weight_kg=0.5,
            country_code="CN",
        ),
        coupons=("SAVE10",),
        payment_card=PaymentCardInput(
            cardholder_name="A",
            card_number="4111111111111",
            expiry_month=3,
            expiry_year=2025,
            cvv="12",
            card_brand="visa",
        ),
    )

    summary = service.preview_order(request, current_year=2026, current_month=1)

    assert not summary.payment_validation.is_valid
    assert summary.discount_amount == 8.0
    assert summary.discounted_subtotal == 72.0
    assert summary.shipping_fee == 5.0
    assert summary.tax_amount == 9.36
    assert summary.order_total == 86.36
