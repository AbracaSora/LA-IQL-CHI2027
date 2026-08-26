# CHI 2027 论文成稿缺口与执行清单

更新日期：2026-08-26

适用主稿：`sigconf-authordraft.tex`

实验工作目录：`../../LA-IQL-Test/`

## 1. 使用说明

本文档把当前论文距离可模拟评审稿/正式投稿稿的缺口分为四类：

1. **A：实验或材料已经完成，但尚未写入论文**：原则上不需要重新运行模型，只需核实来源并落稿。
2. **B：当前即可完成**：主要是写作、格式、审计和已有材料整理，不依赖新增实验结果。
3. **C：需要实验得到**：必须运行新实验、重新统计或完成人工评价后才能填写。
4. **D：需要人工或外部确认**：无法仅从现有代码和产物可靠恢复，需要作者、数据提供方或伦理/平台记录确认。

重要性等级：

- **P0（阻塞）**：不完成可能导致 desk reject、核心结论不成立或评审无法判断实验是否公平。
- **P1（重要）**：显著影响正确性、可复现性、说服力或修改轮次。
- **P2（增强）**：不一定阻塞投稿，但能减少质疑、提高完整度或便于复现。

“格式”指最终应在论文或补充材料中采用的呈现形式，而不是文件格式。

### 1.1 当前落稿状态（2026-08-26）

- **已写入并完成**：A1--A6、A8--A10；B1、B2、B4--B7、B9。
- **已部分写入**：A7（BC 训练 metadata 已进入附录，但尚未进入正式 horizon-100 主比较）；B3（复现表已建立，主 checkpoint 历史训练参数仍受 D2 阻塞）；B12（已转换单栏匿名格式并通过编译，仍需最终 source ZIP 清理）。
- **仍可继续但本轮未完成**：B10（规则化定性案例）、B11（Related Work 增补）。
- **受外部证据阻塞**：B8 必须与 D1 一起完成，不能仅凭代码目录推断数据许可、同意和去标识化流程。
- **无需新增实验但已明确披露缺口**：D2 的不可恢复字段已在附录列明，避免用当前脚本默认值反推。

本轮写入位置：正文的 Abstract、Method、Experimental Design、Results、Discussion、Conclusion、Limitations，以及附录的 Implementation and Reproducibility 与 Context-Sensitivity Intervention。

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
- **重要性及原因**：**P0**。当前论文主要展示统计控制与 no-TD，而完整同数据 learned BC 能帮助评审判断 LA-IQL 是否超过局部 imitation。
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

- **名称**：完整复现表。
- **内容及解释**：整理 optimizer、batch、epochs、LoRA、loss weights、context windows、prompt version、data hashes、software versions、checkpoint provenance 和运行入口。
- **获取方式**：先填已被 artifacts 证明的值；主 checkpoint 缺失参数标为“待历史日志核实”，不能直接使用当前 `sft.py` 默认配置。
- **重要性及原因**：**P0**。当前方法段不足以复现，也无法审计 full/no-TD 是否真正单变量。
- **格式**：附录 1--2 张表；prompt 全文放补充材料而非正文。

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

### B6. 重写 RQ4 和 realization 结论

- **名称**：Realization-gap framing。
- **内容及解释**：当前 consistency accuracy 仅 1.30%--2.63%，且分类器本身较弱、无人评。应把 RQ4 从“contextual appropriateness”收缩为自动 realization screening，并将结果解释为可能的 action--utterance gap，而不是 Candidate 已可靠改善实现质量。
- **获取方式**：修改 RQ4、Evaluation Metrics、摘要、Results、Discussion 和 Conclusion；保持与 G4-v1 证据一致。
- **重要性及原因**：**P0**。现有证据不能支持课堂适切性、自然度或教育质量结论。
- **格式**：正文问题定义和结果段；附录保留完整弱分类器指标及限制。

### B7. 将上下文干预纳入论文

- **名称**：Context-sensitivity subsection。
- **内容及解释**：使用 A8 的既有结果补充“模型是否读取对话语义”，同时保留 Macro-F1 不显著和单 donor/50-state 的限制。
- **获取方式**：从现有报告提取正式英文表述、protocol 和表格；核对数值与 machine-readable artifacts。
- **重要性及原因**：**P0**。这是连接“Markov 高分但无语境能力”和“LA-IQL 是 state-conditioned policy”的关键证据。
- **格式**：正文一段 + 附录一表；不要把它写成 contextual appropriateness 证明。

