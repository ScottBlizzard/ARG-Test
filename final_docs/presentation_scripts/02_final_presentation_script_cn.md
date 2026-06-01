# 最终答辩讲稿（中文对照）

这份文件是对英文讲稿的中文翻译，对应：

- `final_docs/presentation_scripts/01_final_presentation_script_en.md`

建议总时长：

- 约 `15` 分钟
- `5` 个人
- 每人约 `3` 分钟

建议分工：

- 第 1 人：Slides `1` 到 `4`
- 第 2 人：Slides `5` 到 `7`
- 第 3 人：Slides `8` 到 `10`
- 第 4 人：Slides `11` 到 `16`
- 第 5 人：Slides `17` 到 `20`

---

## 第 1 人

**Slides 1 到 4**

**建议时长：**约 `3` 分钟

大家好，我们是 Group 7。我们的项目叫做 ARG-Test，它是一个可审计、具备风险感知能力、面向自然语言需求的黑盒测试生成流水线。

我们的出发点来自期末项目本身。老师要求的并不只是一个 prompt，也不只是一个 benchmark。老师要求我们开发一个 AI 驱动的 AutoTestDesign 工具，然后再用这个工具去测试一个独立的目标应用。

所以在最终版本里，我们清楚地区分了三件事。第一，ARG-Test 是工具。第二，MiniShop Checkout 是独立的被测应用。第三，coupon_discount_engine 是 MiniShop Checkout 里的选定主模块，我们用它来做详细测试设计与执行。

这个区分很重要，因为它修正了我们前期理解里最大的一个问题。我们现在不是把自己的工具当成被测应用，而是用这个工具去测试一个具体的结算应用。

MiniShop Checkout 是一个为这次期末项目专门构建的小型电商结算原型。它的实际实现范围包括：优惠券与促销处理、运费计算、税费与订单总额计算、支付卡校验、自提联系人校验，以及结算预览编排。与此同时，我们也明确把退款流程、库存同步和外部支付网关集成排除在范围之外。这样这个应用既足够小，又足够具体，能够算作一个真实的被测对象。

在明确了应用边界之后，接下来的问题就是：为什么不能只靠 plain LLM？简短的答案是，流畅的输出不等于可审计的测试。一个普通 LLM 可能会给出几个看起来合理的测试建议，比如试一个有效优惠券，或者试一个过期优惠券，但它经常不会清楚告诉我们：重要的非法分区有没有覆盖，边界邻近值有没有覆盖，或者它声称使用的测试技术是否真的对应了需求里的覆盖义务。

所以更深层的问题不只是对不对，而是能不能审。我们想要的系统，不只是从 requirement 到一堆测试，而是能解释自己是怎么从自然语言需求一步步走到结构化、可审查测试套件的。

这也就是后面整场答辩的主线：我们要展示的是，如何把 plain answer 变成 structured、checked、traceable 的测试设计。

---

## 第 2 人

**Slides 5 到 7**

**建议时长：**约 `3` 分钟

接下来我介绍 ARG-Test 作为一个系统是怎么工作的。

最核心的一点是，ARG-Test 不是一个单独的 prompt，而是一条流水线。我们不是直接让模型吐出最终测试列表，而是把流程组织成几个阶段：结构化生成、解析与 schema gate、技术感知的 checker、rerank 与 targeted repair，最后再做导出、评估和可复现报告。

结构化 trace 是系统里最重要的部分之一。我们要求模型输出五段结构：Analysis、Pattern、Steps、Verification 和 FinalAnswer。这件事很重要，因为它把模型输出变成了一个可以被解析和检查的对象，而不只是一个“看起来很像答案”的自由文本。

在这个基础上，我们还做了 technique-aware contract checking。系统里包括 equivalence partition checker、boundary value checker、decision checker 和 state checker。这些 checker 不会神奇地证明语义绝对正确，但它们会验证：生成出来的 trace 和 test suite，是否真的包含了对应测试技术应该覆盖的 obligation。

