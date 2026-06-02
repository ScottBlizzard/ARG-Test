# 最终答辩讲稿（中文对照）

这份文件是对应英文讲稿的中文翻译，对应：

- `final_docs/presentation_scripts/01_final_presentation_script_en.md`

建议总时长：

- 约 `15` 分钟
- `5` 个人
- 建议时长分配：
  - 第 `1` 人：`2.5` 分钟
  - 第 `2` 人：`2.5` 分钟
  - 第 `3` 人：`3.5` 分钟
  - 第 `4` 人：`3.5` 分钟
  - 第 `5` 人：`3.0` 分钟

建议分工：

- 第 `1` 人：Slides `1` 到 `4`
- 第 `2` 人：Slides `5` 到 `7`
- 第 `3` 人：Slides `8` 到 `10`
- 第 `4` 人：Slides `11` 到 `16`
- 第 `5` 人：Slides `17` 到 `20`

---

## 第 1 人

**Slides 1 到 4**

**建议时长：**约 `2.5` 分钟

大家好，我们是 Group 7。我们的项目叫做 ARG-Test，它是一个可审计、具备风险感知能力、面向自然语言需求的黑盒测试生成流水线。

我们的项目包含三个清晰分离的部分。第一，ARG-Test 是我们开发的 AutoTestDesign 工具。第二，MiniShop Checkout 是独立的被测目标应用。第三，coupon_discount_engine 是 MiniShop Checkout 内部选定的主模块，我们用它来完成详细测试设计与执行。

MiniShop Checkout 是一个源自之前小型课程项目的电商结算原型，并在本次期末项目中被选作独立的被测目标应用。它的范围包括优惠券与促销处理、运费计算、税费与订单总额计算、支付卡校验、自提联系人校验，以及结算预览编排。同时，我们明确把退款流程、库存同步和外部支付网关集成排除在范围之外，这样可以让这个应用既足够小，又足够具体，能够成为一个真实可测的目标对象。

ARG-Test 的动机来自一个很直接的观察。普通的 LLM 可以生成流畅的测试建议，但流畅的输出并不等于可审计的测试设计。如果模型只是说“试一个有效优惠券”或者“试一个过期优惠券”，我们仍然不知道非法分区是否被覆盖、边界邻域是否被覆盖，或者它声称使用的测试技术是否真正反映在最终测试套件里。

所以更深层的问题不只是“对不对”，而是“能不能解释、能不能审查、能不能追溯”。我们希望得到的系统，不只是从一段需求生成几条测试，而是能够说明自己如何从自然语言需求一步步走到结构化、可审查、可导出的测试套件。

这也是后面整场展示的主线。我们要说明的是，ARG-Test 如何把普通生成过程变成结构化、可检查、可追踪的测试设计过程，并把这个工具应用到一个具体的被测应用上。

所以这个项目讲的不只是“能不能生成测试”，而是“能不能把整个测试设计过程变得更可用、更可审查”。

---

## 第 2 人

**Slides 5 到 7**

**建议时长：**约 `2.5` 分钟

接下来我介绍 ARG-Test 作为一个系统是如何工作的。

最核心的一点是，ARG-Test 不是单个 prompt，而是一条完整流水线。我们不是直接让模型输出最终测试列表，而是把流程组织成几个阶段：结构化生成、解析与 schema gate、面向测试技术的 checker、rerank 和定向 repair，最后再做导出、评估和可复现报告。

结构化 trace 是系统里最重要的部分之一。我们要求模型输出五段结构：Analysis、Pattern、Steps、Verification 和 FinalAnswer。这样做很重要，因为它把模型输出变成一个可以被解析和检查的对象，而不是只是“看起来像答案”的自然语言文本。

在这之上，我们还做了 technique-aware contract checking。系统里包括 equivalence partition checker、boundary value checker、decision checker 和 state checker。这些 checker 并不是在证明绝对语义正确，但它们会验证：生成出的 trace 和最终 suite 是否真正包含了所选测试技术应当覆盖的 obligation。

因此，模型输出不会被直接当成最终真相。它会变成一个 typed artifact，可以被解析、检查、比较、重排序，并在必要时被修补。

