# ARG-Test 五人小组任务分配说明（中文版）

本文档用于把 5 人小组的任务拆到“人、目录、脚本、产出物、时间点”五个层面，目标是两件事：

1. 每个人拿到仓库后可以立刻知道自己该做什么。
2. 每个人都只修改自己负责的文件范围，尽量不发生冲突。

默认分工如下：

- 1 号：许奕，技术总控 / 仓库负责人 / 最终集成负责人
- 2 号：张洛梧，文档与 PPT 负责人
- 3 号：数据集与主实验负责人
- 4 号：Baseline 实验负责人
- 5 号：评测、消融、错误分析负责人

目前已知实名：1 号为许奕，2 号为张洛梧；3/4/5 号可以后续再替换成真实姓名。

---

## 一、总原则

### 1. 项目目标统一

你们最后要交的不是“几个零散脚本”，而是一整套完整项目：

- 可运行仓库
- 可复现实验
- 可直接引用的结果文件
- 可提交的英文报告
- 可演示的英文 PPT

所以每个人都不能只做“自己看得见的一点点”，必须产出能被下一个人直接接住的结果。

### 2. 文件所有权优先

每个成员都有明确的“可编辑目录”和“禁止主动编辑目录”。

原则：

- 优先改自己负责的目录。
- 如果必须改别人的目录，先告诉该目录 owner，再由 1 号决定是否合并。
- 没有授权，不要顺手改别人的脚本。

### 3. 结果文件要可交接

每个实验成员最后必须提交：

- 能复现的命令
- 对应的输出文件路径
- 一段中文总结：做了什么、结果是什么、还有什么问题

否则 2 号没法写文档，1 号也没法最终收口。

### 4. 1 号是唯一总集成人

所有“跨模块修改”“最后统一跑通”“最后改 prompt / parser / checker / llm 接口”“最后整体验收”全部由 1 号负责。

也就是说：

- 其他人不要私自改核心 pipeline。
- 其他人提出问题、提交结果、提出需求。
- 最后统一由 1 号来收束和定版。

---

## 二、目录级分工总表

下面这张表是最重要的执行边界。

| 成员 | 主要职责 | 允许重点编辑的目录/文件 | 原则上不要改的目录 |
| :--- | :--- | :--- | :--- |
| 1 号 | 核心仓库、LLM 接入、parser/checker/pipeline、最终整合 | `src/`（除明确分给别人部分）、`prompts/`、`README.md`、`requirements.txt`、`.env.example` | `report_assets/` 主文稿、`data/` 内容本体 |
| 2 号 | 报告、proposal、PPT、演讲稿、图表排版 | `report_assets/`、最终 `docs/` 或导出 PDF 源文件 | `src/`、`data/`、实验脚本 |
| 3 号 | requirement 数据集、gold specs、主实验运行与主结果整理 | `data/requirements/`、`data/gold_specs/`、`experiments/run_main.py`（仅少量参数层面） | `src/checker/`、`src/parser.py`、`src/llm_client.py` |
| 4 号 | non-AI baseline、plain LLM baseline、structured-no-checker baseline | `src/baselines/`、`experiments/run_baselines.py` | `src/checker/`、`src/pipeline.py` 核心逻辑 |
| 5 号 | metrics、ablation、generalization、failure analysis | `src/evaluation/`、`experiments/run_ablation.py`、必要时新增 `experiments/run_generalization.py` | `src/llm_client.py`、`prompts/`、`data/requirements/` |

补充说明：

- `outputs/` 和 `artifacts/` 是运行结果目录，不算“代码所有权目录”。谁跑自己负责的实验，谁生成自己的结果文件，但不要手改别人结果。
- `__pycache__/` 一律不要提交，也不要把它当可编辑内容。

---

## 三、每位成员的具体任务

---

## 1 号：技术总控 / 仓库负责人 / 最终集成人

### 你的角色定位

你不是单纯写代码的人，你是整个项目的“主线负责人”。

你的职责包括：

- 维护核心架构不跑偏
- 定义实验接口和文件格式
- 负责最终真实模型接入
- 接收 3/4/5 号的实验结果并统一整合
- 接收 2 号的文档需求并补齐代码/结果支撑
- 最后完成一次从 requirement 到 report 的闭环验收

