# Demo UI 前后端交接说明

这份说明是给负责 `demo` 的同学看的。  
目标不是让你从零设计系统，而是让你在现有稳定基线之上，把 UI 做得更清楚、更好看、更适合录视频。

## 1. 现在已经给你的基础

仓库里已经补好了一个最小可运行前后端：

- 后端：`demo_web/app.py`
- 前端：`demo_web/static/index.html`
- 样式：`demo_web/static/styles.css`
- 交互脚本：`demo_web/static/app.js`
- 启动脚本：`demo_web/run_demo_ui.ps1`

这不是一次性的草图，而是一个真正可跑的演示壳。

## 2. 你这边的职责边界

你负责：

1. 把页面视觉做得更像 final 成品
2. 把录屏时的交互流程做顺
3. 检查按钮、表格、滚动、响应速度、空状态
4. 决定最终录制时页面打开顺序
5. 录出一个稳定清晰的视频

你不负责：

1. 改核心实验逻辑
2. 改 evaluation 指标
3. 改 report 里的正式数字
4. 把 live provider 波动问题伪装成 deterministic

## 3. 推荐架构，不要乱改

当前推荐结构就是：

- 前端：静态 `HTML + CSS + JS`
- 后端：`FastAPI`
- 核心逻辑：直接调用 `src.pipeline.ARGTestPipeline`

这是最稳的方案。

不要临时改成：

- 完整 React/Vue 大工程
- 前后端彻底拆成两个独立仓库
- 录视频前才加复杂状态管理

这些都只会增加不稳定性。

## 4. 当前页面应该展示什么

当前页面已经按四块来设计：

1. `Direct Requirement Input`
2. `CSV Batch Import`
3. `State-Model Extraction`
4. `Formal Evidence Dashboard`

你录视频时必须把这四块都体现到，因为它们分别对应老师需求里的：

- `FR 1.0` 输入
- `FR 2.0` 风险
- `FR 3.0` 黑盒测试生成
- `FR 4.0` 状态模型
- `FR 6.0` 结构化结果

## 5. 录屏时的推荐口径

最稳的讲法是：

1. 先说这个页面是 `ARG-Test` 的 demo console
2. 先做一次 `mock` 交互，证明工具真的能跑
3. 再展示 `CSV` 和 `state model`
4. 最后切到 `Formal Evidence Dashboard`
5. 强调最终质量结论来自 frozen official results

不要一上来就说：

- “我们 live provider 每次都完全一致”
- “这个网页本身就是我们的全部项目”

## 6. 必须保留的稳定性原则

录视频时优先：

- `provider=mock`
- `model=mock-arg-test`
- 使用页面里默认示例 requirement

原因很简单：

- 录屏阶段最重要的是稳定
- 最终效果说明已经有 frozen official results 支撑
- 现场不应该赌外部 provider 延迟和波动

## 7. 你最值得做的优化

如果你要继续加工，这几个方向收益最高：

1. 页面层级更清楚
2. 指标卡片更统一
3. 表格行高和字体更舒服
4. 结果区增加更明显的 loading / success / error 状态
5. formal evidence 部分做得更像展示板

如果时间还够，再考虑：

1. 让 figure gallery 支持点击放大
2. 给状态迁移表做更清楚的 legal / illegal 视觉区分
3. 给 artifact path 加复制按钮

## 8. 不要碰的敏感点

1. 不要改 `.local_runs/formal_qwen_novpn` 里的正式结果
2. 不要把 demo 页面上的实时结果拿去替代 report 正文里的正式实验数据
3. 不要为了页面好看，把真实字段名改得和报告口径不一致

## 9. 启动方式

```powershell
cd D:\软件测试\Final\ARG-Test
powershell -ExecutionPolicy Bypass -File demo_web\run_demo_ui.ps1
```

或：

```powershell
python -m uvicorn demo_web.app:app --host 127.0.0.1 --port 8000
```

打开：

```text
http://127.0.0.1:8000
```

## 10. 你最终应该交给我什么

1. 一份能稳定跑的 UI 版本
2. 一次录制用的最终页面状态
3. 录屏前确认过的 demo 流程
4. 如果你改了 UI，告诉我改了哪些文件
