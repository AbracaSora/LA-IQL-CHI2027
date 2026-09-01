# CHI 2027 论文成稿缺口与执行清单

更新日期：2026-08-27

适用主稿：`sigconf-authordraft.tex`

实验工作目录：`../../LA-IQL-Test/`

## 1. 使用说明

本文档把当前论文距离可模拟评审稿/正式投稿稿的缺口分为四类：

1. **A：实验或材料已经完成，但尚未写入论文**：原则上不需要重新运行模型，只需核实来源并落稿。
2. **B：当前即可完成**：主要是写作、格式、审计和已有材料整理，不依赖新增实验结果。
3. **C：需要实验得到**：必须运行新实验、重新统计或完成人工评价后才能填写。
4. **D：需要人工或外部确认**：无法仅从现有代码和产物可靠恢复，需要作者、数据提供方或伦理/平台记录确认。

当前优先级按论文所处里程碑划分，而不是只按正式投稿风险划分：

- **P0-Draft（导师初稿）**：阻塞理论收口、文章结构完整或导师有效审阅；当前立即完成。
- **P1-Evidence（证据补全）**：在导师确认主线后补充正式实验、统计或材料；可能阻塞核心结果定稿，但不阻塞结构完整的导师初稿。
- **P2-Submission（投稿合规）**：正式投稿前必须完成的伦理、匿名、复现和提交包工作；不应阻塞当前初稿形成。
- **P3-Enhancement（增强项）**：只有在主稿闭环、关键证据完成且时间允许时继续。

文中原有的 **P0/P1/P2** 表示面向正式投稿的风险等级；若与以上阶段优先级冲突，以本节和第 6 节的当前执行顺序为准。

“格式”指最终应在论文或补充材料中采用的呈现形式，而不是文件格式。

### 1.1 当前落稿状态（2026-08-27）

- **已写入并完成**：A1--A6、A8--A10；B1、B2、B4、B5、B6a、B7、B9、B11；全文 claim--evidence 主线审计。
- **已部分写入**：A7（BC 训练 metadata 已进入附录，但尚未进入正式 horizon-100 主比较）；B3（核心训练配置已进入附录，其余 provenance 采用尽力恢复与透明披露原则）；B12（已转换单栏匿名格式并通过编译，仍需最终 source ZIP 清理）。
- **已完成写入**：B6a 与 B6b-KG（RQ4 理论、KG 方法、250 图谱的九系统主表、配对统计、Results、Conclusion、Limitations 及中文翻译已同步）；辅助 Judge、人工 KG 审计、受控门修复、稳定性改进和 growth curve 转入 C6b--C6e。
- **仍可继续但本轮未完成**：B10（规则化定性案例）。
- **受外部确认阻塞**：B8 只需与 D1 一起达到 CHI 投稿所需的如实披露水平；不能仅凭代码目录推断数据许可、伦理审查状态或去标识化流程。
- **无需新增实验但已明确披露缺口**：D2 已恢复三阶段核心配置；其余尚未确认字段已在附录和 D2 清单列明，避免用当前脚本默认值反推。

本轮写入位置：正文的 Abstract、Method、Experimental Design、Results、Discussion、Conclusion、Limitations，以及附录的 Implementation and Reproducibility 与 Context-Sensitivity Intervention。

### 1.2 当前里程碑：供导师修改的理论闭环初稿

当前首要目标不是立即补齐全部实验或投稿材料，而是形成一份理论主线闭合、章节齐全、已有证据与主张边界一致的初稿。该版本应允许导师直接修改研究问题、贡献定位和论证结构，而不必等待新增实验。

当前 claim--evidence 工作表：[`CLAIM_EVIDENCE_MATRIX.md`](CLAIM_EVIDENCE_MATRIX.md)。该表是全文主张审计的唯一入口；新增或删除核心主张时，应同步更新其证据、允许措辞与禁止外推边界。

当前优先顺序如下：

1. **P0-Draft**：claim--evidence 主线审计、B6a 与 B11 已完成；下一步完成 B10 和 B12a，并在后续修改核心主张时维护对照表。
2. **P1-Evidence**：导师确认主线后执行 C6，并视反馈补 A7、C1--C3；再把正式结果写回摘要、Results 和 Conclusion。
3. **P2-Submission**：完成 B8/D1、D3--D5、B12b 和剩余 provenance/匿名/提交包工作。
4. **P3-Enhancement**：C4、C5、C7、C8 及其他不改变当前核心论证的增强实验。

导师初稿允许存在明确标记的内部结果占位符，但不得预写实验方向、虚构数值或把计划中的 C6 当成已完成证据。

---

## 2. A 类：已有材料的落稿状态

### A1. Policy backbone 与动作头身份

- **名称**：主策略模型身份。
- **内容及解释**：主 checkpoint 的 backbone 为 `Qwen/Qwen3.5-0.8B`，policy head 输出维度为 31。正文当前只写了抽象的 language model/backbone，没有给出可核验身份。
- **获取方式**：读取 `../../LA-IQL-Test/checkpoints/sft_stage3/final/meta.json`；模型结构细节可从同目录 `config.json` 获取。
- **重要性及原因**：**P0**。评审必须知道模型规模和底座，才能判断方法贡献、计算预算与基线公平性。
- **格式**：正文 Implementation Summary 一行；附录补充模型 revision、参数量、tokenizer 与结构配置。

### A2. Role model 与 rationale annotation model

