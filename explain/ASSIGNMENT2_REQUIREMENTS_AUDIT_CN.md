# 作业 2 要求逐项核对审计（当前状态）

日期：`2026-06-02`

说明：

- 这份文件记录的是**当前整改后的状态**。
- 它取代旧版“整改前状态”审计，不再沿用“对象理解错误尚未修正”的旧结论。
- 当前仓库中的正式交付主线已经统一为：
  - 工具：`ARG-Test`
  - 独立被测应用：`MiniShop Checkout`
  - 详细执行模块：`coupon_discount_engine`

## 0. 总结先说

严格按老师作业要求看，当前项目已经基本走正，核心结论如下：

1. `ARG-Test` 作为 AutoTestDesign 工具已经具备完整主干能力，`FR 1.0 / 1.1 / 2.0 / 3.0 / 6.0` 明确闭合，`FR 4.0 / 5.0 / 7.0` 也有实质实现。
2. 之前最大的偏差是“把工具本体当成测试对象”，这一点现在已经修正。当前三份正式文档都围绕 `MiniShop Checkout` 来写。
3. `coupon_discount_engine` 没有被浪费，而是被正式定位为 `MiniShop Checkout` 的 selected major module，用于 `04` 的详细测试设计与执行。
4. 老师特别强调的 interactive review 现在也已补强：不仅能改 coverage focus 和 strategy guidance，还能在生成后**直接编辑测试用例并重新导出 revised suite**。
5. 目前剩下的主要风险已经不再是“系统或文档方向错误”，而是**最终提交物是否交齐**，尤其是：
   - 实际 `demo video`
   - 完整工具提交压缩包

一句话结论：

> 当前项目从“方向偏了”已经修到“主体合规、只剩提交收口”。  

---

## 1. 这次核对看的是什么

本次核对以当前仓库里的下列材料为准：

- 作业要求：`homework.txt`
- 工具实现：`src/`、`prompts/`、`demo_web/`、`experiments/`
- 独立目标应用：`target_app/minishop_checkout/`
- 三份正式文档：
  - `final_docs/risk_analysis_report/02_risk_analysis_report_cn.md`
  - `final_docs/test_plan/03_test_plan_cn.md`
  - `final_docs/detailed_test_design_execution/04_detailed_test_design_execution_cn.md`
- 执行证据：
  - `final_docs/execution_evidence/`
  - `tests/`
  - `reference_impl/`
- 演示与 PPT 材料：
  - `report_assets/final_demo_package/`
  - `07_PPT_Assets_For_Luowu/final_ppt.pdf`

---

## 2. 对象口径是否正确

### 2.1 工具是什么

工具本体是：

- `ARG-Test`
- 一个 requirement-driven 的 AI AutoTestDesign 工具

它负责：

- requirement 输入与结构化
- 风险分析与优先级
- black-box test design
- state-model extraction
- structured export
- checker-guided rerank / repair

### 2.2 被测应用是什么

当前被测对象已经明确为：

- `MiniShop Checkout`

这是一个小型电商结算原型应用，位于：

- `target_app/minishop_checkout/`

它的主要模块包括：

- promotion / coupon logic
- shipping fee calculation
- tax and total calculation
- payment-card validation
- pickup validation
- checkout orchestration

### 2.3 详细执行模块是什么

详细测试设计与执行文档聚焦：

- `coupon_discount_engine`

它现在的角色是：

- `MiniShop Checkout` 中的 selected major module
- 也是黑盒 + 白盒 + coverage + mutation 的 executable evidence anchor

### 2.4 三份正式文档对象是否正确

- `02 风险分析报告`：现在面向 `MiniShop Checkout`
- `03 测试计划`：现在面向 `MiniShop Checkout`
- `04 详细测试设计与执行`：聚焦 `MiniShop Checkout` 中的 `coupon_discount_engine`

结论：

- **对象口径现在是正确的**

---

## 3. 按功能需求 FR 逐条核对

| 要求 | 当前状态 | 结论 |
| --- | --- | --- |
| `FR 1.0` 输入/解析 | 支持 plain text、direct input、CSV batch、state-model path，以及 Web demo 入口 | 已完成 |
| `FR 1.1` 需求结构化 | 强制五段结构 trace，解析为 `ParsedTrace` 和结构化 `TestCase` | 已完成 |
| `FR 2.0` 风险分析与优先级 | 有 risk score、priority band、case priority promotion | 已完成 |
| `FR 3.0` 黑盒测试设计 | 支持 `EP / BVA / Decision Table`，并在 pipeline / repair 中闭环 | 已完成 |
| `FR 4.0` 白盒测试建模 | 当前以 state-model / legal-illegal transitions / coverage plans 的形式闭合行为建模要求 | 已完成 |
| `FR 5.0` 测试预言生成 | `Expected Output` 是一等字段，生成、解析、修补、导出全链路保留 | 基本完成 |
| `FR 6.0` 输出与导出 | 导出 `JSON / CSV / Markdown`，并保留 checker log、state model、summary report | 已完成 |
| `FR 7.0` 测试套件优化 | 有 rerank、duplicate penalty、technique bonus、repair 与 priority-aware selection | 已完成 |

