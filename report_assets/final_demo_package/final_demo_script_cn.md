# Final Demo Script (Chinese)

建议总时长：`4` 到 `5` 分钟。下面是录屏时可以直接参考的口播稿。

## 0:00 - 0:20 开场

大家好，这里展示的是我们 final project 的工具本身。ARG-Test 的目标是把自然语言 requirement 转换成结构化、可审计的黑盒测试设计。

这次 demo 使用 `mock` 保证页面交互稳定；正式质量数字来自已经冻结的 formal result bundle，并通过页面 replay 展示。

## 0:20 - 1:10 Formal Evidence

先打开 `Formal Evidence` 页面。这里是最终答辩最安全的数字来源。

页面显示 held-out test split 一共有 `16` 个正式 test requirements，平均 structural checker 为 `0.959`，平均 overall coverage 为 `61.5%`，平均 test count 为 `7.312`。

下面还能看到 baseline comparison、category generalization 和 reproducibility snapshot。正式 PPT 或答辩中引用实验数字时，以这里和 frozen formal snapshot 为准。

## 1:10 - 2:00 Direct Input

接下来切到 `Direct Input`。从下拉框选择 `pickup_station_contact_validation`，点击 `Generate Test Suite`。

这里重点看四个信息：`Structural Checker`、`Overall Coverage`、`Run Mode` 和 `Result Source`。页面显示 `Replay`，并且标注 `Frozen formal replay`、`Matches Formal Evidence coverage`、`No live API call`。

这说明默认正式样例不是临时随机 mock 出来的，而是读取冻结正式输出；因此这里的 coverage 和 Formal Evidence Dashboard 是一致的。

## 2:00 - 2:40 CSV Batch

然后切到 `CSV Batch`，上传 sample CSV。这个入口证明系统不只支持单条 requirement，也支持批量导入。

匹配正式 requirement 的行会显示 `Frozen replay`。如果上传的是临时 ad hoc CSV，页面会走本地 mock 生成路径；那种结果只能用于展示功能，不能当作正式 benchmark。

## 2:40 - 3:25 State Model

接下来切到 `State Model`，选择 `warehouse_pickup_order_workflow`，点击 `Build State Model`。

页面会显示 states、legal transitions、illegal transitions 和 coverage plans。这个部分对应 final specification 里的 `FR 4.0`，说明我们不仅生成普通 test list，还能从 workflow requirement 中提取状态和迁移。

需要注意：如果某个 requirement 没有显式非法迁移规则，illegal transition 为 `0` 是合理的，不代表功能失败。

## 3:25 - 4:10 Executable Evidence

最后补充 detailed executable evidence。我们选取 `coupon_discount_engine` 作为详细执行模块，完成了 `15` 个 module-focused tests，达到 `100%` statement coverage、`100%` branch coverage，并且 `4 / 4` seeded mutants 被杀死。

这说明 final project 不只是生成测试文档，也有真实可执行的测试证据。

## 4:10 - 4:30 结束

总结一下，这个 demo 证明了三点：第一，工具可以稳定运行并支持 Direct、CSV、State Model 和 Formal Evidence；第二，输出是结构化、可审计的，不是单纯 prompt 文本；第三，最终结论由 frozen formal results、replay、regression tests 和 executable evidence 共同支撑。