### 你负责的目录

重点负责：

- `src/config.py`
- `src/llm_client.py`
- `src/parser.py`
- `src/pipeline.py`
- `src/repair.py`
- `src/reranker.py`
- `src/checker/`
- `prompts/`
- `README.md`
- `requirements.txt`
- `.env.example`

你可以改，但尽量最后阶段再统一处理：

- `experiments/run_main.py`
- `experiments/run_baselines.py`
- `experiments/run_ablation.py`

### 你必须完成的具体任务

#### 任务 1：锁定技术接口

你要先把下面这些接口定义清楚，并发给组员：

- requirement 文件命名规则
- gold spec 文件命名规则
- baseline 输出结果命名规则
- ablation 输出结果命名规则
- 所有 summary JSON 的字段格式
- 最终 test case CSV / JSON / Markdown 的字段格式

你要明确告诉所有人：

- 哪个脚本生成哪个输出文件
- 哪个结果文件是 2 号写文档时要引用的“唯一正式来源”

#### 任务 2：接入真实 LLM

当前仓库默认是 `mock` provider。你最后必须完成：

- 选择真实模型和 provider
- 在 `src/llm_client.py` 中接入真实 API
- 测试 `prompts/system_prompt.txt`
- 测试 `prompts/generation_prompt.txt`
- 测试 `prompts/repair_prompt.txt`
- 确定 candidates 数量，例如 1、3 或 5
- 确定是否启用 repair

这里是你的核心工作，其他人不要碰。

#### 任务 3：稳定 parser + checker + pipeline

你要保证：

- 结构化 trace 可以被 `src/parser.py` 正确解析
- `src/checker/` 中的 schema / EP / BVA / Decision / State checker 不会乱报错
- rerank / repair 不会把已有正确结果破坏掉
- `python -m src.main batch ...` 能在真实 provider 下跑通

#### 任务 4：统一合并实验需求

3/4/5 号在做实验时，一定会提出很多修改需求，比如：

- 某个 requirement 不好解析
- baseline 输出格式不统一
- 某个 checker 太严格或太松
- JSON summary 缺字段
- 文档需要增加统计项

这些修改由你统一处理。不要让 3/4/5 号自己去乱改核心 `src/`。

#### 任务 5：最终项目验收

项目最后一周，你必须完成一次完整验收：

1. 检查 `data/requirements/` 和 `data/gold_specs/` 是否定稿。
2. 检查 baseline 和 ablation 是否都能跑。
3. 检查 `outputs/final_tests/` 是否齐全。
4. 检查 `outputs/reports/` 是否有最终引用版本。
5. 检查 2 号文档里的表格、数字、图是否都能在仓库中找到来源。
6. 最后再跑一遍完整实验或至少抽样复跑关键实验。

### 你最后要交付给全组的东西

- 最终可运行仓库
- 最终模型配置说明
- 最终 prompt 定稿
- 最终实验脚本定稿
- 最终结果目录定稿
- 给 2 号的“可引用结果清单”

---

## 2 号：张洛梧，文档与 PPT 负责人

### 你的角色定位

2 号不是“最后把大家内容拼起来的人”，而是从项目中期就开始构建文档主线的人。

你的职责是：

- 提前建立报告结构
- 持续接收 1/3/4/5 号的结果
- 把结果转成可提交的 proposal、report、PPT、演讲稿
- 最后负责 presentation 逻辑和视觉一致性

### 你负责的目录

重点负责：

- `report_assets/report_outline.md`
- `report_assets/ppt_outline.md`
- `report_assets/project_proposal_full_en.md`
- `report_assets/proposal_ppt_script_en.md`
- 你后续新增的报告和 PPT 文稿文件

建议新增但只由你负责的文件：

- `report_assets/final_report_draft_en.md`
- `report_assets/final_ppt_script_en.md`
- `report_assets/figures_needed_checklist_cn.md`
- `report_assets/table_inventory_cn.md`

### 你必须完成的具体任务

#### 任务 1：建立最终文档框架