### B8. 数据、未成年人和标注伦理写实化

- **名称**：Actual data-governance statement。
- **内容及解释**：把当前 “should follow consent/license” 的原则性表述改成作者实际采取的措施；无法确认的部分明确写为数据提供方约束或不公开原因。
- **获取方式**：先从数据说明、原论文和作者记录整理；涉及授权/同意的缺口转入 D1 确认。
- **重要性及原因**：**P0**。课堂数据涉及未成年人，泛化伦理模板不足以回答真实来源与使用权限。
- **格式**：正文 Data and Ethics 各一段；附录给数据表、去标识化和访问条件。

### B9. 统计报告一致性审计

- **名称**：Statistical consistency audit。
- **内容及解释**：统一统计单位、bootstrap seed、cluster 层级、percentile CI、p/q、比较方向和多重校正范围；说明 TD 表为何未校正或补充校正结果。
- **获取方式**：核对 paired CSV/JSON、Results ledger、图中数值和论文表格；逐项建立 claim--number 对照。
- **重要性及原因**：**P1**。当前 Direct--Candidate 使用 BH，而 TD 表多项检验未明确处理，容易被质疑选择性显著。
- **格式**：Evaluation Protocol 一段；表注注明 correction family；附录提供完整 comparison ledger。

### B10. 规则化定性案例

- **名称**：Inspectable trajectory examples。
- **内容及解释**：从预先固定规则选出的 2--3 个相同 lesson/seed 片段，展示 expert、Direct、Candidate/no-TD 的 action sequence、rationale 和 utterance，包含成功、重复和 realization mismatch，而非只挑有利案例。
- **获取方式**：先冻结选例规则，例如最大 paired motif difference、典型 alignment--repetition disagreement、自动 consistency disagreement，再从 formal trajectories 导出。
- **重要性及原因**：**P1**。CHI 读者需要看到指标对应的实际交互行为，单靠 JSD/cycle 数值难以理解设计意义。
- **格式**：正文一张案例图或紧凑表；完整轨迹放补充材料。

### B11. Related Work 与贡献定位补强

- **名称**：HCI literature integration。
- **内容及解释**：补充 inspectable/controllable conversational agents、mixed initiative、strategy-mediated interaction、教育对话代理与 explanation/traceability 的直接比较；明确技术贡献是集成与动作层设计，而非新 IRL 目标。
- **获取方式**：在现有 Related Work 基础上建立 nearest-work comparison，逐项比较输入、显式动作层、离线数据、控制边界和评价对象。
- **重要性及原因**：**P1**。当前稿仍容易被看作 NLP/RL 方法加 HCI framing，CHI 2027 明确要求清晰的 HCI 贡献。
- **格式**：Related Work 增补 2--4 段；可选附录 comparison table。

### B12. 编译、可访问性与提交包清理

- **名称**：Submission hygiene。
- **内容及解释**：修复 overfull boxes，检查单栏图中文字、黑白/色盲可读性、`\Description{}`、PDF metadata 和匿名化；删除提交包中的示例 tex、示例图片、临时 aux/log/synctex 与无关模板文件。
- **获取方式**：在干净临时目录 `latexmk`；检查 log、`pdfinfo`、字体嵌入、压缩包文件清单和匿名关键词。
- **重要性及原因**：**P0**（格式/匿名/编译）与 **P2**（包体清理）。错误格式或匿名泄漏可能 desk reject。
- **格式**：最终单栏 PDF + 最小可编译 source ZIP + 独立 supplementary ZIP。

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

### C6. 更可信的 action--utterance realization 评价

- **名称**：G4 realization evaluation。
- **内容及解释**：当前自动分类器准确率极低。合规路径包括：改进并审计 independent classifier，或在伦理条件满足时完成匿名、随机、盲法的人类 action-support/classroom-appropriateness 判断。
- **获取方式**：自动路径需冻结新 evaluator 并报告其 held-out expert performance；人评路径需先确认伦理、rubric、样本量、评审背景、一致性和 lesson-cluster 统计。
- **重要性及原因**：**P0（若保留 contextual appropriateness/realization improvement 主张）**；若不补，则执行 B6，将其降级为失败/风险发现。
- **格式**：正文主端点和 CI；附录放 evaluator performance、rubric、agreement、抽样与全部次级指标。

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

### D1. 数据名称、许可、同意与去标识化

