# Failure Analysis（test split）

## 本次分析使用的正式结果

- `outputs/reports/test/ablation_summary.json`
- `outputs/reports/test/generalization_by_category.json`
- `artifacts/checker_logs/test/`
- `artifacts/parsed_traces/test/`
- `outputs/final_tests/test/`

个案溯源时可对照 `artifacts/raw_generations/test/{requirement_id}_candidate_*.md` 中的原始生成文本。

## 失败模式 1

- **名称：** Verification 与步骤编号不一致（schema 未通过）
- **典型 requirement ID：** `checkout_promo_stack_and_priority`，`gift_card_and_coupon_combination_rules`（同类形态亦见于 `return_refund_method_eligibility`）
- **相关文件路径：**
  - `artifacts/checker_logs/test/checkout_promo_stack_and_priority.json`
  - `artifacts/checker_logs/test/gift_card_and_coupon_combination_rules.json`
  - `artifacts/parsed_traces/test/checkout_promo_stack_and_priority.json`
  - `outputs/final_tests/test/checkout_promo_stack_and_priority.md`
- **现象：** `schema` 检查未通过，诊断为 `verification references invalid step numbers: [2]`。在 `ablation_summary.json` 中，上述需求的 **`full_pipeline` 与 `structured_no_checker` 在 `overall_coverage`、`checker_score` 上完全一致**（例如 `checkout_promo_stack_and_priority` 均为 0.286 / 0.65），`test_count` 在双臂均为 3，表明 **完整流水线未在摘要指标上带来可观测的覆盖或契约改善**。多条需求呈现同一类 schema 失败形态。
- **原因判断：** **模型、解析与流程层面为主**——Verification 引用了与当前 Steps 枚举不一致的步骤编号，可能源于模板化生成或解析结果未与步骤列表对齐。**Checker 层面为次**——schema 契约准确记录了上述不一致，属于有效诊断，并非误报。
- **建议修复方向：** 在生成或后处理环节约束 Verification 仅引用已存在的步骤编号；解析层输出规范化步骤清单以供校验；对 `test_count` 已饱和的需求，宜优先消除 schema 问题，再评估 repair 的收益。

## 失败模式 2

- **名称：** 相对 gold 的整体覆盖极低，并伴随决策表偏浅或 BVA 缺口
- **典型 requirement ID：** `payment_3ds_authentication_flow`，`order_split_shipment_state_machine`
- **相关文件路径：**
  - `artifacts/checker_logs/test/payment_3ds_authentication_flow.json`
  - `artifacts/checker_logs/test/order_split_shipment_state_machine.json`
  - `outputs/final_tests/test/payment_3ds_authentication_flow.md`
  - `outputs/final_tests/test/order_split_shipment_state_machine.md`
- **现象：** `ablation_summary.json` 中，`payment_3ds_authentication_flow` 的 `overall_coverage` 为 **0.071**（当前 test 子集中最低），`valid_partition_coverage`、`state_coverage`、`illegal_transition_coverage` 等均为 0，仅 `decision_rule_coverage` 为 0.5；`full_pipeline` 为 **`repaired: false`**。`order_split_shipment_state_machine` 的 `overall_coverage` 为 **0.143**，`decision_rule_coverage` 与 `state_coverage` 为 0；`checker_logs` 中 **BVA** 提示缺少上下界用例，**decision_contract** 判定为 shallow。`payment_3ds_authentication_flow` 的终稿仍大量使用 “representative valid input”“legal trigger” 等占位表述，未与 INITIATED、AUTH_REQUIRED 等具体状态及事件相对应。
- **原因判断：** **模型层面为主**——用例未能覆盖 gold 所要求的若干维度（分区、状态迁移、决策行等）。**数据与流程层面为次**——prompt 对工作流类输出未强制「状态名—事件—期望下一状态」等结构。**Checker 与度量层面为次**——`payment_3ds_authentication_flow` 在 checker 总分仍较高而 gold 覆盖极低，说明 **高分与高覆盖不可等同视之**。
- **建议修复方向：** 加强 workflow_state 类 prompt 与 repair 成功判定；针对 `order_split_shipment_state_machine` 补全 BVA 与决策表行级用例；报告中宜 **分列呈现 checker_score 与 overall_coverage**。

## 失败模式 3

