# Target Application Definition

## 1. Purpose

This note fixes the most important project-level distinction for the final submission:

- `ARG-Test` is the **AutoTestDesign tool**
- `MiniShop Checkout` is the **independent application under test**
- `coupon_discount_engine` is the **selected major module** of `MiniShop Checkout` used for the detailed execution document

The risk analysis report, test plan, detailed test design and execution document, and future presentation wording should all follow this same separation.

---

## 2. Target Application Statement

The independent application under test in this final project is **MiniShop Checkout**.

`MiniShop Checkout` is a compact, course-project-level **e-commerce checkout prototype** implemented in:

- `target_app/minishop_checkout/`

It is presented in this repository as a concrete implementation adapted from a previous small course project, so that the final submission contains not only a testing tool, but also a concrete application that the tool can test.

`MiniShop Checkout` is independent from `ARG-Test`. `ARG-Test` analyzes its requirements and helps generate test artifacts, but it is not itself the application under test.

---

## 3. Business Scope of MiniShop Checkout

`MiniShop Checkout` models the core decision-heavy portion of a small e-commerce order flow. Its scope is intentionally limited to the checkout stage so that the application remains compact, but it is still concrete enough to count as a real target application rather than a loose scenario description.

### 3.1 Implemented Functional Areas

| Functional area | Main purpose | Main code path | Requirement basis |
| --- | --- | --- | --- |
| Cart and order preview | represent cart items and compute merchandise subtotal | `target_app/minishop_checkout/models.py`, `target_app/minishop_checkout/checkout.py` | checkout subtotal assumptions used by promotion, shipping, and tax rules |
| Promotion and coupon service | validate coupons and apply discount or free-shipping rules | `target_app/minishop_checkout/promotion.py`, `reference_impl/coupon_discount_engine.py` | `coupon_discount_engine` |
| Shipping calculation | calculate standard/express shipping fees by zone, weight, and threshold | `target_app/minishop_checkout/shipping.py` | `shipping_fee_calculator` |
| Tax and total calculation | calculate taxable amount, tax, and final order total | `target_app/minishop_checkout/tax.py` | `order_total_tax_calculation` |
| Payment input validation | validate cardholder name, card number, expiry, CVV, and brand-specific rules | `target_app/minishop_checkout/payment.py` | `payment_card_expiry_and_cvv_validation` |
| Pickup fulfillment validation | validate pickup station ID, recipient phone, name, and contactless pickup code | `target_app/minishop_checkout/pickup.py` | `pickup_station_contact_validation` |
| Checkout orchestration | assemble the above modules into one checkout-preview flow | `target_app/minishop_checkout/checkout.py` | integration of coupon, shipping, tax, payment, and pickup concerns |

### 3.2 Out-of-Scope Areas

The following areas are not part of the concrete `MiniShop Checkout` application scope:

- order history and after-sales service
- gift-card combination and multi-coupon stack optimization
- refund execution and return approval workflows
- external payment gateway integration
- inventory synchronization and warehouse dispatch
- production web deployment

Some requirement files in the broader repository cover adjacent e-commerce scenarios. They remain useful for **tool evaluation**, but they are not the core definition of the chosen target application for `02`, `03`, and `04`.

---

## 4. Target Application Architecture

The architecture of `MiniShop Checkout` is small but explicit:

| Layer / component | Main responsibility | Main code path |
| --- | --- | --- |
| Client input layer | collects cart, shipping, payment, coupon, and pickup data | conceptual input layer for demo / CLI use |
| Checkout service | coordinates subtotal, promotion, shipping, tax, and validation steps | `target_app/minishop_checkout/checkout.py` |
| Promotion service | applies coupon rules and promotion restrictions | `target_app/minishop_checkout/promotion.py`, `reference_impl/coupon_discount_engine.py` |
| Shipping service | computes standard or express shipping fee | `target_app/minishop_checkout/shipping.py` |
| Tax service | computes taxable amount and final tax | `target_app/minishop_checkout/tax.py` |
| Payment validation service | validates card inputs before checkout confirmation | `target_app/minishop_checkout/payment.py` |
| Pickup validation service | validates pickup recipient and station information | `target_app/minishop_checkout/pickup.py` |

This is the **application architecture** that should be referenced in the risk report and the test plan.

---

## 5. Selected Major Module for Detailed Execution

The selected major feature/module for detailed test design and execution is:

- `coupon_discount_engine`

Its role inside `MiniShop Checkout` is:

- to serve as the promotion-service coupon engine
- to preserve the strongest existing executable test evidence in the repository
- to connect requirement-driven design with `pytest`, `coverage.py`, and mutation-based usefulness evidence

The detailed module implementation remains here:

- `reference_impl/coupon_discount_engine.py`

The target application calls this module through:

- `target_app/minishop_checkout/promotion.py`
- `target_app/minishop_checkout/checkout.py`

So after the remediation, `coupon_discount_engine` is no longer just an isolated reference script. It is a real module inside the selected target application.

---

## 6. Relation to ARG-Test

`ARG-Test` supports the testing of `MiniShop Checkout` by:

1. ingesting checkout-related requirements
2. structuring requirement traces
3. assigning risk and priority
4. generating black-box suites with EP, BVA, Decision Table, and State Transition obligations where applicable
5. exporting auditable test artifacts
6. supporting designer review and revision

Accordingly:

- the **risk analysis report** must analyze `MiniShop Checkout`
- the **test plan** must plan testing for `MiniShop Checkout`
- the **detailed test design and execution document** may focus on `coupon_discount_engine`, because it is one major module of `MiniShop Checkout`

---

## 7. Honest Boundaries

The following boundaries should remain explicit:

- `MiniShop Checkout` is a compact course-project application prototype, not a production deployment
- the repository still contains a broader e-commerce requirement corpus used to evaluate `ARG-Test` as a tool
- `coupon_discount_engine` has the strongest full execution evidence, while the other `MiniShop Checkout` modules currently provide application structure plus smoke-level executable support

These boundaries are acceptable for the course project as long as the final submission describes them accurately.

---

## 8. Final Wording to Reuse

The safest wording for the final submission is:

> The independent application under test is MiniShop Checkout, a compact e-commerce checkout prototype adapted from a previous small course project and implemented in `target_app/minishop_checkout/`. `coupon_discount_engine` is the selected major module of MiniShop Checkout used for detailed test design, execution, and white-box evidence. `ARG-Test` is the AutoTestDesign tool used to analyze MiniShop Checkout requirements and generate test artifacts.