下一页说明这些能力如何对应课程要求。在 mandatory closure 方面，我们完成了 FR 1.0、FR 1.1、FR 2.0、FR 3.0 和 FR 6.0。同时，我们也实现了额外加分项 FR 4.0、FR 5.0 和 FR 7.0。

另一个作业里非常重要的点是 interactive review。我们的系统提供了四个实际可展示的 review surface：Direct Input、CSV Batch、State Model 和 Formal Evidence。

这也意味着 tester 不只有一种固定使用方式，而是可以根据单条需求、批量输入、工作流查看和证据展示这些不同场景来使用系统。

更重要的是，tester 不是被动的。tester 可以检查输出、修改 review guidance、重新运行 pipeline，甚至在生成之后直接编辑测试用例，并导出 revised suite。这样一来，设计者参与就不只是理论上的一句话，而是真正体现在最终工具能力里。

所以这一部分最重要的结论是：ARG-Test 做的不只是生成，而是生成加结构、加检查、加审查、加受控修订。

正是这种组合，让它更接近一个真正可用的 AutoTestDesign 工作流。

---

## 第 3 人

**Slides 8 到 10**

**建议时长：**约 `3.5` 分钟

接下来我介绍面向被测应用的 planning 文档，也就是风险分析和测试计划。

因为我们的目标应用是 MiniShop Checkout，所以风险分析也围绕 MiniShop Checkout 展开。我们使用一个简单但明确的公式来评分：Risk Priority 等于 Impact 乘以 Likelihood 再乘以 Detectability，然后把结果划分为高、中、低三个优先级区间。

这些最终文档建立在 ARG-Test 生成的结构化证据之上，包括 requirement trace、测试技术选择、风险评分、recommended focus、checker diagnostics，以及导出的测试套件。

通过这个分析，我们得到 MiniShop Checkout 里风险最高的几个区域，分别是优惠券与促销逻辑、运费与税费计算、支付卡校验，以及 checkout orchestration。Pickup validation 也很重要，但整体影响范围相对更窄一些。

这个优先级分析直接决定了测试计划的内容。测试计划的 scope 包括 promotion and pricing、shipping and tax、payment validation、pickup validation，以及 checkout orchestration。从架构角度看，这个应用围绕一个 Checkout Service 组织起来，由它协调 Promotion、Shipping、Tax、Payment Validation 和 Pickup Validation。

基于这个架构，我们设计了 promotion suite、shipping and tax suite、payment validation suite、pickup validation suite、checkout orchestration suite，以及最后针对 coupon_discount_engine 的 detailed executable module suite。

在执行组织上，我们的 schedule 很直接：先冻结 target-application scope，然后完成 risk analysis，再 review generated suites，然后执行 detailed module tests，最后打包 evidence 和最终交付物。在执行框架上，我们选择 pytest 和 coverage.py，因为 MiniShop Checkout 是 Python 实现的，这个组合很适合 black-box 和 white-box 验证。

最后，测试计划里还包含了 cost estimation。我们的估算是：如果使用 ARG-Test 来测试这个目标应用，大约需要四点五到七个 person-days；如果完全手工完成同样范围的 requirement decomposition、suite generation、prioritization 和 traceability 整理，那么成本大约会上升到七点五到十个 person-days。也就是说，工具的价值不在于取代人工 review，而在于降低需求拆解、首轮测试套件生成、优先级整理和可追溯性维护的成本。

换句话说，这个计划不只是技术上可行，也是在团队投入和项目节奏上可落地的。

所以这一部分的关键结论是：风险报告和测试计划共同说明了我们如何系统地测试这个目标应用，也说明了这套计划是建立在结构化证据之上的。

它们让整个项目从风险识别到测试套件执行之间，形成了一条很清楚的应用侧逻辑。

---

## 第 4 人

**Slides 11 到 16**

**建议时长：**约 `3.5` 分钟

下面我来介绍实验设置和主要的工具级结果。

我们的评估使用一个冻结的 test split，一共包含十六条 requirement。冻结 test set 的目的，是让最终比较稳定且可辩护。我们把 ARG-Test 和三个 baseline 进行比较：rule-based baseline、plain LLM baseline 和 structured-no-checker baseline。

