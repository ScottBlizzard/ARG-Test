"""MiniShop Checkout target application prototype."""

from .checkout import MiniShopCheckoutService, calculate_merchandise_subtotal
from .models import (
    CartItem,
    CheckoutRequest,
    CheckoutSummary,
    CustomerProfile,
    PaymentCardInput,
    PickupContact,
    ShippingRequest,
    ValidationResult,
)
from .payment import validate_payment_card
from .pickup import validate_pickup_contact
from .promotion import CouponApplicationResult, apply_coupon
from .shipping import ShippingQuote, calculate_shipping_fee
from .tax import TaxBreakdown, calculate_order_tax

__all__ = [
    "CartItem",
    "CheckoutRequest",
    "CheckoutSummary",
    "CouponApplicationResult",
    "CustomerProfile",
    "MiniShopCheckoutService",
    "PaymentCardInput",
    "PickupContact",
    "ShippingQuote",
    "ShippingRequest",
    "TaxBreakdown",
    "ValidationResult",
    "apply_coupon",
    "calculate_merchandise_subtotal",
    "calculate_order_tax",
    "calculate_shipping_fee",
    "validate_payment_card",
    "validate_pickup_contact",
]