所以模型输出不会再被直接当成最终真相。它变成了一个 typed artifact，可以被解析、检查、比较、rerank，如果需要的话还可以修补。

下一页讲的是这些能力如何对应到老师的课程要求。在 mandatory closure 方面，我们完成了 FR 1.0、FR 1.1、FR 2.0、FR 3.0 和 FR 6.0。同时，我们还完成了额外加分项 FR 4.0、FR 5.0 和 FR 7.0。

另一个老师特别强调的点是 interactive review。我们的最终系统提供了四个实际可展示的 review surface：Direct Input、CSV Batch、State Model 和 Formal Evidence。

更重要的是，tester 不是被动看结果的人。tester 可以检查输出，可以修改输入或 review guidance，可以重跑 pipeline，而且在最终版本里，还可以直接编辑生成后的测试用例，再导出 revised suite。这样 designer participation 就不再只是文档里说说，而是真正体现在系统能力里。

所以这一部分最重要的结论是：ARG-Test 做的不只是生成，而是生成加结构、加检查、加审查、加受控修订。

---

## 第 3 人

**Slides 8 到 10**

**建议时长：**约 `3` 分钟

接下来我介绍面向被测应用的 planning 文档，也就是风险分析和测试计划。

因为我们的目标应用是 MiniShop Checkout，所以风险分析也必须针对 MiniShop Checkout。我们用一个简单但明确的公式来做评分：Risk Priority 等于 Impact 乘以 Likelihood 再乘以 Detectability，然后把结果划分成高、中、低三个优先级区间。

通过这个分析，我们得到 MiniShop Checkout 里风险最高的几个区域：优惠券与促销逻辑、运费与税费计算、支付卡校验，以及 checkout orchestration。Pickup validation 也很重要，但和价格、总额以及支付接受路径相比，它的整体影响范围相对更窄一些。

这个优先级分析直接决定了测试计划怎么写。测试计划的 scope 包括 promotion and pricing、shipping and tax、payment validation、pickup validation，以及 checkout orchestration。从架构上看，这个应用围绕一个 Checkout Service 组织起来，由它协调 Promotion、Shipping、Tax、Payment Validation 和 Pickup Validation 这些模块。

在这个架构上，我们设计了几套 planned suites：promotion suite、shipping and tax suite、payment validation suite、pickup validation suite、checkout orchestration suite，以及最后的 detailed executable module suite，也就是针对 coupon_discount_engine 的那套详细执行证据。

接下来是执行组织。我们的 schedule 很直接：先冻结 target-application scope，然后完成 risk analysis，再 review generated suites，然后执行 detailed module tests，最后再打包 evidence 和最终交付物。

在执行框架上，我们选择了 pytest 加 coverage.py。原因也很简单。MiniShop Checkout 是 Python 实现的，pytest 非常适合写 black-box 和 white-box assertion，同时又能很自然地和 coverage 集成，而这对 selected detailed module 尤其重要。

最后，老师要求 test plan 里还要有 cost estimation，所以我们也做了这一块。我们的估算是：如果用 ARG-Test 去测试这个目标应用，大约需要四点五到七个 person-days；如果完全不用这个工具，而是纯手工做同样范围的 requirement decomposition、suite selection、traceability 和整理，成本大约会上升到七点五到十个 person-days。也就是说，工具的价值不是取消人工 review，而是降低 requirement analysis、第一轮 suite generation、prioritization 和 traceability maintenance 的成本。

所以这一部分的关键结论是：风险报告和测试计划现在都已经统一成“如何测试目标应用”，而不是“如何描述我们的工具”。

---

## 第 4 人

**Slides 11 到 16**

**建议时长：**约 `3` 分钟

下面我来介绍实验设置和主要工具级结果。

我们的评估使用一个冻结的 test split，一共有十六条 requirement。之所以把 test set 冻结下来，是为了让最终对比稳定、可 defend。我们把 ARG-Test 和三个 baseline 做比较：rule-based baseline、plain LLM baseline 和 structured-no-checker baseline。