补充说明：

- `FR 4.0` 在老师原文里虽然写成 white-box modeling，但括号例子给的是 state-transition graph；你们现在的实现是沿这条路闭合的。
- `FR 5.0` 更像“与 requirement 对齐的 expected-result synthesis”，不是独立复杂 oracle engine，但对课程要求已经够用。
- `FR 7.0` 不是形式化最优化算法，但对“prioritize / minimize based on risk or coverage efficiency”的课程要求来说，当前实现已经是实质闭合。

---

## 4. 老师特别强调的 interactive review 是否满足

老师要求的关键点是：

- 设计者要能交互式修改 coverage items、strategy、test cases

当前实现已经具备三层闭环：

1. **生成前**
   - 在 `Direct Input` 页指定 technique emphasis
   - 输入 coverage items to review
   - 输入 designer review notes

2. **生成后**
   - 在同一页面直接编辑生成出的 test cases
   - 支持新增 case
   - 支持删除 / 修改 case 字段

3. **修订后**
   - 点击 `Export Revised Suite`
   - 后端重新计算 checker / coverage 诊断
   - 导出新的 reviewed suite artifacts

这条能力的实现证据在：

- `demo_web/static/index.html`
- `demo_web/static/app.js`
- `demo_web/app.py`
- `tests/test_demo_web_api.py`

结论：

- **interactive review 现在可以判为已满足，不再只是“部分符合”**

---

## 5. 按非功能需求 NFR 核对

### 5.1 Performance

最新本地/mock NFR 结果：

- `100 requirements` 总处理时间：`0.3646 s`
- 平均每条 requirement：`0.0036 s`
- 单条 requirement 最大值：`0.0056 s`

结论：

- **本地/mock 路径显著满足老师给出的课程级性能门槛**
- **live provider 延迟仍应继续作为外部变量诚实说明**

### 5.2 Usability / UX / UI

当前可用路径包括：

- CLI
- Direct Input
- CSV Batch
- State Model
- Formal Evidence
- 生成后 test-case editor

结论：

- **课程项目级可用性已经足够**
- **重点不再是“有没有界面”，而是“界面是否能完成交互式审查任务”，这一点现在已闭合**

### 5.3 Security

当前证据显示：

- API key 通过 `.env` / environment variable 注入
- artifact manifest 不写入密钥
- 生成物扫描未发现 obvious secret leak

结论：

- **课程级安全要求满足**

### 5.4 Maintainability

当前仓库证据：

- `src/` Python modules：`27`
- experiment scripts：`19`
- test files：`8`
- automated test cases：`45`
- latest pytest summary：`45 passed, 1 warning in 1.41s`

结论：

- **可维护性证据明显强于课程最低要求**

---

## 6. 三份正式文档是否理解正确

### 6.1 风险分析报告

现在的风险分析报告已经在写：

- `MiniShop Checkout` 的业务与质量风险
- 促销、支付、税费、运费、校验、编排等优先级

结论：

- **当前理解正确**

### 6.2 测试计划

现在的测试计划已经覆盖：

- scope
- test items
- application architecture
- suite design
- schedule / checklist
- team responsibilities
- testing framework and rationale
- cost estimation

并且这些内容现在都围绕 `MiniShop Checkout`，不再把 `ARG-Test` 当成 system under test。

结论：

- **当前理解正确**

### 6.3 详细测试设计与执行文档

`04` 现在的定位是：

- 针对 `MiniShop Checkout` 中 selected major module 的 detailed design and execution

结论：

- **当前理解正确，而且是三份文档里最强的一份**

---

## 7. 交付物层面是否齐全

### 已具备

- 工具代码与提示词：有
- 三份正式文档 Markdown：有
- 三份正式文档 PDF：有
- 最终 PPT PDF：本地已有 `07_PPT_Assets_For_Luowu/final_ppt.pdf`

### 当前仍需确认 / 补齐

- **demo video**：当前仓库里仍未看到实际视频文件
- **完整工具提交压缩包**：当前明确可见的是 `submission_artifacts/arg_test_final_test_scripts.zip`，更像测试脚本包；建议再整理一个完整工具材料压缩包

结论：

- **提交物主体已齐，但最后两项仍需明确收口**

---

## 8. 严格结论

如果现在按老师要求逐条验收：

- **项目实现层面：基本合格**
- **三份正式文档对象理解：合格**
- **interactive review 要求：合格**
- **FR / NFR 主体能力：合格**
- **详细执行证据：很强**

真正还不能完全打勾的，只剩：

1. `demo video` 是否实际录好并提交
2. 完整工具提交压缩包是否按最终提交格式整理好

所以当前最准确的一句话是：

> 这个项目现在已经不是“要求理解错了”的状态，而是“实现和文档已经基本贴要求，只剩最后提交包装要收口”的状态。  