- **名称**：Dataset governance confirmation。
- **内容及解释**：需要确认数据集正式名称、采集机构、语言/地区、访问许可、未成年人及教师同意条件、研究用途授权、去标识化流程和是否可发布派生数据。
- **获取方式**：查询数据提供协议、原始项目记录、IRB/伦理豁免文件和数据提供方；不能仅根据目录内容推断。
- **重要性及原因**：**P0**。涉及真实课堂和未成年人，来源与授权不清可能阻塞投稿或数据发布。
- **格式**：正文 Data 与 Ethical Considerations；附录 Data Statement；必要时 supplementary 只发布不可逆匿名化的 manifest。

### D2. 主 checkpoint 的历史训练 provenance

- **名称**：`sft_stage3/final` 与 `sft_stage3_woTD/final` 训练审计。
- **内容及解释**：恢复实际 optimizer、LR、epochs、batch、LoRA、loss weights、teacher/self-generated ratio、训练 seed、初始化 checkpoint、代码版本和 checkpoint selection rule。当前 `sft.py` 已重构，不能证明旧 checkpoint 使用了现有默认值。
- **获取方式**：查服务器 stdout/stderr、shell history、旧代码快照、checkpoint epoch metadata、训练平台任务记录或作者实验笔记；恢复后生成不可变 `training_manifest.json`。
- **重要性及原因**：**P0**。这是完整 Implementation 表目前最大的证据缺口，也决定 no-TD 是否真是单变量消融。
- **格式**：附录主训练配置表；补充材料提供 machine-readable manifest 与 checkpoint hash。

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

### 6.1 模拟评审稿最低冻结门槛

- [x] 完成 B1：已切换为 CHI 2027 单栏匿名审稿格式。
- [x] 完成 A1--A6、A8--A10 的证据核对并落稿。
- [ ] A7 部分完成：BC 训练 metadata 已写入附录；正式 trajectory comparison 尚未完成。
- [x] 完成 B2、B4--B7：Implementation、系统差异、seed 边界、RQ4 和上下文干预。
- [ ] B3 部分完成：复现表已建立；D2 所列历史训练字段仍待恢复。
- [ ] 完成 B8、D1：实际数据治理表述至少达到可审计状态。
- [x] 完成 B9：统计单位、多重校正与 fixed-checkpoint 推断边界已写明。
- [ ] B12 部分完成：单栏转换与编译复核已完成；最终提交包清理仍待冻结时执行。
- [x] 对 D2 无法恢复的参数显式标记，未由当前脚本默认值反推。

达到以上门槛后，稿件适合进入一次真正关注贡献和证据的模拟评审。

### 6.2 正式投稿主张分岔

**路线一：不新增昂贵实验，收缩主张。**

- 执行 B5、B6，把 TD 限定为固定-checkpoint finding，把 G4 降级为 realization risk。
- 将现有 50-state context test 作为 exploratory evidence。
- 不声称训练稳定性、课堂适切性、rationale faithfulness 或教育效果。

**路线二：保留较强方法主张。**

- 优先完成 C1（独立训练 seeds）、C2（扩展 context test）和 C6（可信 realization 评价）。
- 根据篇幅和预算选择 C3/C4/C5；C7 用于确认长程结论不依赖 END suppression。

### 6.3 建议暂不阻塞投稿的增强项

- C3 在 Candidate 仅作为描述性探索时可延后。
- C4/C5 在明确把 rationale 限定为 supervised textual intermediate 时可延后。
- 正式用户研究不是当前成稿的必要条件；没有伦理和招募条件时，不应仓促开展。

---

## 7. 成稿完成定义

只有同时满足以下条件，才把论文标为“可提交成稿”：

1. 单栏匿名格式正确，干净环境可重复编译，无 undefined reference/citation 和实质性 overflow。
2. 所有模型、数据、checkpoint、训练 seed、生成 seed 和外部 API 均有明确 provenance。
3. 每个核心主张能指向正文中的直接证据，负结果与混杂没有被隐藏。
4. Full/no-TD 的推断范围与训练重复数量一致；Direct/Candidate 不被写成未完成的单因素消融。
5. RQ4 的措辞与实际 G4 证据强度一致。
6. 数据许可、未成年人隐私、去标识化和可发布范围已经确认。
7. 主文自包含，关键实现与核心结果不依赖评审主动查看附录。
8. PDF、source ZIP、supplement、匿名链接和投稿系统元数据通过最终合规检查。
