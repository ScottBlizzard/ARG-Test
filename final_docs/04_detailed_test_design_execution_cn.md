# Detailed Test Design and Execution Draft

## 1. Selected Major Module

建议选定：

- `coupon_discount_engine`

## 2. Why this module

该模块最适合作为 final 的详细测试设计对象，因为它同时具备：

- 输入有效/无效划分
- 数值边界
- 多条件业务规则
- 明确的 expected output
- 易于补 reference implementation 进行 white-box 执行

## 3. Requirement Summary

从当前数据与样例输出可抽取的核心规则包括：

- only one coupon can be applied
- `SAVE10` requires subtotal >= 50
- `SAVE20` requires subtotal >= 100 and premium membership
- `FREESHIP` requires subtotal >= 30
- expired coupons are invalid
- `SAVE20` cannot be used with sale items

## 4. Black-Box Test Design

### 4.1 Equivalence Partitioning

- valid coupon + valid threshold
- valid coupon + unmet threshold
- expired coupon
- premium-only coupon used by non-premium member
- restricted combination with sale items

### 4.2 Boundary Value Analysis

- subtotal around 30
- subtotal around 50
- subtotal around 100

### 4.3 Decision Table Testing

重点条件：

- coupon type
- subtotal threshold reached or not
- premium membership
- sale item presence
- expiry status

重点动作：

- accept coupon
- reject coupon
- apply discount percent
- set shipping fee to zero

## 5. White-Box Test Design

### 5.1 Planned implementation

在 final 阶段补一个小型 reference implementation，例如：

- `coupon_engine.py`

函数可包含以下决策点：

- coupon type dispatch
- expiry validation
- threshold checks
- membership checks
- sale-item restriction checks
- final discount/shipping calculation

### 5.2 White-box objectives

- statement coverage
- branch coverage
- condition coverage for critical boolean combinations

### 5.3 White-box framework

- `pytest`
- `coverage.py` or equivalent pytest coverage plugin

## 6. Execution Evidence to Collect

final 版详细文档建议至少保留下列证据：

- manually curated final test case table
- decision table
- selected boundary rationale
- pytest run output
- branch or statement coverage summary
- failing tests on seeded defects or mutants if time permits

## 7. Expected Final Structure of This Document

### Section A

- feature background
- requirement text
- scope and assumptions

### Section B

- black-box design
- EP table
- BVA table
- decision table

### Section C

- white-box design
- control-flow or branch discussion
- mapping from branches to tests

### Section D

- execution results
- pass/fail summary
- coverage summary
- defect or weakness analysis

## 8. Strong-version upgrade

为了超过老师最低要求，建议 detailed execution 再多做一步：

- 对 reference implementation 人工植入 2 到 3 个小缺陷
- 用生成的测试和人工补强后的测试去检验 defect detection ability

这样 final 报告里就不只是“设计了测试”，而是能展示“这些测试确实能发现问题”。
