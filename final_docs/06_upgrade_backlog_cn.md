# Final Upgrade Backlog

本文件只保留“真正能显著提升 final 质量”的升级项，不列低价值装饰性工作。

## P0: 必做

### U1. 定稿 final 文档体系

- 完成风险分析
- 完成 test plan
- 完成 detailed test design and execution
- 完成 evidence checklist

完成标准：

- final_docs 中 4 类文档都有可扩写母版

### U2. 选定一个详细执行主模块

建议模块：

- `coupon_discount_engine`

完成标准：

- 在报告、PPT、demo、执行文档中使用同一个主模块

### U3. 建立正式结果引用口径

完成标准：

- 所有主结论能落到 `outputs/reports/` 或 `artifacts/` 的固定文件

## P1: 强烈建议

### U4. 为主模块补 reference implementation

建议新增：

- `reference_impl/` 或 `examples/` 下的可测模块

完成标准：

- 可以用 pytest 执行
- 可以测 statement/branch coverage

### U5. 加 white-box 执行证据

完成标准：

- 有测试脚本
- 有执行结果
- 有覆盖率摘要

### U6. 清理 final 示例中的占位输出

完成标准：

- final 展示案例中的 Input / Expected Output 不再是模板式占位语句

## P2: 若时间允许

### U7. 加 risk-aware prioritization

目标：

- 将风险评分或 priority 更系统地体现在最终 test suite 中

### U8. 改善 workflow/state 类表现

目标：

- 针对 workflow 类 requirement 优化 prompt、checker 或 repair

### U9. 加 defect-seeded usefulness demonstration

目标：

- 证明测试不只“看起来有覆盖”，而且对缺陷敏感

## 不建议投入过多时间的事项

- 新开完全独立仓库
- 做大量无执行价值的 UI 包装
- 再扩很多 requirement，但不提升 final 证据质量
- 生成很多图，但没有进入最终叙事

## 最终退出条件

只有满足下面 4 条，才算进入 final 可交状态：

1. 文档完整
2. 证据可追溯
3. 主模块执行闭环成立
4. 演示和答辩材料能支撑主要结论
