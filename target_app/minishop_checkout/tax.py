from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


TAX_RATES = {
    "US": Decimal("0.08"),
    "CN": Decimal("0.13"),
}


@dataclass(frozen=True)
class TaxBreakdown:
    country_code: str
    taxable_amount: float
    tax_rate: float
    tax_amount: float
    order_total: float


def _money(value: float) -> Decimal:
    return Decimal(str(round(value, 2)))


def calculate_order_tax(country_code: str, net_subtotal: float, shipping_fee: float) -> TaxBreakdown:
    if net_subtotal < 0:
        raise ValueError("net subtotal must not be negative")
    if shipping_fee < 0:
        raise ValueError("shipping fee must not be negative")

    normalized_country = country_code.strip().upper()
    tax_rate = TAX_RATES.get(normalized_country, Decimal("0"))
    taxable_amount = _money(net_subtotal + shipping_fee) if normalized_country == "US" else _money(net_subtotal)
    tax_amount = (taxable_amount * tax_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    order_total = (_money(net_subtotal) + _money(shipping_fee) + tax_amount).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    return TaxBreakdown(
        country_code=normalized_country,
        taxable_amount=float(taxable_amount),
        tax_rate=float(tax_rate),
        tax_amount=float(tax_amount),
        order_total=float(order_total),
    )
