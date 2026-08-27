# Claim--Evidence 对照表

更新日期：2026-08-27  
适用主稿：`../sigconf-authordraft.tex`  
当前用途：形成可交导师修改的理论闭环初稿

## 使用规则

- **已支持**：可以进入 Abstract、Results、Discussion 和 Conclusion，但措辞不得超过“允许表述”。
- **有限支持**：可以报告为固定 checkpoint、描述性对比或探索性诊断，必须同时写明限制。
- **结构性主张**：由方法设计或系统边界直接成立，不等于用户价值或经验效果已经得到验证。
- **待证据**：只能出现在 RQ、Method、Evaluation Plan、Limitations 或醒目的内部占位符中，不能写成结果。
- **已失效**：不得作为论文证据；仅在审计记录中保留失效原因。

## 主表

| ID | 对应问题 | 核心主张 | 直接证据 | 稿件位置 | 状态/强度 | 当前允许表述 | 禁止或必须收缩的表述 | 下一步 |
|---|---|---|---|---|---|---|---|---|
| C0 | 总体贡献 | 本文提出动作中介的研究范式，并以 LA-IQL 将其操作化：开放式交互被分解为可读 rationale、显式动作选择和独立语言实现，策略在固定人类示范上离线学习。 | 方法形式化、31 动作空间、双头模型、Direct/Candidate 推理边界，以及分别评价对齐、时间组织、上下文使用、控制分配与实现的协议；这是设计与实现事实。 | Introduction、Contributions、Method、Discussion、Conclusion。 | **结构性主张，已支持** | “我们提出 action-mediated research paradigm，并用 rationale-conditioned 离线语言策略连接真实人类轨迹、显式策略学习和独立语言实现；该边界使多种行为属性可以分别研究。” | “这是首个显式动作对话系统”“该结构天然改善交互质量、可用性、可解释性或学习效果。” | 保持范式贡献与经验效果分离；Introduction、Contributions、Method 和 Conclusion 统一使用 paradigm--instantiation--evaluation 三层结构。 |
| R1-1 | RQ1 | 局部专家模式对齐不足以证明策略具有上下文敏感性。 | 不读取对话文本的一阶 Markov control 在 paired bigram JSD、pooled bigram JSD 和 transition-row JSD 上达到最优或更优局部结果。 | Baselines：约 627--637 行；Results：约 825--845 行；Discussion 5.1。 | **已支持** | “Aggregate/local human-pattern similarity alone is insufficient evidence of context-sensitive interaction.” | “Markov control 比学习策略更智能”或“G2 衡量上下文适切性”。 | 无需新实验；继续把 Markov 解释为 metric-matched diagnostic control。 |
| R1-2 | RQ1 | 学习系统不存在跨 G1/G2 的单一全面优胜者，而呈现多样性、重复与专家对齐的差异化表现。 | G1/G2 主表和完整 G1 表；Direct、Candidate 与控制方法在不同指标上排序不同。 | Tables 2--3；Results 约 825--903 行；Appendix Full G1。 | **已支持，但仅限所报告指标** | “The systems exhibit different behavioral profiles/trade-offs on diversity, recurrence, and local expert-pattern alignment.” | “LA-IQL 全面优于全部 baseline”或“更像人类课堂”。 | 在 Abstract/Conclusion 避免使用无条件的 outperform。 |
| R1-3 | RQ1/上下文诊断 | 主 Full 策略的分布会响应动作历史之外的对话文本。 | 冻结 50-state 干预：expert-action probability 下降 0.0767；60% argmax flip；平均 JSD 0.2957；Macro-F1 区间跨零。 | Results：约 847--860 行；Appendix Context-Sensitivity Intervention。 | **有限支持；探索性** | “The fixed policy distribution responds to dialogue text beyond the preserved action history.” | “模型理解了上下文”“选择在课堂中是适当的”或“证明了语境能力”。 | 初稿保留结果与限制；扩展样本/多 donor 属 P1-Evidence。 |
| R2-1 | RQ2：TD | 对当前两个固定 checkpoint，含 TD 的 Direct 轨迹呈现更少的两步循环和重复模体。 | Cycle-2：0.1708 vs. 0.2607；motif：0.3957 vs. 0.5379；lesson-cluster bootstrap 均 $p=.0002$。 | Abstract；Results：约 778--796 行；Table 4；Discussion 5.2。 | **有限支持；固定 checkpoint 对比** | “For the evaluated fixed checkpoints, the TD-associated difference is concentrated in recurrent sequence organization.” | “TD 普遍/显著稳定训练”“TD 在不同训练 seed 下可靠改善长程行为”。 | 保持 fixed-checkpoint 限定；只有完成 C1 独立训练重复后才能外推训练目标效应。 |
| R2-2 | RQ2：TD 与 G2 | 当前 TD/no-TD checkpoint 的局部专家模式对齐没有可靠差异。 | Paired bigram JSD：0.0827 vs. 0.0835，差值 $-0.0007$，CI 跨零，$p=.8281$；transition JSD 同样不可区分。 | Results：约 789--796 行；Table 4；Discussion 5.2。 | **已支持的负结果，仍受固定 checkpoint 限制** | “The observed TD-associated difference concerns recurrence rather than local imitation fidelity.” | “TD 提高专家模式对齐”或“TD 对 G2 完全没有影响”。 | 与 R2-1 联合回答 RQ2，不单独把 G2 写成完整长程质量指标。 |
| R2-3 | RQ2：控制分配 | Direct 更接近留出专家局部动作分布，而 Candidate 重复更少，形成 alignment--repetition trade-off。 | Direct/Candidate paired bigram JSD：0.0827/0.1059；Cycle-2：0.1708/0.0488；motif：0.3957/0.1413；30 个配对 seed--lesson 单元。 | Abstract；Results：约 862--903 行；Table 5；Discussion 5.3。 | **有限支持；描述性 system-level contrast** | “Direct and Candidate expose a descriptive alignment--repetition trade-off under the completed configurations.” | “Candidate re-ranking 因果地减少重复”或“Direct 解码因果地提高 G2”。 | 明确两配置同时改变 rationale temperature（0.0/0.6），且比较是在查看留出结果后提升为重点；C3 后才能作解码归因。 |
| R3-1 | RQ3 | 遮蔽显式标签后，生成 rationale 仍包含与所选动作有关的可预测信息。 | G3-v2：Direct rationale-only Macro-F1 0.3986、state-only 0.0159、增量 simulatability 0.3885；Candidate 和 no-TD 也报告相同协议结果；shuffle controls 较低。 | Results：约 904--919 行；Appendix G3-v2 table。 | **已支持的关联/可模拟性诊断** | “Masked rationales contain action-predictive information beyond the state-only evaluator and explicit label strings.” | “Rationale 因果决定动作”“rationale 是忠实解释”或“提升了策略性能”。 | 初稿保留 association/simulatability 边界；C4/C5/C8 属后续增强。 |
| R3-2 | RQ3 | 当前证据不能建立 rationale 的因果忠实性、语义正确性或用户可理解性。 | 当前只有独立预测器和 shuffle controls；remove/paraphrase/counterfactual 与人工语义审计未完成。 | Results 约 904--919 行；Limitations；Evaluation Details。 | **边界已确认** | “Rationales are supervised textual intermediates and should not be interpreted as faithful causal explanations.” | “可解释决策”“忠实推理链”“用户可验证解释”。 | 在 Abstract、Contributions 和 Discussion 全文维持这一限制。 |
| R4-1 | RQ4 | 不同动作控制分配下，长程生成对话可能呈现不同的知识引入、关联与发展模式。 | 当前已有研究问题、系统控制边界、冻结评价计划、统计单位、三个主端点和 Results 骨架；尚无正式 G4 系统级结果。 | RQ4；Evaluation Metrics；Results 的 pending 段；`G4_KNOWLEDGE_CONSTRUCTION_EVALUATION_PLAN.md`。 | **待证据；结构已完成** | 初稿中仅作为 RQ、操作化方法和 Results 内部占位符；明确“no G4 system-level inference is reported”。 | 任何关于哪个系统知识建构更好、知识更丰富、教学质量更高、事实更正确或学习效果更好的结论。 | B6a 已完成；导师确认后执行 C6，完成质量门控与数值分析后再同步 Abstract/Results/Discussion/Conclusion。 |
| R4-2 | RQ4/语言实现边界 | 现有规则检查没有发现完全重复或两类严重违规，但不能衡量语言实现质量或课堂适切性。 | Direct、Candidate、w/o-TD Direct 的规则检查为零；局部 trigram redundancy 无可靠差异。 | Results：约 921--931 行；Appendix Judgment Status。 | **有限支持；窄范围负检查** | “The retained rule-based diagnostics did not detect these specific violations.” | “话语实现可靠”“课堂适切”“安全/自然/事实正确”。 | 只作为 secondary diagnostic；不得替代新 G4 或人工评价。 |
| INV-1 | 旧 G4-v1 | 原 action--utterance classifier 的一致率、Macro-F1、CI、$p/q$ 和系统排名不能作为证据。 | 分类器未完成训练协议；主稿已移除 Direct 1.30%、Candidate 2.63%、w/o-TD 1.01% 等初步结果。 | Evaluation Metrics：约 667--679 行；Results：约 921--931 行；Appendix Judgment Status。 | **已失效** | 只能说明该评测为何被排除，以及保留了哪些独立规则诊断。 | 恢复旧数值、称 Candidate 改善 realization，或把旧结果并入新 G4。 | 全文与图表继续保持删除；只有新 evaluator 通过冻结 gates 后以新版本号重新进入附录。 |
| BND-1 | 全文统计边界 | 三个 42--44 是生成 seed，共用每个条件的单一训练 checkpoint；现有 bootstrap 不包含训练 seed 不确定性。 | Formal trajectory config、workflow 和论文统计协议。 | Experimental Design：约 681--699 行；Results：约 760--776 行；Implementation tables。 | **已支持的方法边界** | “Inference covers held-out lesson and generation variation for the evaluated checkpoint(s).” | “three independent training runs”“训练稳定性”“跨训练 seed 显著”。 | 全文统一使用 generation seeds；涉及 TD 的一般化结论依赖 C1。 |

