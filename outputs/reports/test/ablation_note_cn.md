# 5 号 Ablation / Generalization 说明（test split）

Ablation 数据取自 `outputs/reports/test/ablation_summary.json`（运行配置为 mock：`provider=mock`，`model=mock-arg-test`，`candidates=3`）。Generalization 由 `experiments/run_generalization.py` 根据 `outputs/reports/test/run_main_summary.json` 与 `data/requirements/manifest.json` 聚合得到。当前仓库中主实验 metrics 与 ablation 的 **full_pipeline** 臂一致，故 generalization 表中的类均值可与本文一并核对。

## 正式输出文件

- `outputs/reports/test/ablation_summary.json`
- `outputs/reports/test/tables/ablation_summary_table.csv`
- `outputs/reports/test/tables/ablation_summary_table.md`
- `outputs/reports/test/generalization_by_category.json`
- `outputs/reports/test/tables/generalization_by_category.csv`
- `outputs/reports/test/tables/generalization_by_category.md`

## Ablation 结论

- **structured-no-checker 与 full pipeline 的总体差异：** test 分割共 **10** 条需求。其中 **7** 条在两臂下 **`overall_coverage` 及各分项 `coverage` 完全一致**，涉及 `address_international_format_validation`、`bank_transfer_rule_checker`、`checkout_promo_stack_and_priority`、`coupon_discount_engine`、`gift_card_and_coupon_combination_rules`、`return_refund_method_eligibility`、`ticket_booking_refund_rule`。其余差异主要体现在 **`checker_score` 由 0.65 升至 0.75（部分需求维持 0.65）**，以及 **`test_count` 在个别需求上增加 1～2**。`order_approval_state_machine`：`overall_coverage` 由 **0.286 升至 0.31**，`state_coverage` 由 **0 升至 0.167**，`checker_score` 由 **约 0.85 升至约 0.95**。`order_split_shipment_state_machine`：两臂 **`overall_coverage` 均为 0.143**，`test_count` 由 **4 增至 6**，`checker_score` 由 **约 0.75 升至约 0.85**。`payment_3ds_authentication_flow`：两臂 **`overall_coverage` 均为 0.071**，`test_count` 由 **4 增至 5**，`checker_score` 由 **约 0.85 升至约 0.95**。

- **repair 的可见影响：** `full_pipeline` 中 **`repaired: true`** 共 8 条，**`repaired: false`** 为 `order_approval_state_machine` 与 `payment_3ds_authentication_flow`。对 `checkout_promo_stack_and_priority`、`gift_card_and_coupon_combination_rules`、`return_refund_method_eligibility`，两臂在 **coverage、checker、test_count** 上完全一致；虽标记为 `repaired: true`，**摘要 JSON 中几乎观察不到修复带来的数值变化**，与仍存在的 schema 类问题相一致（详见 `failure_analysis_cn.md`）。

- **checker-aware control 的可见影响：** 全部 10 条需求的 **full_pipeline `checker_score` 均不低于 structured 臂**。多数需求在 gold 侧 **双臂覆盖不变**，表明在当前 mock 配置下 **契约得分的改善与相对 gold 的覆盖改善并不同步**；仅 `order_approval_state_machine` 等少数条目出现 **覆盖与 checker 同步小幅上升**。

## Requirement-Type / Generalization 结论

- **business_rules 类：** `requirement_count=6`，`avg_checker_score=0.7`，`avg_overall_coverage≈0.366`，`avg_test_count=4.5`，`avg_duplicate_count=0.0`。条间 `overall_coverage` 分布在约 **0.286～0.571**（`coupon_discount_engine` 最高，若干促销、礼品卡与退款组合类需求接近 **0.286**）。撰写报告时宜 **对照单需求表**，不宜仅凭类均值概括全部条目。

- **input_validation 类：** `requirement_count=1`（`address_international_format_validation`），`avg_checker_score=0.75`，`avg_overall_coverage≈0.327`，`avg_test_count=6.0`。该类 **仅有单一需求**，类层面统计 **不宜推广到所有输入校验类题目**。

- **workflow_state 类：** `requirement_count=3`，`avg_checker_score≈0.917` 偏高，而 **`avg_overall_coverage≈0.175` 明显低于** business_rules 与 input_validation，表明工作流类需求在 gold 维度上 **整体更难取得高覆盖**；其中 `payment_3ds_authentication_flow` 覆盖极低，**显著拉低类别均值**。

- **类别间对比：** 同时存在 **workflow_state：checker 偏高而 gold 覆盖均值偏低**，以及 **business_rules：覆盖离散度较大** 两种格局。跨类比较可置于「按需求类型泛化」一节，并说明 **input_validation 仅 1 条、workflow_state 仅 3 条** 所带来的统计局限。

## 可直接给张洛梧使用的结果解释

**主结果（test 规模与指标含义）**  
在 test **10** 条需求上，full pipeline 相对 structured-no-checker **在多数条目中提高或维持 checker 得分**；另有约 **7** 条在双臂下 **gold 的 `overall_coverage` 与分项覆盖保持不变**。叙述主方法贡献时，宜 **并列说明契约得分与相对 gold 的覆盖**，以免读者将 checker 提升 **直接等同于** 测试套件在 gold 意义上的完备性提高。

**消融（两臂差异与 repair）**  
`order_approval_state_machine` 与 `payment_3ds_authentication_flow` 在 full 臂为 **`repaired: false`**，表明轻量修复流程 **未在这两条上判定为成功**。`checkout_promo_stack_and_priority`、`gift_card_and_coupon_combination_rules`、`return_refund_method_eligibility` 虽为 **`repaired: true`**，两臂在 **coverage、checker、用例数** 上仍完全一致，可在 limitation 中用于讨论 **修复效果是否体现在可引用的摘要指标中**。

**按需求类别的泛化**  
`business_rules` 共六条，类平均覆盖约 **0.37**、checker 约 **0.70**，单条覆盖约介于 **0.29～0.57**；`workflow_state` 三条平均覆盖约 **0.18**、checker 约 **0.92**，表现为 **得分较高而 gold 覆盖均值偏低**；`input_validation` 当前仅一条，覆盖约 **0.33**，**不宜由该类均值外推**。正文建议 **同时给出 `ablation_summary_table` 与 `generalization_by_category` 表**，再辅以定性归纳，避免仅凭类均值 **掩盖单条需求之间的差异**。