你要在最早阶段就把下面内容搭起来：

- 报告目录
- 每节要放什么内容
- 每张图表需要谁提供
- 每张实验表的编号和含义
- PPT 每页讲什么

你不要等实验全部做完再开始写，那样一定来不及。

#### 任务 2：维护“结果需求清单”

你要建立一个文档，明确告诉 3/4/5 号：

- 主实验表需要哪些指标
- baseline 对比表需要哪些指标
- ablation 表需要哪些指标
- case study 需要哪些原始输出截图或样例
- failure analysis 需要哪些典型失败例子

这个清单最好按表来列，例如：

- 表 1：Main comparison
- 表 2：Baseline comparison
- 表 3：Ablation
- 表 4：Cost analysis
- 图 1：整体架构图
- 图 2：一个 requirement 到 final tests 的案例图

#### 任务 3：负责 proposal / report / PPT 的语言整合

你要把实验成员给的结果转成英文论文式表达。

你的文档一定要覆盖：

- 背景和问题
- 为什么 plain LLM 不够
- 我们的方法
- baselines
- 实验设置
- 主结果
- 消融实验
- 局限性
- 与非 AI 方法对比
- 结论

#### 任务 4：准备 presentation 版本

你最后要把书面报告内容转成 15 分钟 presentation 版本。重点不是内容越多越好，而是逻辑清晰：

- 什么问题
- 为什么难
- 你们的方法是什么
- 为什么比 plain LLM 更强
- 实验支持什么结论
- 局限性是什么

### 你不要做的事情

- 不要自己改 `src/` 核心逻辑
- 不要自己改实验脚本
- 不要自己去“编造”实验数字
- 不要自己推断结果，所有数字必须来自正式输出文件

### 你最后要交付给全组的东西

- 最终 proposal 英文版
- 最终 report 英文版
- 最终 PPT 逐页文案
- 最终答辩提纲
- 图表需求清单与最终图表来源表

---

## 3 号：数据集与主实验负责人

### 你的角色定位

3 号负责“项目输入质量”和“主实验跑通”。

一句话：
如果 3 号的数据和 gold spec 没做好，后面的 coverage、comparison、ablation 都会变得不可信。

### 你负责的目录

重点负责：

- `data/requirements/dev/`
- `data/requirements/test/`
- `data/gold_specs/dev/`
- `data/gold_specs/test/`
- `experiments/run_main.py`（仅参数和运行层面）

你可以新增的辅助文档：

- `data/requirements/requirement_catalog_cn.md`
- `data/gold_specs/gold_spec_guideline_cn.md`
- `outputs/reports/dev/run_main_notes_cn.md`
- `outputs/reports/test/run_main_notes_cn.md`

### 你必须完成的具体任务

#### 任务 1：定稿 requirement 数据集

你要把 requirement 数据集整理成最终版本，要求：

- `dev` 集和 `test` 集明确分开
- 每个 requirement 有唯一 ID
- requirement 内容是完整、可理解、适合黑盒测试的
- requirement 类型要有覆盖：
  - 输入校验类
  - 业务规则类
  - 状态流转类

你要检查每个 requirement：

- 是否存在明显歧义
- 是否真的可以设计出 EP/BVA/Decision/State 测试
- 是否有明确 expected behavior
- 是否会让模型输出无法判断对错

#### 任务 2：编写 gold specs

你要为每个 requirement 写对应的 gold spec，至少包括：

- `valid_partitions`
- `invalid_partitions`
- `boundaries`
- `decision_rules`
- `states`
- `illegal_transitions`
- `exception_cases`

你负责的是“金标准 checklist”，不是随便填几个字段。

每写完一个 gold spec，都要自查：

- 这个 requirement 的核心覆盖点有没有漏
- 这个 gold spec 会不会和 requirement 文本矛盾
- 这个 gold spec 能不能被后面的 `metrics.py` 用来统计

#### 任务 3：运行主实验

你要负责主流程实验的运行与结果整理。标准命令示例：

```powershell
Set-Location 'd:\软件测试\ARG-Test'
python experiments\run_main.py --split dev --provider mock --model mock-arg-test --candidates 3
python experiments\run_main.py --split test --provider mock --model mock-arg-test --candidates 3
```