- **名称：** 状态机类需求终稿仍以占位为主，full pipeline 未判定 repair 成功，并拖累 workflow 类平均覆盖
- **典型 requirement ID：** `order_approval_state_machine`
- **相关文件路径：**
  - `artifacts/checker_logs/test/order_approval_state_machine.json`
  - `artifacts/parsed_traces/test/order_approval_state_machine.json`
  - `outputs/final_tests/test/order_approval_state_machine.md`
  - `artifacts/raw_generations/test/order_approval_state_machine_candidate_1.md`
- **现象：** `full_pipeline` 为 **`repaired: false`**；`overall_coverage` 约 **0.31**，在 workflow 类题目中优于 `payment_3ds_authentication_flow` 但仍偏低；`decision_contract` 为 shallow。终稿表格的 Input 列多为占位表述，与 Analysis 中 Draft、Submitted 等规则 **未形成逐条对应**。`generalization_by_category.json` 中 **workflow_state** 的 `avg_overall_coverage` 约 **0.175**（三条需求平均），受极低覆盖样本影响明显。
- **原因判断：** **模型层面为主**。**流程层面为次**——repair 未对该需求判定为成功，需核查修复链路与触发条件。`gold_spec_found` 为真，**不属于 gold 缺失**。
- **建议修复方向：** 与失败模式 2 协同，强化状态机输出规范；单独排查 `order_approval_state_machine` 的 repair 逻辑；在 generalization 叙述中说明 **workflow_state 样本量少、条间方差大**。

## 失败模式 4

- **名称：** 业务规则或输入校验类需求仍触发 state_contract 与浅决策表；ablation 中出现边界、决策维度为 0 与终稿表观不一致
- **典型 requirement ID：** `bank_transfer_rule_checker`，`ticket_booking_refund_rule`
- **相关文件路径：**
  - `artifacts/checker_logs/test/bank_transfer_rule_checker.json`
  - `artifacts/checker_logs/test/ticket_booking_refund_rule.json`
  - `outputs/final_tests/test/bank_transfer_rule_checker.md`
  - `outputs/final_tests/test/ticket_booking_refund_rule.md`
- **现象：** `manifest.json` 中二者类别为 **business_rules**（输入校验与规则混合场景可对照 `address_international_format_validation`），但 `checker_logs` 中 **state_contract** 未通过（例如 missing legal/illegal transition；`ticket_booking_refund_rule` 等含 “analysis and steps do not clearly model states…”）。`decision_contract` 普遍为 shallow。`ablation_summary.json` 中 **`bank_transfer_rule_checker` 的 `boundary_coverage` 与 `decision_rule_coverage` 为 0**，而终稿表格中可出现具体金额边界，**摘要指标与表观用例之间易出现解读张力**。
- **原因判断：** **Checker 层面为主**——统一状态类契约作用于非状态主导的需求时，失败信号与「业务规则是否错误」不易一一对应。**模型层面为次**——决策表行级粒度不足。**数据与评测层面为次**——覆盖算法、`covered_item` 与 gold 的对齐方式需由集成负责人核实，以解释 boundary 维度为 0 等现象。
- **建议修复方向：** 按 `category` 对 state 类检查分流或弱化无关项；提升规则类生成的决策行具体性；在方法部分明确覆盖度量的操作化定义。

## 可以写进 limitations 的文字素材

- test 共 10 条需求中，**schema 失败、gold 覆盖极低与终稿占位** 并存，对「单一流水线即可稳定产出可执行用例」的论断宜采取审慎表述。
- `generalization_by_category.json` 中 **input_validation 仅含 1 条**，**workflow_state 条均覆盖偏低**，类别均值的 **可外推性有限**。
- **checker 得分与 overall_coverage 可能出现显著背离**（例如 `payment_3ds_authentication_flow`），报告宜 **同时呈现两类指标**。

## 可以写进 threats to validity 的文字素材

- **Construct validity：** 若将 state_contract 失败直接解释为「状态建模层面的业务错误」，在 business_rules 类需求上可能 **夸大** 该解释，从而影响指标与真实缺陷类型之间的对应关系。
- **内部可解释性：** 当 `boundary_coverage` 等维度为 0 而终稿表格仍含具体边界取值时，若未说明 gold 映射与覆盖算法，将影响读者对数值含义理解的一致性。
- **外部效度：** 当前结果基于 mock provider 的可复现运行；更换真实 LLM 后，失败模式分布可能发生变化，正式结论应以重跑结果为依据。