主结果页面显示，在这十六条冻结的测试 requirement 上，ARG-Test 的平均 checker score 是 0.959，平均 overall coverage 是 0.615，而且 duplicate cases 为零。

这意味着什么？意味着完整 pipeline 明显强于三个更弱的对照方法。和 rule-based 相比，提升说明它在 requirement understanding 上更强。和 plain LLM 相比，提升说明单纯 prompting 不够。和 structured no-checker 相比，提升说明 checker-guided control 是真的有价值的，而不是只是让输出看起来更规整。

我们还看了 generalization 和 ablation。这个方法不仅能处理 business-rule requirements，也能处理 input-validation requirements 和 workflow-state requirements。而在 ablation 里，最诚实的说法是：checker-guided control 显著提升了 checker alignment，同时让 coverage 保持在可比范围内。换句话说，checker 这一层不是装饰，它确实改变了最终选出的 suite 质量。

Representative cases 这一页则给出三个具体例子，分别展示 business-rule logic、input validation 和 workflow-oriented cases。它的作用是让老师看到：你们的方法不是只对某一种 requirement 有效。

所以这一部分最重要的结论有两个。第一，ARG-Test 在一个有意义的 requirement 范围上是能工作的。第二，structured and checked pipeline 在冻结评估设置下，确实比几个更弱的 baseline 更强。

这也就把讲述自然过渡到了最后一部分：从 design-level evidence 走向 executable evidence。

---

## 第 5 人

**Slides 17 到 20**

**建议时长：**约 `3` 分钟

最后我来讲最强的执行证据，以及整个项目的边界。

在 MiniShop Checkout 里，我们选定 coupon_discount_engine 作为主要模块来做 detailed test design and execution。之所以选它，是因为它属于高风险的 financial-rule component，里面有边界值、非法情况、规则组合和清晰的 expected result，所以非常适合用来证明 requirement-driven design 可以真正落到可执行测试上。

这让我们拥有的不只是设计级指标，而是真正的 executable evidence。在最终版本里，这个 selected module 由 black-box tests、white-box tests、full statement coverage、full branch coverage，以及 mutation-based usefulness evidence 支撑。同时，在 repository level 上，我们当前的 regression suite 也保持通过。

我们还特别重视 reproducibility 和 practical validation。在 seeded mock control 下，repository-level chain 是 deterministic 的。对于 live provider，我们保持诚实：它仍然有 variance。所以我们的 submission-level reproducibility 不依赖于夸大 live determinism，而是依赖 frozen generations 加 replay。这样我们在 demo 和 report 里展示的 formal examples 都可以被重建出来。

Limitations 这一页同样重要。我们明确承认：我们做的是 requirement-driven branch；我们的评估是 course-scale，不是大型 public benchmark；coverage 仍然依赖人工编写的 gold specs；live providers 也仍然存在 residual nondeterminism。我们没有把这些当成需要隐藏的缺点，而是当成项目边界诚实地说出来。

所以最后的结论是：structured reasoning 让 black-box test design 变得可审计；完整的 ARG-Test pipeline 打败了非 AI 和较弱 AI 的 baseline；而最终提交物也不只是一个 prompt demo，它包含了工具本身、面向目标应用的 risk report、target-application test plan、针对选定模块的 detailed execution document，以及一套可复现的 final artifacts。

谢谢大家，我们准备回答问题。

---

## 简短分工说明

### 建议讲述顺序

1. 第 1 人：标题、对象分离、目标应用、问题动机
2. 第 2 人：架构、structured trace、checker、interactive review
3. 第 3 人：风险报告和测试计划
4. 第 4 人：实验与 benchmark 结果
5. 第 5 人：可执行证据、可复现性、限制与总结

### 排练建议

- 人与人之间的衔接尽量短一点。
- 不要逐字重念 slide 上所有 bullet。
- 让 slide 负责视觉，讲稿负责讲故事。
- 如果时间不够，可以优先压缩第 4 人，尤其是 Slides `11` 和 `12`。 
