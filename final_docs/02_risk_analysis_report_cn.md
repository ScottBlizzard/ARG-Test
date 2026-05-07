# Risk Analysis Report Draft

## 目的

本报告面向 `ARG-Test` final release，识别影响最终交付质量的关键风险，并给出优先级与缓解动作。

## 风险评分口径

建议使用三维评分：

- Impact: 对 final 成绩、可信度、答辩表现的影响
- Likelihood: 在当前仓库状态下发生的可能性
- Detectability: 是否容易在提交前被发现

建议计算：

`Risk Priority = Impact x Likelihood x Detectability`

其中每项用 1 到 5 分。

## 高优先级风险

| Risk ID | Risk | Impact | Likelihood | Detectability | Priority | Mitigation |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | 生成结果中仍有占位式 expected output / input，导致 final 示例不够真实 | 5 | 4 | 3 | 60 | 对最终展示案例逐条人工校核，并优先修正主模块输出 |
| R2 | checker score 与 overall coverage 可能背离，导致报告结论被质疑 | 5 | 4 | 4 | 80 | 报告中并列展示两类指标，避免只讲单一得分 |
| R3 | workflow/state 类需求覆盖偏弱，影响 generalizability 说服力 | 4 | 4 | 3 | 48 | 将其作为局限明确写出，并补一个更强的 workflow case study |
| R4 | 缺 white-box 执行证据，Detailed Test Design 部分不够扎实 | 5 | 5 | 5 | 125 | 为主模块补 reference implementation、pytest、coverage |
| R5 | 文档引用了非正式或 mock 结果，导致 final 证据不可信 | 5 | 3 | 5 | 75 | 只引用 `official_result_sources_cn.md` 指定路径中的正式结果 |

## 中优先级风险

| Risk ID | Risk | Impact | Likelihood | Detectability | Priority | Mitigation |
| --- | --- | --- | --- | --- | --- | --- |
| R6 | 风险分析、测试计划、详细执行文档之间缺少一致叙事 | 4 | 3 | 3 | 36 | 用同一个主模块、同一组术语和同一套结果源 |
| R7 | 团队材料分散，答辩时找不到对应证据 | 4 | 3 | 4 | 48 | 建 final_docs 与 evidence source map |
| R8 | 成本估算和 schedule 写得过空，显得像模板作业 | 3 | 4 | 3 | 36 | 给出人天级拆分，而不是泛泛文字 |

## 低优先级风险

| Risk ID | Risk | Impact | Likelihood | Detectability | Priority | Mitigation |
| --- | --- | --- | --- | --- | --- | --- |
| R9 | README 与 final 目录结构不同步 | 2 | 3 | 5 | 30 | 持续同步仓库入口说明 |
| R10 | 冻结的中期材料与 final 工作区混用 | 3 | 2 | 4 | 24 | 只把 `frozen_middle/` 作为历史参考 |

## 风险响应策略

### 必须在 final 提交前解决

- R2 checker score 与 coverage 背离的解释问题
- R4 white-box 执行证据缺失
- R5 正式结果来源不清

### 可以作为局限保留，但必须写明

- workflow/state 类需求表现不稳定
- 轻量 checker 只能验证 contract consistency，不能证明完整语义正确

## final 报告中的呈现建议

建议把本风险报告拆成两层写进正式文档：

1. `Project/Test Plan` 中写总体测试与交付风险
2. `Limitations and Improvements` 中写方法本身的技术风险

## 当前结论

若只以当前仓库现状直接提交，最大风险不是“没有东西”，而是：

1. 证据还不够 final
2. 详细执行部分不够硬
3. 部分结果容易在答辩时被追问

因此 final 阶段的重点不是再扩很多功能，而是把高风险点补成可 defend 的证据链。
