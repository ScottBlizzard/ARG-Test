from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


ShippingMethod = Literal["standard", "express"]
DestinationZone = Literal["local", "domestic", "international"]
FulfillmentMode = Literal["delivery", "pickup"]
CardBrand = Literal["visa", "mastercard", "amex"]


@dataclass(frozen=True)
class CartItem:
    sku: str
    unit_price: float
    quantity: int
    item_discount: float = 0.0
    is_sale_item: bool = False

    def gross_total(self) -> float:
        return round(self.unit_price * self.quantity, 2)

    def net_total(self) -> float:
        return round(self.gross_total() - self.item_discount, 2)


@dataclass(frozen=True)
class CustomerProfile:
    customer_id: str
    is_premium: bool = False


@dataclass(frozen=True)
class ShippingRequest:
    destination_zone: DestinationZone
    shipping_method: ShippingMethod
    package_weight_kg: float
    country_code: str


@dataclass(frozen=True)
class PaymentCardInput:
    cardholder_name: str
    card_number: str
    expiry_month: int
    expiry_year: int
    cvv: str
    card_brand: CardBrand


@dataclass(frozen=True)
class PickupContact:
    recipient_name: str
    recipient_phone: str
    pickup_station_id: str
    contactless_pickup: bool = False
    pickup_code: str | None = None
    note: str | None = None


@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    errors: tuple[str, ...] = ()


@dataclass(frozen=True)
class CheckoutRequest:
    customer: CustomerProfile
    items: tuple[CartItem, ...]
    shipping: ShippingRequest
    coupons: tuple[str, ...] = ()
    fulfillment_mode: FulfillmentMode = "delivery"
    payment_card: PaymentCardInput | None = None
    pickup_contact: PickupContact | None = None
    coupon_is_expired: bool = False


@dataclass(frozen=True)
class CheckoutSummary:
    merchandise_subtotal: float
    discounted_subtotal: float
    shipping_fee: float
    discount_amount: float
    tax_amount: float
    order_total: float
    applied_coupon: str | None
    coupon_status: str
    promotion_reason: str | None
    payment_validation: ValidationResult
    pickup_validation: ValidationResult
    notes: tuple[str, ...] = field(default_factory=tuple)
