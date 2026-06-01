# MiniShop Checkout

`MiniShop Checkout` is the independent target application used by the final-project deliverables in this repository.

It is intentionally small enough for a course project, but concrete enough to count as an actual application under test rather than a loose business scenario.

## Application scope

The prototype covers the core checkout flow of a small e-commerce system:

- cart items and merchandise subtotal
- coupon and promotion handling
- shipping-fee calculation
- order tax and total calculation
- payment-card input validation
- pickup-contact validation

## Code structure

| File | Responsibility |
| --- | --- |
| `models.py` | domain objects for checkout, customer, shipping, payment, and pickup |
| `checkout.py` | end-to-end checkout orchestration for order preview |
| `promotion.py` | promotion-service entry point; reuses the detailed-execution coupon engine |
| `shipping.py` | shipping fee calculation |
| `tax.py` | tax and order-total calculation |
| `payment.py` | payment-card validation |
| `pickup.py` | pickup-station contact validation |

## Relation to the detailed execution module

The promotion service uses the existing `reference_impl/coupon_discount_engine.py` implementation as its coupon module.

This keeps the final project's strongest detailed execution evidence intact:

- black-box `pytest` tests
- white-box `pytest` tests
- full statement and branch coverage
- mutation-based usefulness evidence

Within the target application, `coupon_discount_engine` is therefore a real application module rather than a standalone orphan script.

## Why this structure matters

The assignment requires both:

1. an AI-driven AutoTestDesign tool, and
2. an independent application under test.

`ARG-Test` is the tool. `MiniShop Checkout` is the application under test. The detailed document then focuses on one major module of that application: `coupon_discount_engine`.