后续真实模型接入后，由 1 号给你新的 provider / model 参数，你再跑正式版本。

#### 任务 4：整理主实验交接物

你跑完后要交给 1 号和 2 号：

- 主实验命令
- 主实验输出文件路径
- 每个 requirement 的最终 score
- 哪几个 requirement 表现最好
- 哪几个 requirement 表现最差
- 主流程的典型成功样例
- 主流程的典型失败样例

### 你不要做的事情

- 不要自己改 `src/checker/`
- 不要自己改 `src/parser.py`
- 不要自己接 API
- 不要自己定义新的主流程逻辑

如果你发现问题：

- 把问题记录清楚
- 标注是哪个 requirement、哪个输出、哪个 checker
- 交给 1 号处理

### 你最后要交付给全组的东西

- 定稿 requirement 数据集
- 定稿 gold specs
- 主实验最终 summary
- 主实验成功/失败案例清单
- 给 2 号可直接引用的主实验说明

---

## 4 号：Baseline 实验负责人

### 你的角色定位

4 号负责“对比组是否成立”。

如果 baseline 做得太弱，你们的实验就没有说服力；如果 baseline 输出格式乱，2 号也没法写对比分析。

### 你负责的目录

重点负责：

- `src/baselines/plain_llm.py`
- `src/baselines/rule_based.py`
- `src/baselines/structured_no_checker.py`
- `src/baselines/__init__.py`
- `experiments/run_baselines.py`

你可以新增的辅助文档：

- `outputs/reports/test/baseline_notes_cn.md`
- `outputs/reports/test/baseline_observations_cn.md`

### 你必须完成的具体任务

#### 任务 1：完善三个 baseline

你要把以下三个 baseline 做到“逻辑清晰、输出统一、可比较”：

1. `rule_based`
2. `plain_llm`
3. `structured_no_checker`

你的重点不是把 baseline 做得和主方法一样复杂，而是：

- 它们要足够合理
- 它们要能稳定运行
- 它们的输出格式要能被统一评测

#### 任务 2：统一 baseline 输出格式

你要保证三种 baseline 最后都能落到统一形式：

- `test_count`
- `duplicate_count`
- `coverage`
- `overall_coverage`
- `checker_score`

如果 baseline 输出结构不统一，5 号很难做后续比较，2 号也很难画表。

#### 任务 3：运行 baseline 对比实验

标准命令示例：

```powershell
Set-Location 'd:\软件测试\ARG-Test'
python experiments\run_baselines.py --split test --provider mock --model mock-arg-test
```

正式实验阶段，再使用 1 号给你的真实 provider / model 参数。

#### 任务 4：形成 baseline 分析结论

你不能只交一个 JSON 文件。你还要交：

- 哪个 baseline 最弱，为什么
- plain LLM 主要失败在哪
- structured-no-checker 比 plain LLM 强在哪里
- rule-based 的优势和劣势分别是什么

### 你不要做的事情

- 不要改 `src/pipeline.py` 主逻辑
- 不要改 `src/checker/`
- 不要改 `data/gold_specs/`
- 如果需要新增统计项，先和 5 号、1 号确认

### 你最后要交付给全组的东西

- baseline 脚本定稿
- baseline summary JSON
- baseline 中文结论说明
- 给 2 号可直接引用的 baseline 对比要点

---

## 5 号：评测、消融、错误分析负责人

### 你的角色定位

5 号负责“把实验讲清楚”。

一句话：
3 号和 4 号主要负责把结果跑出来，你负责把这些结果变成“可分析、可对比、可写进论文”的评测体系。

### 你负责的目录

重点负责：

- `src/evaluation/metrics.py`
- `src/evaluation/__init__.py`
- `experiments/run_ablation.py`

必要时你可以新增：

- `experiments/run_generalization.py`
- `outputs/reports/test/ablation_notes_cn.md`
- `outputs/reports/test/failure_analysis_cn.md`
- `outputs/reports/test/generalization_notes_cn.md`

### 你必须完成的具体任务

#### 任务 1：明确评测口径

