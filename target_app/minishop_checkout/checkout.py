from __future__ import annotations

from .models import CheckoutRequest, CheckoutSummary, PickupContact, ValidationResult
from .payment import validate_payment_card
from .pickup import validate_pickup_contact
from .promotion import apply_coupon
from .shipping import calculate_shipping_fee
from .tax import calculate_order_tax


def calculate_merchandise_subtotal(items) -> float:
    if not items:
        raise ValueError("at least one cart item is required")

    subtotal = 0.0
    for item in items:
        if item.unit_price < 0:
            raise ValueError("item unit_price must not be negative")
        if item.quantity <= 0:
            raise ValueError("item quantity must be positive")
        if item.item_discount < 0:
            raise ValueError("item_discount must not be negative")
        if item.item_discount > item.gross_total():
            raise ValueError("item_discount must not exceed item gross total")
        subtotal += item.net_total()
    return round(subtotal, 2)


class MiniShopCheckoutService:
    """Compact checkout orchestration for the MiniShop Checkout target app."""

    def preview_order(
        self,
        request: CheckoutRequest,
        *,
        current_year: int | None = None,
        current_month: int | None = None,
    ) -> CheckoutSummary:
        merchandise_subtotal = calculate_merchandise_subtotal(request.items)
        shipping_quote = calculate_shipping_fee(
            destination_zone=request.shipping.destination_zone,
            subtotal=merchandise_subtotal,
            package_weight_kg=request.shipping.package_weight_kg,
            shipping_method=request.shipping.shipping_method,
        )

        has_sale_items = any(item.is_sale_item for item in request.items)
        coupon_result = apply_coupon(
            merchandise_subtotal,
            shipping_quote.fee,
            list(request.coupons),
            is_premium=request.customer.is_premium,
            has_sale_items=has_sale_items,
            is_expired=request.coupon_is_expired,
        )

        tax_breakdown = calculate_order_tax(
            country_code=request.shipping.country_code,
            net_subtotal=coupon_result.subtotal,
            shipping_fee=coupon_result.shipping_fee,
        )

        payment_validation = ValidationResult(is_valid=True)
        if request.payment_card is not None:
            payment_validation = validate_payment_card(
                request.payment_card,
                current_year=current_year,
                current_month=current_month,
            )

        pickup_validation = ValidationResult(is_valid=True)
        if request.fulfillment_mode == "pickup":
            pickup_contact = request.pickup_contact or PickupContact(
                recipient_name="",
                recipient_phone="",
                pickup_station_id="",
                contactless_pickup=False,
            )
            pickup_validation = validate_pickup_contact(pickup_contact)

        notes = [shipping_quote.reason]
        if coupon_result.reason:
            notes.append(coupon_result.reason)
        if not payment_validation.is_valid:
            notes.append("payment input requires correction")
        if not pickup_validation.is_valid:
            notes.append("pickup information requires correction")

        return CheckoutSummary(
            merchandise_subtotal=merchandise_subtotal,
            discounted_subtotal=round(coupon_result.subtotal, 2),
            shipping_fee=round(coupon_result.shipping_fee, 2),
            discount_amount=round(coupon_result.discount_amount, 2),
            tax_amount=round(tax_breakdown.tax_amount, 2),
            order_total=round(tax_breakdown.order_total, 2),
            applied_coupon=coupon_result.applied_coupon,
            coupon_status=coupon_result.status,
            promotion_reason=coupon_result.reason,
            payment_validation=payment_validation,
            pickup_validation=pickup_validation,
            notes=tuple(notes),
        )