- **名称**：语言实现模型和 rationale 重写模型。
- **内容及解释**：teacher/student role model 均记录为 `deepseek-chat`，role-model temperature 为 0.8；rationale rewrite 同样使用 `deepseek-chat`，temperature 为 0.7，共处理 9,168 条记录。
- **获取方式**：读取 formal trajectory 尾部的 `config`；rationale 信息来自 `../../LA-IQL-Test/artifacts/rationale_rewrite_deepseek/rewrite_manifest.json`。
- **重要性及原因**：**P0**。两类外部模型直接影响 rationale 和最终话语，不能继续以匿名的 “annotation model”/“role model” 代替。
- **格式**：正文 Implementation Summary；附录列 provider、调用日期、prompt version、temperature 和输出数量。

### A3. 冻结数据划分与哈希

- **名称**：Formal split provenance。
- **内容及解释**：lesson-level 35/5/10 划分，split seed 为 `20260731`，按 `subject|stage` 分层；已有 source、original、rewritten 和 expert data SHA-256。
- **获取方式**：读取 `../../LA-IQL-Test/artifacts/g1_formal/split_manifest.json`。
- **重要性及原因**：**P0**。它证明 lesson 无泄漏、划分在正式评价前冻结，并允许复核数据版本。
- **格式**：正文保留 35/5/10、lesson-level 和分层规则；附录 Reproducibility 表列 split seed、version 和 SHA-256。

### A4. Rationale 重写 provenance 与自动质量报告

- **名称**：Rationale annotation provenance。
- **内容及解释**：已有 prompt version、run fingerprint、input digest、模型、temperature、运行时间、记录数、唯一率、平均长度和重试次数。当前质量报告版本是 `length-only-v1`，只能证明格式/长度/唯一性，不能当作语义正确性证据。
- **获取方式**：读取 `rewrite_manifest.json`、`rewrite_quality_report.json` 和 `prompts/rationale_rewrite/`。
- **重要性及原因**：**P1**。rationale 是模型输入和论文贡献的一部分，必须说明其由谁、如何生成以及当前审计边界。
- **格式**：附录单独一小节和一张 provenance 表；正文用一句话说明由 DeepSeek 生成并经过标签泄漏过滤。

### A5. Formal inference 实际配置

- **名称**：Direct/Candidate rollout configuration。
- **内容及解释**：实际轨迹内已经记录 policy window 2 turns/2 actions、role window 30 turns/5 actions、policy max length 512、rationale max-new-tokens 256、role temperature 0.8、每角色 3 个候选、horizon 100、`END` minimum step 50 和 logit margin 3.0。
- **获取方式**：优先读取 `traj_rd/formal_100/*/seed*/<lesson>.json` 尾部 `config`，不要直接抄当前 `inference_rd.py` 默认值。
- **重要性及原因**：**P0**。当前脚本的 `END_MIN_STEP` 已漂移为 80，而论文 formal trajectories 记录为 50；实际轨迹配置才是结果的权威来源。
- **格式**：正文 Implementation Summary 保留核心窗口、temperature、候选数和 stopping rule；完整配置放附录。

### A6. Generation seeds 的真实含义

- **名称**：训练随机性与生成随机性区分。
- **内容及解释**：formal workflow 中 seeds 42、43、44 是 `generation_seed`，三个 seed 共享同一个 `sft_stage3/final` checkpoint；它们不能写成三个独立训练重复。
- **获取方式**：核对 `scripts/workflows/run_sft_stage3_formal_100.ps1`、`run_sft_stage3_woTD_direct_formal_100.ps1` 和 trajectory JSON。
- **重要性及原因**：**P0**。若继续模糊称为 “three seeds”，评审可能认为统计推断包含训练随机性，构成方法学误导。
- **格式**：所有表注统一改为 “three generation seeds”；正文统计协议明确推断仅针对固定 checkpoint 下的 lesson/rollout variation。

### A7. Frozen BC 与 LoRA BC 的训练配置

- **名称**：强 learned baseline provenance。
- **内容及解释**：Frozen BC 和 LoRA BC 已有三训练 seeds 的 `baseline_meta.json`，包括 objective、base model、样本数、validation 数、epochs、batch size、learning rate、max length、LoRA rank、dtype、peak memory 和 epoch history。
- **获取方式**：读取 `checkpoints/baselines/formal/sft_bc_seed*/baseline_meta.json` 与 `lora_policy_seed*/baseline_meta.json`。
- **重要性及原因**：**P1-Evidence；正式投稿时是否升为 P0 取决于最终 baseline 主张**。它不阻塞导师初稿，但完整同数据 learned BC 能帮助评审判断 LA-IQL 是否超过局部 imitation；若暂不纳入，初稿必须明确其状态和当前比较边界。
- **格式**：正文 baseline 表至少列 Frozen BC/LoRA BC 是否进入主比较；完整超参数和训练曲线放附录。

### A8. 上下文敏感性干预结果

- **名称**：Context-dependence diagnostic。
- **内容及解释**：在 50 个预冻结 held-out states 上，替换话语语义但保留动作历史与说话者结构后，Full 模型 expert-action probability 平均下降 0.0767，60% 状态发生 argmax 翻转，JSD 为 0.2957；Macro-F1 降幅区间跨零。该结果支持“策略分布利用文本语义”，但不证明上下文适切性优势。
- **获取方式**：读取当前论文仓库 `../experiments/context_sensitivity/REPORT_ZH.md` 及其 `artifacts/`；源 checkpoint 与预测保存在相应 manifest 中。
- **重要性及原因**：**P0**。论文用 Markov control 证明局部统计不足，却缺少 LA-IQL 确实使用语义上下文的正向证据；该实验正好填补逻辑断点。
- **格式**：正文 Results 增加一段 exploratory finding；附录放完整表、干预定义和置信区间，并明确 50-state 限制。