## 导师初稿的当前结论边界

导师初稿可以完整回答 RQ1--RQ3，但 RQ2 必须同时报告 G1 的重复结果和 G2 的负/权衡结果，并保持固定 checkpoint 或 system-level 限定。RQ4 当前只能形成理论问题、操作化方案和结果结构，不能形成经验结论。

提交导师前，逐句检查 Abstract 和 Conclusion：其中每个经验性句子都必须能映射到上表某一条非“待证据/已失效”的记录；若不能映射，则删除、收缩或改为内部占位符。

## 2026-08-27 全文审计记录

- 已覆盖 Abstract、Introduction/Problem、Contributions、RQ1--RQ4、Evaluation、Results、Discussion、Conclusion、Limitations 和相关附录。
- TD 统一限定为单一训练 checkpoint 条件下的 matched fixed-checkpoint contrast；未把生成 seed 写成训练重复，也未把无可靠差异写成等价性结论。
- Direct--Candidate 统一限定为 rationale temperature 不匹配、且查看留出结果后重点分析的描述性 system-level contrast。
- G3 统一为 association/simulatability 证据，不外推为因果忠实性、语义正确性或用户可理解性。
- 旧 G4-v1 分类器数值继续排除；新 RQ4 仅保留冻结方法、统计单位、三个主端点、Results 骨架和限制，不预写方向或数值。
- 英文主稿与中文翻译已同步；此后任何核心经验主张的增删都必须同步更新本表。

## 2026-08-28 积极叙事重构审计

- 摘要、贡献、讨论与结论已统一为“动作中介研究范式—LA-IQL 技术实例—多维长程评价”三层主线。
- 积极结果优先呈现为：固定 checkpoint 下更少的循环与模体、理由的动作预测信息、策略对语义文本的响应，以及可观察的控制权衡。
- Markov control 被解释为支持多维评价范式必要性的诊断证据，而非论文开篇的失败叙事。
- 所有经验性措辞继续保留 fixed-checkpoint、system-level、association 和 exploratory 边界；未新增全面优于 baseline、教学效果、上下文适切性、因果忠实性或用户效用主张。