主结果页显示，在这十六条冻结 requirement 上，ARG-Test 的平均 checker score 是 0.959，平均 overall coverage 是 0.615，并且 duplicate cases 为零。

这说明完整 pipeline 明显强于三个更弱的对照方法。和 rule-based 相比，它体现了更强的 requirement understanding。和 plain LLM 相比，它说明单纯 prompting 不够。和 structured no-checker 相比，它说明 checker-guided control 有真实价值，而不只是让输出看起来更整齐。

我们还分析了 generalization 和 ablation。这个方法不仅能处理 business-rule requirements，也能处理 input-validation requirements 和 workflow-state requirements。而在 ablation 视角下，最诚实的表述是：checker-guided control 显著提升了 checker alignment，同时让 coverage 保持在可比范围内。换句话说，checker 这一层不是装饰，它确实改变了最终被选中 suite 的质量。

Representative cases 这一页又给出了三个具体例子，分别对应 business-rule logic、input validation 和 payment validation。这说明我们的系统并不是只对一种狭窄的 requirement 有效。

所以这一部分最重要的结论有两个。第一，ARG-Test 能在一个有意义的 requirement 范围上稳定工作。第二，structured and checked pipeline 在冻结评估设定下，确实优于几个更弱的 baseline。

所以这些实验结果的价值，不只是数字本身，而是它们支撑了整个工具设计的合理性。

这也自然过渡到最后一部分，也就是从 design-level evidence 走向 executable evidence。

---

## 第 5 人

**Slides 17 到 20**

**建议时长：**约 `3.0` 分钟

最后我来讲最强的执行证据，以及整个项目的边界。

在 MiniShop Checkout 里，我们选择 coupon_discount_engine 作为主模块来做 detailed test design and execution。之所以选择它，是因为它属于高风险的 financial-rule component，里面包含阈值、非法情况、规则组合和清晰的 expected result，因此很适合用来证明 requirement-driven design 能够真正落到可执行测试上。

这让我们拥有的不只是设计层面的指标，而是真正的 executable evidence。在最终版本里，这个 selected module 由 black-box tests、white-box tests、full statement coverage、full branch coverage，以及 mutation-based usefulness evidence 支撑。同时，在 repository level 上，我们当前的 regression suite 也保持稳定通过。

我们也非常重视 reproducibility 和 practical validation。在 seeded mock control 下，repository-level chain 是 deterministic 的。对于 live provider，我们保持诚实：它仍然存在 variance。所以我们的 submission-level reproducibility 不依赖于夸大 live determinism，而是依赖 frozen generations 加 replay。这样我们在 demo 和 report 里展示的 formal examples 都可以被重新构建出来。

Limitations 这一页同样重要。我们明确说明：我们做的是 requirement-driven branch；我们的评估是 course-scale，而不是大型 public benchmark；coverage 仍然依赖人工编写的 gold specifications；live providers 也仍然存在 residual nondeterminism。我们把这些视为清晰的项目边界。

把这些边界讲清楚，反而会让我们的最终结论更可信，因为我们同时说明了项目的能力和限制。

所以最后的总结是：structured reasoning 让 black-box test design 变得可审计；完整的 ARG-Test pipeline 优于非 AI 和较弱 AI 的 baseline；而最终提交物也不只是一个 prompt demo，它包括工具本身、系统导出的结构化证据、建立在这些证据之上的目标应用风险分析报告和测试计划、针对选定模块的详细执行文档，以及可复现的最终工件。

谢谢大家，我们准备回答问题。

---

## 简短分工说明

### 建议讲述顺序

1. 第 1 人：标题、目标应用、项目动机
2. 第 2 人：架构、structured trace、checker、interactive review
3. 第 3 人：风险报告和测试计划
4. 第 4 人：实验和 benchmark 结果
5. 第 5 人：可执行证据、可复现性、限制与总结

### 排练建议

- 人与人之间的衔接尽量短一点。
- 不要逐字重念 slide 上所有 bullet。
- 让 slide 负责视觉，讲稿负责讲故事。
- 这版时长已经重新分配，第 3 人和第 4 人会有更充足的空间。