### A9. Generation validity gate

- **名称**：结构化输出验收。
- **内容及解释**：主模型与 no-TD checkpoint 均保存 50-sample generation validation，结构合法率、rationale/action 闭合率为 100%，无 degeneration 或长度上限命中。
- **获取方式**：读取 `checkpoints/sft_stage3/final/generation_validation.json` 和 `checkpoints/sft_stage3_woTD/final/generation_validation.json`。
- **重要性及原因**：**P2**。它不能证明策略质量，但能证明结果不是由 schema 破坏或结构解析失败造成。
- **格式**：附录 Implementation/Quality Gates 表；正文无需展开。

### A10. 软件依赖与可执行环境

- **名称**：Software environment。
- **内容及解释**：已有 Python 最低版本、Torch/Transformers/PEFT/scikit-learn 等依赖范围、CUDA 12.8 wheel 索引和完整 `uv.lock`。
- **获取方式**：读取 `../../LA-IQL-Test/pyproject.toml` 与 `uv.lock`。
- **重要性及原因**：**P1**。支撑代码复现并减少模型加载/数值行为差异。
- **格式**：附录环境表；补充材料保留 lockfile，正文只报告主要框架版本。

---

## 3. B 类：当前可以完成，不需要新增实验（含本轮状态）

### B1. 转换为 CHI 2027 单栏匿名审稿格式

- **名称**：Review-format conversion。
- **内容及解释**：当前 `sigconf,review,anonymous` 生成双栏稿；CHI 2027 初审应使用 `manuscript,review,anonymous` 单栏格式。
- **获取方式**：修改主稿 document class，在单栏模式重新编译并逐页检查图表、公式、浮动体和行号。
- **重要性及原因**：**P0**。错误审稿格式存在直接 desk-reject 风险。
- **格式**：`\documentclass[manuscript,review,anonymous]{acmart}`；输出单栏匿名 PDF。

### B2. 正文 Implementation Summary

- **名称**：核心实现摘要表。
- **内容及解释**：用紧凑表格集中报告数据划分、policy/role/annotation models、核心 loss、checkpoint 数、训练/生成 seed、Direct/Candidate 配置与 rollout protocol。
- **获取方式**：从 A1--A7 的权威 manifest、checkpoint meta 和 trajectory config 整理；未知值不得由当前脚本倒推。
- **重要性及原因**：**P0**。让评审不翻附录也能判断模型规模、比较公平性和统计边界。
- **格式**：正文半栏至一栏的两列 `Component | Configuration` 表。

### B3. 附录 Reproducibility Details

- **名称**：核心复现与 provenance 表。
- **内容及解释**：优先整理会影响方法理解和 Full/no-TD 比较的核心配置，包括模型、batch、epochs、LoRA 训练方式、loss weights、context window、seed 与 checkpoint 来源。optimizer 细节、软件小版本、data/checkpoint hashes 和完整运行入口在能够可靠恢复时补充。
- **获取方式**：先填已被 artifacts 证明的值；主 checkpoint 缺失参数标为“待历史日志核实”，不能直接使用当前 `sft.py` 默认配置。
- **重要性及原因**：**P1**。核心配置应足以解释方法与主要消融；无法恢复的次要执行细节只要透明披露，不阻塞模拟评审或投稿冻结。
- **格式**：附录 1--2 张紧凑表；prompt 全文可在补充材料中提供，机器可读 manifest 属于增强项。

### B4. 系统差异与混杂表

- **名称**：System provenance matrix。
- **内容及解释**：逐行列出 Full Direct、Candidate、w/o-TD Direct、Frozen BC、LoRA BC 的 checkpoint、训练目标、TD、动作选择、rationale temperature、role candidates、训练 seed 和生成 seed。
- **获取方式**：结合 workflow、trajectory config 和 baseline metadata。
- **重要性及原因**：**P0**。Direct--Candidate 同时改变 decoding mode 和 rationale temperature；该表能防止读者误认其为单因素消融。
- **格式**：正文或 Results 开头一张横向表；混杂项用脚注/符号突出。

### B5. 收缩 TD 推断措辞

- **名称**：Fixed-checkpoint inference boundary。
- **内容及解释**：在未获得独立训练重复前，把“TD significantly reduces repetition”改为“for the evaluated fixed checkpoints, TD trajectories show lower repetition”；明确 bootstrap 聚类 lesson，而非训练 seed。
- **获取方式**：全文搜索 `significant`、`stabilizes`、`TD regularization`、`three seeds`，逐句对照实验单位。
- **重要性及原因**：**P0**。避免把生成随机性错误外推为训练方法稳定性。
- **格式**：摘要、Results、Discussion、Conclusion 统一改写；表注统一写 generation seeds。

### B6. 将 RQ4 转为长程知识建构问题