你要检查并定稿当前评测项，确保所有 summary 结果都是可解释的。

至少要覆盖：

- valid partition coverage
- invalid partition coverage
- boundary coverage
- decision rule coverage
- state coverage
- illegal transition coverage
- exception coverage
- duplicate count
- overall coverage
- checker score

你要对每个指标写一句中文说明：

- 它在测什么
- 它的值高说明什么
- 它的局限是什么

#### 任务 2：做消融实验

你要重点比较：

- structured-no-checker
- full pipeline

如果 1 号后面把 best-of-N / repair 接到真实模型上，你还要继续比较：

- 单候选 vs 多候选 rerank
- repair off vs repair on

标准命令示例：

```powershell
Set-Location 'd:\软件测试\ARG-Test'
python experiments\run_ablation.py --split test --provider mock --model mock-arg-test --candidates 3
```

#### 任务 3：做失败模式分析

你要从输出中总结模型最常见的错误类型，例如：

- 漏 invalid cases
- 漏边界点
- decision rules 不全
- state transition 不完整
- expected output 不一致
- checker score 高但 coverage 仍不足

你需要把失败模式总结成“类别 + 典型 requirement + 典型输出路径 + 原因解释”的格式。

#### 任务 4：支持 2 号做 results / limitations

你要把分析结果转成 2 号能直接使用的形式：

- 一段主结果解释
- 一段消融结果解释
- 一段局限性说明
- 一段 threat to validity 说明

### 你不要做的事情

- 不要改 requirement 数据集内容
- 不要改 baseline 逻辑
- 不要私自修改主流程 prompt
- 不要和 1 号抢核心 pipeline 逻辑

### 你最后要交付给全组的东西

- metrics 说明定稿
- ablation summary
- failure analysis
- generalization 或 requirement-type 分析
- 给 2 号可直接引用的结果解释和 limitation 段落素材

---

## 四、为了避免冲突，必须执行的协作规则

## 1. Git 分支规则

每个人固定自己的分支：

- 1 号：`feat/integration-final`
- 2 号：`feat/docs-ppt`
- 3 号：`feat/data-main-exp`
- 4 号：`feat/baselines`
- 5 号：`feat/eval-ablation`

不要所有人都在 `main` 上改。

## 2. 提交规则

每次提交信息必须写清楚范围，例如：

- `data: finalize 2 dev requirements and gold specs`
- `baseline: improve structured_no_checker output normalization`
- `eval: add boundary coverage notes and ablation summary`
- `docs: draft method and experiment sections`

不要写：

- `update`
- `fix`
- `change files`

## 3. 冲突处理规则

如果你发现自己必须改别人的目录：

1. 先把原因发给 1 号。
2. 说明改哪个文件。
3. 说明为什么你这边不能绕开。
4. 等 owner 或 1 号确认后再改。

## 4. 结果交接规则

3/4/5 号每次交结果给 1 号和 2 号时，必须带这三样：

- 运行命令
- 输出文件路径
- 中文说明 5 到 10 行

例如：

```text
命令：python experiments\run_baselines.py --split test --provider openai --model xxx
输出：outputs/reports/test/baseline_summary.json
结论：plain LLM 在 4 个 requirement 上平均 overall coverage 低于 structured-no-checker，主要漏 invalid partition 和 boundary。
```

## 5. 核心文件冻结规则

在最后整合阶段，以下文件默认冻结，只允许 1 号修改：

- `src/llm_client.py`
- `src/parser.py`
- `src/pipeline.py`
- `src/checker/*`
- `prompts/*`

冻结后，其他人只能提 issue，不能再直接改。

---

## 五、推荐执行时间表（按阶段）

这里不写死具体日期，统一用 T0、T1、T2 来表示。

## 阶段 T0：仓库初始化完成后，立即开始

### 1 号

- 讲解目录结构
- 讲解接口
- 发布分工说明
- 指定每人目录边界

### 2 号

- 建好 report / PPT 主框架
- 列结果需求清单

### 3 号

- 检查 requirement 集是否足够
- 开始补充或修订 gold specs

### 4 号

- 检查 baseline 当前逻辑
- 规划 baseline 对比项

