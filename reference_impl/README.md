# Reference Implementations

This directory stores executable reference modules used to support the final project's detailed test design and execution document for the independent target application.

Current module:

- `coupon_discount_engine.py`: the coupon module used by the `MiniShop Checkout` target application's promotion service.

Purpose:

- preserve a stable detailed-execution module for black-box and white-box testing
- support `pytest` execution evidence
- support branch/condition coverage discussion in the final report
- serve as the promotion-engine implementation imported by `target_app/minishop_checkout/promotion.py`