- **状态（2026-08-29）**：**KG-only 初稿闭环已完成**。英文主稿与中文翻译已写入 250 张正式图谱、九个系统的三个预指定端点、Direct--Candidate 与 Direct--w/o-TD 的 lesson-cluster 比较，并同步更新 Abstract、Results、Conclusion 与 Limitations。正文暂不写入 LLM Judge、临时可靠性阈值、受控门失败、人工审计空表或稳定性改进结果。
- **名称**：Knowledge-construction framing 与结果集成。
- **内容及解释**：**B6a（P0-Draft）** 理论定义与文章结构已完成；**B6b-KG（P0-Draft）** 正式 KG 数值、主表和结论已完成。尚未进入论文的辅助 judge、growth curve、人工语义审计和受控验证改进继续留在 C6，不阻塞导师初稿。结果只能说明生成文本中表达的知识结构，不能说明学生认知改变、事实正确性、教学质量或学习效果。
- **获取方式**：以 `todo/G4_KNOWLEDGE_CONSTRUCTION_EVALUATION_PLAN.md` 为冻结设计依据；KG 主结果已同步写入 RQ4、Evaluation Metrics、Results、Conclusion、Limitations 和中文翻译。未完成的辅助评价不在论文中预留位置，分别按 C6b--C6e 继续追踪。原 G4-v1 分类器训练未完成，其一致率、Macro-F1、显著性和系统排名已从主稿移除。
- **重要性及原因**：**B6a 为 P0-Draft；B6b 为 P1-Evidence，正式投稿时为 P0**。先固定理论问题和证据边界，避免在导师审阅前把时间投入到可能因主线调整而作废的完整实验。
- **格式**：导师初稿正文包含完整 RQ4、KG 方法、主表、配对区间、结论与边界；不保留明显占位段。未完成或需重设计的辅助评价只在本 TODO 中追踪。

### B7. 将上下文干预纳入论文

- **名称**：Context-sensitivity subsection。
- **内容及解释**：使用 A8 的既有结果补充“模型是否读取对话语义”，同时保留 Macro-F1 不显著和单 donor/50-state 的限制。
- **获取方式**：从现有报告提取正式英文表述、protocol 和表格；核对数值与 machine-readable artifacts。
- **重要性及原因**：**P0**。这是连接“Markov 高分但无语境能力”和“LA-IQL 是 state-conditioned policy”的关键证据。
- **格式**：正文一段 + 附录一表；不要把它写成 contextual appropriateness 证明。

### B8. 满足 CHI 审核的数据与伦理声明

- **名称**：Minimum CHI-compliant data and ethics statement。
- **内容及解释**：如实说明课堂转录文本的来源类型、作者获得数据的方式与研究使用依据、伦理审查状态（如已批准、豁免、由原采集项目覆盖或不适用）、采用的去标识化措施，以及为何不公开原始转录。不得把未知情况写成已经获得同意或伦理批准。
- **获取方式**：优先向导师或数据提供方取得一段可引用的事实说明；现阶段不要求建立完整的数据治理档案。仍无法确认的非关键细节可概括为受数据提供方协议限制。
- **重要性及原因**：**P2-Submission，正式投稿前为 P0**。导师初稿可保留醒目的事实核实标记；提交前必须满足 CHI 对真实参与者数据的透明披露和风险说明要求，但不需要完成超出投稿范围的全面治理审计。
- **格式**：正文 Data/Method 与 Ethical Considerations 中各用一小段即可；除非模板或评审明确要求，不强制另设完整 Data Statement 或发布数据 manifest。

### B9. 统计报告一致性审计

- **名称**：Statistical consistency audit。
- **内容及解释**：统一统计单位、bootstrap seed、cluster 层级、percentile CI、p/q、比较方向和多重校正范围；说明 TD 表为何未校正或补充校正结果。
- **获取方式**：核对 paired CSV/JSON、Results ledger、图中数值和论文表格；逐项建立 claim--number 对照。
- **重要性及原因**：**P1**。当前 Direct--Candidate 使用 BH，而 TD 表多项检验未明确处理，容易被质疑选择性显著。
- **格式**：Evaluation Protocol 一段；表注注明 correction family；附录提供完整 comparison ledger。

### B10. 规则化定性案例

- **状态**：**最低 P0-Draft 版本已完成（2026-08-27）**。正文已按预先声明的确定性规则选入一个可追溯案例：在 30 个匹配单元中选择 Direct--Candidate 两步循环率差值最大者，并以模体率差值和字典序破局；入选课程 4873、生成种子 43、第 13--16 回合。案例同时呈现局部上下文、action、压缩后的 rationale 与 utterance，既展示 Direct 的 action recurrence，也保留 Candidate 第 15 回合可检查的局部 rationale--realization shift，并明确说明动作循环不等同于语义停滞或教学失败。扩展为 2--3 个规则化案例仍属 P1-Evidence。
- **名称**：Inspectable trajectory examples。
- **内容及解释**：从预先固定规则选出的 2--3 个相同 lesson/seed 片段，展示 expert、Direct、Candidate/no-TD 的 action sequence、rationale 和 utterance，包含成功、重复和 realization mismatch，而非只挑有利案例。
- **获取方式**：先冻结选例规则，例如最大 paired motif difference、典型 alignment--repetition disagreement、自动 consistency disagreement，再从 formal trajectories 导出。
- **重要性及原因**：**至少一个可检查案例为 P0-Draft；扩展到 2--3 个规则化案例为 P1-Evidence**。导师需要从实例判断 action mediation、控制分配和失败模式是否被论文准确表达，单靠 JSD/cycle 数值难以修改理论叙事。
- **格式**：导师初稿正文先放一个带来源的案例图或紧凑表；正式版本扩展规则化选例，完整轨迹放补充材料。

### B11. Related Work 与贡献定位补强

