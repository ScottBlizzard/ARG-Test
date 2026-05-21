# Final Demo Script (Chinese)

## 建议总时长

推荐总时长：`4` 到 `5` 分钟

## 0:00 - 0:20 开场

大家好，这里演示的是我们 final project 的工具本身，而不是完整 PPT。

这次演示里，现场运行部分我们使用 `mock` 模式来保证稳定和可重复；项目最终质量则通过已经冻结的正式结果和可执行证据来展示。

## 0:20 - 1:10 现场运行命令

首先，我们演示 direct text input。工具可以直接从文本输入 requirement，并自动生成结构化测试结果，同时给出 risk 和 state-model 信息。

第二，我们演示 CSV batch input。这样可以说明系统不仅能处理单条 requirement，也能批量导入并分别导出结果。

第三，我们演示 state-model extraction。这个功能对应 final project 里比较重要的一项能力，也就是从 requirement 中提取状态、转移和 coverage plan。

这里的重点不是 benchmark 数字，而是证明工具真的能运行，输入方式不是单一的，而且输出不是随便一段文本。

## 1:10 - 1:50 看 direct-text 输出

现在我们打开 direct-text 的 summary。

这里可以看到，输出不仅有 test cases，还有 candidate control、checker score、risk assessment，以及 state model 和对应的 coverage plan。

这说明我们的系统不是 one-shot prompting，而是一个可审计的 testing pipeline。

## 1:50 - 2:20 看 CSV 输出

接下来打开 CSV run 里的一条结果。

这里主要想说明两点。第一，CSV batch input 是支持的。第二，输出会自动导成 Markdown、JSON 和 CSV，方便报告、检查和后续使用。

## 2:20 - 2:50 看 workflow state-model 输出

现在打开 workflow requirement 的 state-model 文件。

这里可以看到状态集合、合法转移、非法转移，以及 All States 和 All Transitions 的覆盖计划。这个部分说明我们不仅在做普通黑盒测试枚举，还进一步做了行为建模。

## 2:50 - 3:20 切到正式实验结果

刚才的 live mock run 展示的是工具接口和功能链。接下来展示 final 项目的正式结果。

在 held-out test split 上，ARG-Test 的 average checker score 是 `0.959`，average overall coverage 是 `0.615`，并且明显优于 `rule-based`、`plain LLM` 和 `structured-no-checker` baseline。

这部分说明我们的项目不仅能跑，而且效果是成立的。

## 3:20 - 3:45 讲 reproducibility

接着看 reproducibility。

这里我们明确区分两层：一层是 pipeline-level reproducibility，另一层是 provider-level nondeterminism。我们的本地链路是可控的，而最终 submission-level reproducibility 通过 frozen generations 加 replay 来保证。

所以我们不会过度宣称 live provider 是完全 deterministic 的，但我们能保证最终提交包是可重现的。

## 3:45 - 4:15 讲 executable evidence

最后展示详细模块证据，也就是 `coupon_discount_engine`。

这里我们有 `15` 个 module-focused tests，`100%` statement coverage，`100%` branch coverage，以及 `4/4 mutants killed`。

这说明我们的 final project 不只是 requirement-level 设计，还有真正的 executable evidence。

## 4:15 - 4:30 结束

总结一下，这个 demo 说明了三件事：

第一，工具真的能运行，而且支持多种输入方式。  
第二，输出是结构化、可审计的，而不是简单 prompt 文本。  
第三，final project 还进一步有正式结果、复现性说明和可执行证据支撑。