### 5 号

- 检查 metrics 定义
- 规划 ablation 和 failure analysis 模板

## 阶段 T1：数据与实验口径冻结

### 3 号必须完成

- requirement 数据集定稿
- gold specs 第一版定稿

### 4 号必须完成

- baseline 脚本可跑
- baseline 输出字段统一

### 5 号必须完成

- metrics 口径定稿
- ablation 脚本可跑

### 1 号必须完成

- 真正接 API 或至少准备好 provider 接入方案
- 确认 prompt 与 parser 可用

### 2 号必须完成

- proposal 主体初稿
- PPT 结构初稿

## 阶段 T2：正式实验阶段

### 3 号

- 跑主实验
- 整理主结果

### 4 号

- 跑 baseline 对比
- 整理 baseline 结论

### 5 号

- 跑 ablation
- 做 failure analysis
- 整理 limitation / threats to validity 素材

### 1 号

- 处理跑实验时暴露出来的 parser/checker/pipeline 问题
- 决定是否重跑关键实验

### 2 号

- 实时把结果写进 report 和 PPT
- 向 3/4/5 号催缺失图表和说明

## 阶段 T3：最终收口阶段

### 1 号

- 冻结核心代码
- 统一整合结果
- 最后复跑关键脚本

### 2 号

- 定稿 report
- 定稿 PPT
- 定稿演讲稿

### 3/4/5 号

- 只负责补缺失结果和解释
- 不再大改代码逻辑

---

## 六、每个人交付给 1 号和 2 号的最终清单

## 3 号最终清单

- `data/requirements/` 最终版
- `data/gold_specs/` 最终版
- `outputs/reports/*/run_main_summary.json`
- 主实验成功/失败案例说明

## 4 号最终清单

- `src/baselines/` 最终版
- `experiments/run_baselines.py` 最终版
- `outputs/reports/test/baseline_summary.json`
- baseline 中文分析说明

## 5 号最终清单

- `src/evaluation/metrics.py` 最终版
- `experiments/run_ablation.py` 最终版
- `outputs/reports/test/ablation_summary.json`
- failure analysis 中文说明
- limitations / threats to validity 素材

## 2 号最终清单

- proposal 定稿
- report 定稿
- PPT 定稿
- 讲稿定稿
- 图表来源表

## 1 号最终清单

- 最终可运行仓库
- 最终 prompt 和 API 配置
- 最终实验命令清单
- 最终提交包检查清单

---

## 七、最关键的“禁止事项”

下面这些事如果不禁止，最后一定冲突：

- 3/4/5 号不要同时改 `src/pipeline.py`
- 2 号不要自己发明实验数字
- 4 号不要自己改 gold specs
- 5 号不要自己改 requirement 文本
- 所有人不要直接在 `main` 上乱改
- 所有人不要把“本地临时测试结果”当最终结论
- 所有人不要把 `mock` 结果写成真实实验结论

---

## 八、推荐的实际执行顺序（最稳妥版本）

如果你要的是最现实、最不容易翻车的执行路线，那就按下面顺序走：

1. 1 号先把接口、目录边界、结果格式讲清楚。
2. 3 号先把 requirement 和 gold specs 做扎实。
3. 4 号把 baseline 跑通并固定输出格式。
4. 5 号把 metrics 和 ablation 体系搭好。
5. 2 号从一开始就同步写文档，不要等到最后。
6. 1 号在中后期接真实模型、统一修 bug、统一重跑。
7. 最后由 1 号和 2 号一起收口：1 号保代码和结果，2 号保 presentation 和文档。

---

## 九、给你这个 1 号的实际建议

如果最后你会和我一起把项目跑通，那你现在最应该做的，不是自己把所有实验都做了，而是：

- 先把这份分工说明发给组员
- 要求 3/4/5 号每个人只对自己的目录负责
- 要求 2 号提前建立文档框架
- 你只盯三件事：
  - 核心 pipeline 稳定
  - 真实模型接入
  - 最后统一整合

这样分配以后，你不会被 baseline、数据、报告、PPT 四条线同时拖死，而且最后还能把整套系统真正跑通。