- **状态**：**已完成（2026-08-27）**。英文正文已重组为教学结构化 LLM 对话、示范驱动的交互策略学习、主动性与控制分配、教学对话评价与模拟有效性四条文献线，并已同步中文翻译；新增文献均已写入 `references.bib` 并通过编译。
- **名称**：HCI literature integration。
- **内容及解释**：补充 inspectable/controllable conversational agents、mixed initiative、strategy-mediated interaction、教育对话代理与 explanation/traceability 的直接比较；明确技术贡献是集成与动作层设计，而非新 IRL 目标。
- **获取方式**：在现有 Related Work 基础上建立 nearest-work comparison，逐项比较输入、显式动作层、离线数据、控制边界和评价对象。
- **重要性及原因**：**P0-Draft**。这是理论收口而非普通润色；当前稿仍容易被看作 NLP/RL 方法加 HCI framing，导师需要基于清晰的 nearest-work 边界判断贡献是否成立。
- **格式**：Related Work 增补 2--4 段；可选附录 comparison table。

### B12. 编译、可访问性与提交包清理

- **名称**：Submission hygiene。
- **内容及解释**：修复 overfull boxes，检查单栏图中文字、黑白/色盲可读性、`\Description{}`、PDF metadata 和匿名化；删除提交包中的示例 tex、示例图片、临时 aux/log/synctex 与无关模板文件。
- **获取方式**：在干净临时目录 `latexmk`；检查 log、`pdfinfo`、字体嵌入、压缩包文件清单和匿名关键词。
- **重要性及原因**：拆为 **B12a（P0-Draft）**：正文可编译、无缺图/缺表/未定义引用、图表可读；以及 **B12b（P2-Submission）**：匿名、metadata、source ZIP、supplement 和包体清理。错误格式或匿名泄漏可能 desk reject，但不应阻塞导师对理论主线的审阅。
- **格式**：导师初稿先提供稳定可读 PDF；投稿前生成最终单栏匿名 PDF、最小可编译 source ZIP 和独立 supplementary ZIP。

---

## 4. C 类：需要实验或新增评价得到

### C1. Full 与 no-TD 的独立训练重复

- **名称**：Training-seed replication。
- **内容及解释**：为 Full 和 matched no-TD 至少训练多个独立 seeds，并在相同 checkpoint-selection rule 下生成相同 test lessons。当前 42/43/44 是生成 seeds，不能代替训练重复。
- **获取方式**：冻结训练配置与 seeds，逐 seed 保存完整 training manifest、validation history、checkpoint hash，再进行 matched rollout 和层级/双层不确定性分析。
- **重要性及原因**：**P0（若保留一般化 TD 效果主张）**；若不补实验，则必须执行 B5 收缩为固定-checkpoint 发现。
- **格式**：正文主结果表按训练 seed 汇总；附录列每个训练 seed 与 generation seed 的结果。

### C2. 扩展上下文敏感性干预

- **名称**：Expanded context-dependence evaluation。
- **内容及解释**：把现有 50-state、单 deterministic donor 扩展到更多 held-out transitions，并加入多 donor、mask、paraphrase 或局部最小语义干预。
- **获取方式**：复用 `experiments/context_sensitivity/` pipeline，冻结干预生成规则和 primary endpoint 后运行；以 lesson 为 cluster 报告 CI。
- **重要性及原因**：**P1**。现有结果足以做 exploratory evidence，但不足以成为强 contextual sensitivity 结论。
- **格式**：正文一张核心表/图；附录放全部干预、模型和 per-lesson 结果。

### C3. Matched-temperature Direct--Candidate 对照

- **名称**：Decoding-only ablation。
- **内容及解释**：在相同 rationale temperature 下比较 Direct 与 Candidate，隔离 proposal constraint/decoding mode 的影响。
- **获取方式**：优先复用同 checkpoint、同 lessons、同 role temperature、同 generation seeds；只修改 action-selection mode。
- **重要性及原因**：**P1**。当前比较混入 0.0 vs. 0.6 rationale temperature，只能称 system-level contrast。
- **格式**：正文若作为机制结论则报告 matched result；否则保留当前描述性比较并把新实验放附录。

### C4. Rationale 与 consistency component ablations

- **名称**：No-rationale / no-consistency ablations。
- **内容及解释**：比较 full、no-rationale、no-consistency 和 rationale-conditioned no-TD，检验 rationale-conditioned dual-head 与 consistency loss 是否有独立价值。
- **获取方式**：冻结相同 backbone、数据、训练预算、checkpoint selection 与 direct decoding；至少运行核心训练 seeds。
- **重要性及原因**：**P1**。当前 G3 只证明 rationale 含 action-predictive information，不证明 rationale 或 consistency loss 改善策略。
- **格式**：正文消融表；附录提供训练与 per-seed 结果。

### C5. Rationale 因果干预

- **名称**：Rationale remove/paraphrase/counterfactual tests。
- **内容及解释**：对同一 state 删除、同义改写或替换为支持另一同角色动作的 rationale，测量 selected-action probability、flip rate 和 policy JSD。
- **获取方式**：复用 G3 计划和 checkpoint，冻结干预模板、替代动作选择与评价样本；避免根据结果挑选案例。
- **重要性及原因**：**P1**。若不完成，只能声称 simulatability/association，不能声称 rationale 是忠实或因果解释。
- **格式**：附录为主；若结果稳定，可在正文 G3 加一张简表。

### C6. 执行多视角知识建构 G4

