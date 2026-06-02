# Final Demo 补录说明（仅补新功能）

这份文件用于说明：  
**如果旧版 demo 视频已经录好，不需要整段重录，只需要额外补录一小段新功能视频，再和旧视频剪在一起即可。**

本次需要补录的新功能是：

- **生成后可交互修改测试用例，并重新导出 revised suite**

也就是老师要求里非常关键的这一点：

- tester 不仅能看结果
- 还能修改 coverage / strategy guidance
- 并且在生成后**直接编辑测试用例本身**

这正是我们后来补上的功能闭环。

---

## 1. 这段补录的目的

旧视频如果只展示了：

- Direct Input 生成
- CSV Batch
- State Model
- Formal Evidence

那么它还缺一个最关键的证明：

- **设计者可以在生成后直接修改 test cases**

所以这段补录的作用非常明确：

> 用最短的一段画面，证明我们的工具已经支持“生成后人工编辑测试用例并重新导出”的交互式审查能力。

---

## 2. 最推荐的剪辑插入位置

把这段补录插在旧视频的：

- `Direct Input` 结果刚生成出来之后
- `切去 CSV Batch` 之前

也就是说，最自然的顺序应该变成：

1. 打开 `Direct Input`
2. 选择 requirement
3. 点击 `Generate Test Suite`
4. 展示右侧结果
5. **插入这段补录：编辑 test cases 并导出 revised suite**
6. 再继续原视频里的 `CSV Batch`
7. 后面照旧

这样剪进去最自然，因为逻辑上它本来就属于 Direct Input 的后半段。

---

## 3. 建议补录时长

建议长度：

- `30` 到 `60` 秒

不建议太长。  
这段的目标不是重新解释整个系统，而是**明确补一个合规性闭环证据**。

---

## 4. 补录前准备

保持和旧视频一致：

- 继续使用 `mock` provider
- 继续用当前 Web demo
- 最稳妥的 requirement 仍然建议选：
  - `pickup_station_contact_validation`

启动方式不变：

```powershell
python -m uvicorn demo_web.app:app --host 127.0.0.1 --port 8000
```

浏览器打开：

```text
http://127.0.0.1:8000/
```

---

## 5. 补录时具体操作

建议按下面这套动作录：

1. 进入 `Direct Input`
2. 选择 `pickup_station_contact_validation`
3. 点击 `Generate Test Suite`
4. 等右侧结果出来
5. 向下滚动到生成后的 **test-case editor**
6. 修改一条已有 case  
   例如改：
   - `Expected Output`
   - 或 `Priority`
7. 点击 `Add Test Case`
8. 新增一条简单负例 case
   - 比如：`contactless pickup = true` 且 `pickup_code missing`
9. 在 `Revision Notes` 里写一句：
   - `Added an explicit invalid case after designer review.`
10. 点击 `Export Revised Suite`
11. 停留一两秒，让画面显示：
   - `Manual case revision saved`
   - 或 revised artifact path

---

## 6. 最推荐的英文口播

你们补录时可以直接说这几句，尽量简短：

```text
After generation, the tester is not limited to inspection only.

Here we can directly revise an existing test case,
add a new negative case,
and export a reviewed suite.

This closes the designer-in-the-loop requirement,
because coverage focus, strategy guidance,
and test cases themselves can all be modified interactively.
```

如果想更短一点，也可以只说：

```text
After generation, the tester can directly edit individual test cases
and export a revised suite.

This is our final interactive review closure.
```

---

## 7. 中文理解

这段英文口播的意思就是：

- 生成之后，tester 不只是看结果
- 还可以直接改已有 case
- 也可以新增一个负例 case
- 最后重新导出 reviewed suite

这样就能证明：

- coverage focus 可以交互调整
- strategy guidance 可以交互调整
- test cases 本身也能交互修改

这正好对应老师要求里的那句：

- **工具必须支持对覆盖项、策略和测试用例的交互式修改**

---

## 8. 录制时不要说错的话

这段补录里不要说：

- `the model automatically becomes correct after editing`
- `this proves full semantic correctness`
- `live provider is deterministic`

最稳的说法始终是：

- this supports interactive review
- this supports human revision
- this improves traceability and controllability

不要把“可编辑”说成“自动保证正确”。

---

## 9. 剪辑时的建议

剪辑时最稳的做法：

- 旧视频里 `Direct Input` 结果出现后
- 直接接入这段补录
- 补录结束后再接回原来切去 `CSV Batch` 的地方

如果担心观感不连贯，可以在补录片段开头加一个很短的字幕：

```text
Supplemental interactive review step
```

或者：

```text
Post-generation case editing
```

这样老师会立刻明白，这是一段补充展示，而不是剪辑错误。

---

## 10. 补录完成后的检查清单

补录完成后，请确认这几件事都出现了：

- 生成后的 case editor 真的出现在画面里
- 至少修改了一条现有 case
- 至少新增了一条 case
- 点击了 `Export Revised Suite`
- 屏幕上出现了 revised 保存成功的反馈
- 口播里明确说了：
  - `edit individual test cases`
  - `export a revised suite`
  - `interactive review`

如果这 `6` 点都满足，这段补录就足够了，不需要重录整支视频。

---

## 11. 一句话结论

你们现在最应该补录的，不是重新讲系统，而是用 `30-60` 秒明确展示这一点：

> **After generation, the tester can directly edit test cases and export a revised suite.**

这就是这次补录最核心的任务。