- **状态（2026-08-29）**：**KG 主分析完成并已写入论文；多视角辅助验证尚未收口。** 已完成正式输入审计、250/250 图谱抽取、九系统汇总、七组配对统计、70/70 受控图谱抽取和 25/25（10%）重复抽取。正文当前只采用三个预指定 KG 端点。
- **名称**：G4 knowledge-construction evaluation。
- **内容及解释**：在冻结的 formal-100 完整轨迹上，使用带逐字 evidence 的知识图谱抽取作为当前论文证据，并以确定性图算法计算 UER$_{100}$、平均关系度和后期关系增长。辅助 LLM Judge、人工 KG 审计、受控破坏和重复抽取稳定性暂不作为正文证据，不得合成单一“课堂质量分”。
- **获取方式**：复用 `scripts/traj_rd/formal_100/` 的 Full Direct、Full Candidate、w/o-TD Direct 三组 `generation seeds 42--44 × 10 lessons`，以及冻结的 10 个 held-out expert transcripts；原则上不重新生成轨迹。按 `todo/G4_KNOWLEDGE_CONSTRUCTION_EVALUATION_PLAN.md` 完成输入 hash、controlled-corruption validation、KG extraction、动态图指标和 lesson-cluster 统计。
- **重要性及原因**：**KG 主分析已满足 P0-Draft**。以下剩余项为 P1-Evidence；正式投稿前需由导师决定是否恢复为正文证据。
- **格式**：正文当前保留三个 KG 主端点及一张九系统主表；growth curve、辅助 judge、受控门和审计材料完成后再决定进入附录或补充材料。

#### C6b. KG 人工语义审计

- **当前状态**：审计模板已有 180 项，但 `evaluator_id`、证据支持、类型/范围/关系正确性和 notes 均为 0/180。
- **获取方式**：至少由一名领域评审者完成分层抽样；正式投稿若声称图语义有效，应加入第二评审者与一致性统计。
- **重要性及原因**：**P1-Evidence；强 KG 有效性主张下为 P0-Submission**。当前 100% acceptance 仅是机器 schema 与证据 ID 校验，不能替代语义正确性。

#### C6c. KG 稳定性与受控门修复

- **当前状态**：10% 重复抽取覆盖门通过，但 node-name F1 为 0.681、canonical-edge F1 为 0.352；UER$_{100}$、平均关系度和后期增长的平均绝对差分别为 5.463、0.259 和 0.057。五个非 Judge 受控门中四个通过；`loop_duplicate_relation_evidence_increases` 失败（差值 $-0.0331$）。
- **获取方式**：优先改进实体规范化、关系合并和 loop proxy；冻结修订版后只重跑稳定性样本与对应受控项，不覆盖当前正式结果。
- **重要性及原因**：**P1-Evidence**。节点层面尚可，但精确边稳定性偏低；最终稿中的边级解释必须保守或由人工审计支撑。

#### C6d. LLM Judge 协议重设计

- **当前状态**：现有成对 Judge 已完成数据调用，但存在明显 A/B 位置偏置；冻结 order-consistency 目标 0.80 未达到。为生成导师初稿报告曾临时使用 0.05 门限，该门限不得作为最终论文标准。relation-corruption 对照在现有五维 rubric 下全部判平，原因是局部事实/关系词替换没有破坏 rubric 所测的互动连贯性。
- **获取方式**：改为单轨迹独立五维评分，再在相同 lesson/seed 上离线配对；以重复评分 MAE、ICC 或 weighted kappa 替代顺序一致性。若继续 relation corruption，应构造真正破坏跨话轮 uptake/coherence 的矛盾，而不是只修改数字和局部词语。
- **重要性及原因**：**P2-Draft、P1-Submission**。当前论文不依赖 Judge，因此不阻塞导师初稿；若最终将其作为辅助证据，必须先冻结新协议并重新运行。

#### C6e. Growth curve 与 KG 定性案例

- **当前状态**：动态图端点已计算，但正文尚无 growth curve，也没有按预注册规则选择的 KG 案例。
- **获取方式**：从已有图谱产物生成按归一化话轮进度的实体/关系增长曲线；先冻结选例规则，再导出 1--2 个可核查案例。
- **重要性及原因**：**P1-Evidence**。用于解释聚合端点，不阻塞当前 KG-only 初稿。

### C6a. 原 action--utterance 评测的选择性保留

- **保留**：冻结轨迹、数据划分、label mapping、训练/预测脚本、classifier audit、confusion matrix、盲化条目、rubric、随机化 manifest，以及不依赖分类器训练的局部冗余、完全重复和规则违规指标。
- **暂不保留为论文证据**：Direct 1.30%、Candidate 2.63%、w/o-TD 1.01%、一致性 Macro-F1、对应 CI/$p$/$q$ 和“Candidate 改善 realization”的结论。
- **恢复条件**：只有完整训练协议完成，且在冻结 held-out expert、类别覆盖、label mapping、受控错配和生成域稳定性 gates 上通过后，才以新版本号作为 secondary action--utterance diagnostic 重新进入附录；旧数值永久标记为 preliminary invalidated run，不与新结果合并。
- **优先级**：**P2**。不阻塞新 G4；距离 DDL 较近时，先完成 KG 主分析和论文闭环。

### C7. END suppression 敏感性分析

- **名称**：Minimum-horizon sensitivity。
- **内容及解释**：比较 `END` minimum step 50 与不抑制/更自然 stopping rule，检查 cycle、motif、JSD 与终止率是否由强制最短长度驱动。
- **获取方式**：在相同 checkpoint、lessons 和 generation seeds 下仅改变 END rule；提前冻结比较指标。
- **重要性及原因**：**P1**。当前论文把终止行为解释为 policy outcome，但前 50 步不能终止，可能影响长程重复和稳定性解释。
- **格式**：正文 Limitations 提及；附录敏感性表，若影响主结论则移入正文。

### C8. Rationale 人工语义审计

- **名称**：Annotation quality audit。
- **内容及解释**：现有 `length-only-v1` 只检查表面质量。需要抽样评价 rationale 是否与 state/action 相符、是否包含臆测、是否泄漏标签以及是否具有模板偏差。
- **获取方式**：按 lesson/action frequency 分层抽样，至少双人独立评分一部分样本，报告 rubric 和 agreement；若无法正式人评，至少做作者审计并清楚标为非独立审计。
- **重要性及原因**：**P1**。错误 rationale 会同时污染训练目标和 G3 simulatability 结论。
- **格式**：附录 audit table；正文一句话报告抽样规模与主要错误率。

---

## 5. D 类：需要人工或外部确认

### D1. CHI 投稿所需的最低数据伦理确认

- **名称**：Minimum ethics confirmation for CHI submission。
- **最低必须确认**：数据并非未经许可取得；当前研究可以使用这些课堂转录；论文能够准确陈述伦理审查/豁免/原项目覆盖状态；输入模型前已移除或替换直接身份信息；原始转录不会随论文公开。若涉及未成年人，应确认同意与数据使用责任由原采集项目或数据提供方承担，并避免作出无法证明的具体程序性声称。
- **不再作为硬门槛**：正式数据集名称、完整采集机构档案、逐参与者同意文本、原始 IRB 文件副本、可发布派生数据范围和独立匿名化审计。只有计划公开数据或评审要求补充时再追查。
- **获取方式**：向导师或数据提供方取得书面确认或可记录的事实摘要即可；无需为当前论文重建原始采集项目的全部伦理档案。
- **重要性及原因**：**P2-Submission，正式投稿前为 P0**。这是 CHI 审核的最低合规底线；导师初稿阶段先明确待确认事实和禁止臆测的边界，超过该底线的治理材料属于增强项。
- **格式**：正文给出简洁、真实且不过度承诺的 Data/Ethics 声明；必要时在附录补充限制，不要求发布 manifest。

### D2. 主 checkpoint 的历史训练 provenance

- **名称**：`sft_stage3/final` 与 `sft_stage3_woTD/final` 训练审计。
- **已确认并写入论文**：三阶段 LoRA 训练；每阶段 2 epochs；Stage 1/2/3 学习率为 `1e-4/1e-4/5e-5`；物理 batch size 4、gradient accumulation 1、有效 batch 4；max length 512；training seed 42；grad clip 1.0；各阶段 policy、consistency、LM-action、结构 token、recovery 与 teacher/self-generated 权重。Full 与 no-TD 的已恢复配置仅在 Stage 3 TD loss weight 上不同，分别为 1 与 0。配置注释中的 micro-batch 1 × accumulation 4 以及 Stage 3 名称中的 “+ TD” 均为过时文字，以实际参数为准。
- **优先确认**：optimizer 类型和 weight decay；scheduler/warm-up；LoRA rank/alpha/dropout/target modules；数值精度；base model/tokenizer revision；checkpoint selection rule。这些信息若无法恢复，应在附录中明确标为 unknown，而不是用当前默认值代替。
- **非阻塞增强项**：betas/epsilon、stage 间 optimizer state、gradient checkpointing、精确 optimizer steps、四个新增 token 的 embedding 初始化、保存/验证频率、完整 deterministic 设置、历史代码 commit、各阶段 checkpoint hash 与完整训练日志。
- **获取方式**：优先查现有 checkpoint metadata、训练配置和实验笔记；只有在方便且可靠时再追查 stdout/stderr、shell history 或平台记录。可选生成 `training_manifest.json`，不要求恢复到逐 bit 重放。
- **重要性及原因**：**P1**。现有核心配置已经支持“Stage 3 TD weight 1 vs. 0”的受限单变量描述；剩余字段用于增强可信度和复用性，不再作为论文主张成立的硬性前提。
- **格式**：附录保留主训练配置表和 unknown 标记；machine-readable manifest 与 checkpoint hash 为可选补充材料。

### D3. 计算硬件、时长与成本

- **名称**：Compute and cost statement。
- **内容及解释**：确认 GPU 型号/数量、显存、训练耗时、推理/API 调用量和大致成本。现有目录只能证明使用 CUDA 12.8 环境，不能恢复主训练硬件与总耗时。
- **获取方式**：查询服务器调度日志、`nvidia-smi` 记录、云账单、API usage 和作者实验日志。
- **重要性及原因**：**P1**。帮助评审判断方法资源需求与可复现性，尤其 role model 使用外部 API。
- **格式**：附录 Compute 表；正文 Implementation Summary 可给总 GPU-hours/API calls。

### D4. DeepSeek API 版本与可重放性

- **名称**：External model snapshot。
- **内容及解释**：`deepseek-chat` 是可漂移别名，需要确认 2026-08-09 rationale rewrite 与 formal rollout 时对应的具体模型版本/API revision、调用日期和 seed 支持行为。
- **获取方式**：查询 API 响应 metadata、平台公告、调用日志或账单；若无法恢复，明确报告 alias、日期和不可完全重放限制。
- **重要性及原因**：**P1**。外部模型漂移可能使语言实现和 rationale annotation 无法精确复现。
- **格式**：附录 External Models 表；Limitations 中说明版本漂移。

### D5. 投稿级匿名与学术合规确认

- **名称**：Submission compliance sign-off。
- **内容及解释**：确认作者列表/顺序、第三人称自引、相关预印本、并行投稿、数据/代码匿名链接、PDF metadata、补充材料路径和所有作者的 review responsibility。
- **获取方式**：由全体作者在最终冻结前逐项签字确认；自动扫描只能辅助，不能代替作者确认。
- **重要性及原因**：**P0**。匿名泄漏、未披露相关稿件或投稿责任问题可能直接 desk reject。
- **格式**：内部 submission checklist；论文中只保留必要的匿名化披露。

---

## 6. 推荐执行顺序

### 6.1 P0-Draft：导师初稿冻结门槛

- [x] 完成全文 claim--evidence 审计：已逐句核对 Abstract、Problem、Contributions、RQ1--RQ4、Results、Discussion、Conclusion、Limitations 和附录中的主张层级，并同步英文主稿、中文翻译与对照表。
- [x] 完成 B6a 与 B6b-KG：新 RQ4 的理论定义、KG 方法、统计单位、三个主端点、九系统主表、配对结果、结论和限制均已同步至英文主稿与中文翻译；正文不再保留 RQ4 数值占位符。
- [x] 完成 B11：已补齐最邻近 HCI/NLP/教育对话工作，并明确 action mediation、inspectability、control allocation、自动评价与模拟有效性的贡献边界。
- [x] 完成 B10 最低版本：正文已有一个按冻结规则选择、可追溯到课程 4873／生成种子 43／第 13--16 回合的轨迹案例，同时展示 action、rationale、utterance 及 action-recurrence 解释边界。
- [ ] 完成 B12a：主稿可稳定编译，无缺图、缺表、undefined reference/citation 或阻碍阅读的版面问题。
- [x] 检查旧 G4-v1 未完成分类器的数值、显著性和系统排名已全部从主论证移除；正文仅保留其未完成及排除说明。
- [x] 完成 B1：已切换为 CHI 2027 单栏匿名审稿格式。
- [x] 完成 A1--A6、A8--A10 的证据核对并落稿。
- [x] B3 最低要求已完成：核心训练配置已写入，无法恢复的字段透明标记。
- [x] 完成 B5、B7、B9：推断边界、上下文干预和统计单位已写明。

达到以上门槛后，稿件即定义为“可交导师修改的理论闭环初稿”。A7、C6b--C6e、完整伦理确认和提交包不阻塞这一里程碑。

### 6.2 P1-Evidence：导师确认主线后的证据补全

1. KG 主表与正文闭环已完成；下一步由导师决定是否继续 C6b--C6e（人工审计、稳定性/受控门、独立单轨迹 Judge、growth curve 与 KG 案例）。
2. 根据导师对核心主张的要求决定 A7、C1、C2、C3：只有保留对应强主张时才升级为必做。
3. 扩展 B10 为 2--3 个按冻结规则选择的定性案例。
4. 保持 TD 为 fixed-checkpoint finding，除非 C1 独立训练重复完成；保持 Direct--Candidate 为 system-level contrast，除非 C3 完成。

### 6.3 P2-Submission：正式投稿前

- [ ] 完成 B8/D1：取得最低数据使用、伦理状态和去标识化事实确认，并写入 Data/Ethics。
- [ ] 完成 D3--D5：硬件/成本、外部 API 版本、匿名与学术合规确认。
- [ ] 完成 B12b：最终匿名 PDF、source ZIP、supplement、metadata 和文件清单清理。
- [ ] 完成 A7 或在正文明确其不进入正式主比较；核对全部模型、数据、checkpoint 和 seed provenance。
- [ ] 确认每个最终核心主张均有已完成证据，不保留内部占位符。

### 6.4 P3-Enhancement：不阻塞当前主线

- C4/C5：在 rationale 明确限定为 supervised textual intermediate 时可延后。
- C7：仅在需要证明长程结果不依赖 END suppression 时升级。
- C8：用于增强 rationale 语义可信度，不支持当前因果 faithfulness 主张。
- 正式用户研究不是当前初稿的必要条件；没有伦理和招募条件时，不应仓促开展。

---

## 7. 完成定义

### 7.1 可交导师修改的初稿

满足以下条件即可交导师，不等待新增实验：

1. 理论问题、方法设计、四个 RQ 和贡献声明形成单一一致主线。
2. 每个 RQ 均有对应的方法、评价、Results 位置、讨论和限制；未完成结果以内部占位符明确标识。
3. Abstract 和 Conclusion 只总结已有证据，不把计划实验写成结论。
4. Related Work 足以判断与最邻近 HCI/NLP/RL 工作的差异。
5. 至少一个可检查轨迹案例帮助理解显式动作层和控制分配。
6. 论文可稳定编译，图表、交叉引用和引用完整，不存在明显结构空洞。

### 7.2 可提交成稿

只有同时满足以下条件，才把论文标为“可提交成稿”：

1. 单栏匿名格式正确，干净环境可重复编译，无 undefined reference/citation 和实质性 overflow。
2. 所有模型、数据、checkpoint、训练 seed、生成 seed 和外部 API 均有明确 provenance。
3. 每个核心主张能指向正文中的直接证据，负结果与混杂没有被隐藏。
4. Full/no-TD 的推断范围与训练重复数量一致；Direct/Candidate 不被写成未完成的单因素消融。
5. RQ4 的措辞与实际 G4 证据强度一致。
6. 已确认数据可用于本研究、伦理审查状态和基本去标识化措施，并明确原始转录不公开；无需在投稿前恢复完整原始伦理档案。
7. 主文自包含，关键实现与核心结果不依赖评审主动查看附录。
8. PDF、source ZIP、supplement、匿名链接和投稿系统元数据通过最终合规检查。
