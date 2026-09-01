# 2025--2026 年相关工作整理与插入建议

适用主稿：`../sigconf-authordraft.tex`  
整理日期：2026-09-01  
范围：interactive agents、interactive/conversational agency、长期交互策略、教学智能体、对话评价与模拟有效性。

## 1. 使用原则

1. Abstract、Introduction、Discussion 和 Conclusion 是导师确认后的冻结锚点。除非导师同意，不重写其论证；Introduction 只建议在现有句末补充新引用。
2. 新增论述优先进入 Related Work 的三个现有 subsection，不继续增加 subsection 数量。
3. `interactive agents` 指系统对象；`interactive agency` 或 `conversational agency` 指主动参与、控制分配和行动能力；`language model`、`language realization` 和 LA-IQL 的方法名应保留。
4. 不能因为年份新就加入文献。优先选择能支撑以下四个缺口的工作：长期互动不等于单轮流畅、显式策略与控制分配、从真人互动中学习行为结构、互动质量不能由自动指标单独确立。

## 2. 最小推荐修改集

若正文篇幅有限，建议新增以下 7 篇；它们与现有文献的重复最少。

| 优先级 | 文献 | 主要补足 | 推荐位置 |
|---|---|---|---|
| P0 | Deshpande et al. 2025, MultiChallenge | 现代模型在真实多轮交互中的持续困难 | Introduction 第三段仅补 citation；2.3 |
| P0 | Srinivas et al. 2025, Substance over Style | 用户体验、专家评价与 LM 评价可能不一致 | 2.3；必要时 5.4 仅补 citation |
| P0 | Tokida et al. 2026, AI Virtual Peer | 教师控制的显式 speech-act 层，是 LA-IQL 的最近 HCI 系统对照 | 2.1，紧接 ScaffoldLM |
| P0 | Lee et al. 2026, Tutor Personas | 从真人 tutor dialogue 学习可解释的行为差异 | 2.1，紧接 Tokida et al. |
| P1 | Chen et al. 2025, Balanced Conflict | 主动干预的时机、策略和用户自主权 | 2.2，紧接 Inner Thoughts |
| P1 | Gao et al. 2025, Interaction Matters | 互动质量需要 dialogue-level 与 micro-level 指标 | 2.3，开头评价框架段 |
| P1 | Samanta et al. 2026, Biased Judges | LLM Judge 对社会对话结构和人类偏好的失配 | 2.3 末尾；若恢复 Judge 再进入 Limitations |

推荐的最小插入顺序：

- 2.1：Puech / ScaffoldLM → Tokida → Lee → LA-IQL 差异。
- 2.2：Inner Thoughts → Balanced Conflict → shared autonomy / participation control → LA-IQL 控制边界。
- 2.3：Interaction Matters → MRBench / ReWIRED / EducationQ → Substance over Style / MultiChallenge → simulated learners → Biased Judges → 本文评价边界。

## 3. 建议新增文献

### 3.1 Deshpande et al. (2025) — MultiChallenge

- **题目**：*MultiChallenge: A Realistic Multi-Turn Conversation Evaluation Benchmark Challenging to Frontier LLMs*
- **来源**：Findings of ACL 2025；DOI `10.18653/v1/2025.findings-acl.958`
- **官方链接**：https://aclanthology.org/2025.findings-acl.958/
- **内容概要**：提出面向真实人机多轮对话的评测集，覆盖需要同时处理指令遵循、上下文分配和上下文推理的四类挑战。论文报告，即使前沿模型在既有基准上接近满分，在该基准上的准确率仍低于 50%。
- **与本文关系**：直接支持导师要求的核心问题陈述：单轮回答能力或表面流畅并不等于持续互动能力。它评价多轮任务鲁棒性，而 LA-IQL 进一步把跨轮互动策略显式化并评价其时间组织。
- **插入位置**：
  - 冻结 Introduction 第三段中 `Individually fluent turns can accumulate into repetitive or poorly coordinated interaction` 的 citation 列表，可加入该文献，不改句子。
  - 2.3 在讨论 interaction-level evaluation 时加入。
- **可用英文句**：`Recent multi-turn benchmarks likewise show that strong single-turn performance does not guarantee robust behavior when dialogue requires simultaneous context allocation, instruction following, and cross-turn reasoning~\citep{deshpande2025multichallenge}.`

### 3.2 Srinivas et al. (2025) — Substance over Style

- **题目**：*Substance over Style: Evaluating Proactive Conversational Coaching Agents*
- **来源**：ACL 2025；DOI `10.18653/v1/2025.acl-long.1017`
- **官方链接**：https://aclanthology.org/2025.acl-long.1017/
- **内容概要**：实现五种多轮 coaching agents，并通过 155 次对话的用户研究比较第一人称用户反馈、健康专家第三方评价和语言模型评价。用户重视核心功能，只有风格而缺少核心能力会被负面评价；不同评价视角之间存在显著失配。
- **与本文关系**：支持把互动策略、语言风格和用户体验分开评价，也支持本文不把结构指标直接解释为 engagement 或 usefulness。不同之处是该工作有用户研究，而本文提供动作层和长程结构诊断。
- **插入位置**：2.3 在 MRBench / EducationQ 后，用于说明自动或第三方评价不能替代第一人称互动体验。
- **可用英文句**：`User-centered evidence further shows that conversational style, core interactive functionality, and perceived quality are not interchangeable, and that first-person, expert, and model-based evaluations can disagree~\citep{srinivas2025substance}.`

### 3.3 Gao et al. (2025) — Interaction Matters

- **题目**：*Interaction Matters: An Evaluation Framework for Interactive Dialogue Assessment on English Second Language Conversations*
- **来源**：COLING 2025；页码 10977--11012
- **官方链接**：https://aclanthology.org/2025.coling-main.729/
- **内容概要**：提出两层互动评价框架，包括 topic management、tone appropriateness、conversation opening/closing 等 dialogue-level 标签，以及 backchannels、reference words 等 17 类 micro-level 特征，并分析微观信号与整体互动质量的关系。
- **与本文关系**：证明互动评价需要高层对话组织与低层实现共同存在，和本文将 action-pattern organization 与 language realization 分开但联合检查的思路一致。该工作评价真人 ESL 对话，而非学习智能体策略。
- **插入位置**：2.3 第一段，在 `Evaluation must likewise distinguish structural fidelity from pedagogical quality` 之后。
- **可用英文句**：`Interaction-level assessment has similarly been decomposed into dialogue-level organization and micro-level realizations, showing that fluency alone does not capture topic management or other forms of interactional competence~\citep{gao2025interaction}.`

### 3.4 Chen et al. (2025) — Maintaining “Balanced” Conflict

- **题目**：*Maintaining “Balanced” Conflict: Proactive Intervention Strategies of AI Voice Agents in Online Collaboration of Temporary Design Teams*
- **来源**：CHI 2025；DOI `10.1145/3706598.3713457`
- **官方链接**：https://doi.org/10.1145/3706598.3713457
- **内容概要**：研究 AI voice agent 在在线团队协作中的主动干预，区分 resolve、mitigate、redirect、promote 等策略，并讨论何时不干预、何时提供客观或情感支持，以及如何用建议式语言降低对用户自主权的侵扰。
- **与本文关系**：是 `interactive agency` 和显式策略选择的直接 HCI 证据，表明“是否参与、何时参与、采用何种动作”是独立于措辞的设计变量。其策略由研究设计和情境规则配置；LA-IQL 从固定真人轨迹学习动作策略。
- **插入位置**：2.2 在 Inner Thoughts 后、shared autonomy 前。
- **可用英文句**：`Proactive voice agents likewise require explicit decisions about whether, when, and how to intervene, with different conflict states calling for qualitatively different strategies and different constraints on user autonomy~\citep{chen2025balanced}.`

### 3.5 Lee et al. (2026) — Tutor Personas from Human Dialogue

- **题目**：*Letting Tutor Personas Speak Up for LLMs: Learning Steering Vectors from Dialogue via Preference Optimization*
- **来源**：BEA 2026；DOI `10.18653/v1/2026.bea-1.7`
- **官方链接**：https://aclanthology.org/2026.bea-1.7/
- **内容概要**：从真人 tutor--student dialogue 中学习 tutor persona steering vectors，捕捉 scaffolding、directiveness、feedback 和 affective support 等跨情境差异。结果显示，steering 能提升与真人 tutor utterance 的语义对齐，并产生可解释的 tutor 间行为结构。
- **与本文关系**：与 human-grounded 的数据来源最接近：两者都从真人课堂/辅导对话中提取控制信号。区别是该工作学习连续的 persona/style 方向并直接影响生成，LA-IQL 学习离散、人类可读的 interaction acts，并把动作选择与语言实现分开。
- **插入位置**：2.1 在 ScaffoldLM 或 Tokida et al. 之后，作为 closest recent work 之一。
- **可用英文句**：`Recent work also learns tutor-specific behavioral variation directly from human dialogue through activation-space steering~\citep{lee2026tutorpersonas}; LA-IQL instead exposes a discrete action policy whose individual choices and temporal organization can be inspected separately from realization.`

### 3.6 Tokida et al. (2026) — Teacher-Controlled AI Virtual Peer

- **题目**：*Design and Evaluation of a Photorealistic AI Virtual Peer in Elementary Collaborative Classroom*
- **来源**：CHI 2026；DOI `10.1145/3772318.3791450`
- **官方链接**：https://doi.org/10.1145/3772318.3791450
- **内容概要**：构建课堂 AI virtual peer “Saya”，使用 GPT-4o-mini 生成对话，同时让教师从 expand、probe、summarize、lighten 和 incorrect answer 五类 speech acts 中选择行为；并在真实小学课堂中开展分阶段研究。
- **与本文关系**：这是当前最接近“显式动作层 + 独立语言生成”的 HCI 系统。关键差异是 Saya 由教师在线选择动作，LA-IQL 则从固定真人轨迹离线学习动作策略，不依赖部署时人工选择。
- **插入位置**：2.1 在 BIPED / ScaffoldLM 后，必须明确 nearest-work difference；也可在 2.2 控制分配段引用教师控制。
- **可用英文句**：`A complementary HCI design gives teachers direct control over five speech acts used by a classroom virtual peer before an LLM realizes the selected act~\citep{tokida2026virtualpeer}. LA-IQL targets the complementary problem of learning this action-selection layer offline from human trajectories.`

### 3.7 Samanta et al. (2026) — Simple Agents, Biased Judges

- **题目**：*Simple Agents, Biased Judges: Efficient Multi-Party Dialogue Generation & The Evaluation Gap*
- **来源**：ACL 2026；DOI `10.18653/v1/2026.acl-long.2006`
- **官方链接**：https://aclanthology.org/2026.acl-long.2006/
- **内容概要**：在 319 个 pairwise comparisons 上比较人类与 LLM judges 对多方社会对话的评价，报告接近随机的人机一致性（Cohen's kappa 约 0.11），并发现 tie aversion、assistant-style verbosity 偏好以及对随机打乱话轮结构不敏感等系统偏差。
- **与本文关系**：直接支撑本文不使用失败的成对 LLM Judge 作为主证据，以及不能用自动 judge 证明 naturalness、engagement 或整体互动质量。该文关注多方开放域对话，本文关注动作层结构与课堂长程轨迹。
- **插入位置**：2.3 末段，在模拟有效性之后加入自动评价有效性；只有未来恢复 LLM Judge 时才在 Limitations 再引用。
- **可用英文句**：`Recent human comparisons also expose systematic biases in LLM-based dialogue judges, including sensitivity to assistant-style verbosity and weak responsiveness to disrupted conversational order~\citep{samanta2026biasedjudges}. We therefore rely on auditable action and graph endpoints rather than treating an LLM judge as evidence of overall interaction quality.`

## 4. 现稿已有、建议保留的 2025--2026 文献

### 4.1 Interaction agency 与控制分配

#### Liu et al. (2025), Proactive Conversational Agents with Inner Thoughts

- **当前 key**：`liu2025proactive`
- **概要**：把内部 thought formation 与公开参与分开，使 agent 不只被动等待提示，而能判断何时主动加入对话。
- **当前位置**：2.2。
- **保留原因**：直接对应“何时参与”的 conversational agency；与 LA-IQL 的差异是其重点为参与时机，而 LA-IQL 学习可读动作上的策略轨迹。
- **官方 DOI**：https://doi.org/10.1145/3706598.3713760

#### Cheng et al. (2025), Conversational Agents on Your Behalf

- **当前 key**：`cheng2025surrogates`
- **概要**：通过 18 个 dyads 比较无自治、共享自治和完全自治的语音代理，显示控制分配对多任务表现、监控负担和使用体验存在非单调影响。
- **当前位置**：2.2。
- **保留原因**：支撑“更多 policy control 不天然更好”，与 Direct--Candidate 的 control-allocation framing 相容，但不能把该用户研究结果外推为本文系统的用户效果。
- **官方 DOI**：https://doi.org/10.1145/3706598.3714017

#### Houde et al. (2025), Controlling AI Agent Participation in Group Conversations

- **当前 key**：`houde2025controlling`
- **概要**：研究用户如何控制 AI 在群体对话中何时、说什么和在哪里参与，并指出用户反感 agent 主导对话。
- **当前位置**：2.2。
- **保留原因**：为 participation control 提供直接 HCI 背景，并帮助限定 LA-IQL 的控制边界是系统内部 policy--role-model 分配，不是用户控制实验。
- **官方 DOI**：https://doi.org/10.1145/3708359.3712089

### 4.2 教学对话中的显式规划、动作和策略学习

#### Puech et al. (2025), Pedagogical Steering / StratL

- **当前 key**：`puech2025steering`
- **概要**：用 transition graph 表示预设的 productive-failure 多轮教学计划，并优化 prompt 以引导 LLM 遵循该计划；包含 17 名高中生的 field study。
- **当前位置**：2.1。
- **保留原因**：最直接说明“helpful assistant”倾向会过早给出答案，教学需要跨轮策略。与 LA-IQL 的差异是 StratL 遵循预定义计划，LA-IQL 从真人轨迹学习策略。
- **官方链接**：https://aclanthology.org/2025.findings-acl.1348/

#### Dinucu-Jianu et al. (2025), RL for Pedagogical Alignment

- **当前 key**：`dinucu2025teaching`
- **概要**：利用模拟 student--tutor interaction 和在线 RL，在 pedagogical support 与 student problem-solving accuracy 之间调节奖励权重。
- **当前位置**：2.1 第二段。
- **保留原因**：构成 LA-IQL “无需在线探索、模拟器或手工标量奖励”差异的最近 RL 对照。
- **官方链接**：https://aclanthology.org/2025.emnlp-main.15/

#### Li et al. (2026), ScaffoldLM

- **当前 key**：`li2026scaffoldlm`
- **概要**：维护分步教学计划、学习者认知状态、进度和 assessment-driven memory，并跨轮自适应选择 tutoring actions。
- **当前位置**：2.1。
- **保留原因**：支撑长程规划和显式 action selection；与 LA-IQL 的差异是 ScaffoldLM 围绕解题计划和推断状态，LA-IQL 从真实课堂的认知动作轨迹学习通用策略层。
- **官方链接**：https://aclanthology.org/2026.acl-long.325/

### 4.3 教学智能体和模拟的评价

#### Maurya et al. (2025), Unifying AI Tutor Evaluation / MRBench

- **当前 key**：`maurya2025unifying`
- **概要**：提出学习科学驱动的 tutor evaluation taxonomy，并提供带人工标注的多维评价资源。
- **当前位置**：2.3。
- **保留原因**：支持教学质量是多维对象，不能被单一动作分布或 KG 指标替代。
- **官方链接**：https://aclanthology.org/2025.naacl-long.57/

#### Anagnostopoulou et al. (2025), ReWIRED / Teaching Acts

- **当前 key**：`anagnostopoulou2025rewired`
- **概要**：标注专家解释性对话中的 teaching acts，并评价人类与 LLM 对这些行为和解释质量的判断。
- **当前位置**：2.3。
- **保留原因**：支撑细粒度行为标签的可解释价值，也提醒结构标签不能代替功能质量。
- **官方链接**：https://aclanthology.org/2025.codi-1.15/

#### Shi et al. (2025), EducationQ

- **当前 key**：`shi2025educationq`
- **概要**：用动态 multi-agent dialogue 评价教学能力，并报告通用模型能力与教学效果并非单调对应。
- **当前位置**：2.3。
- **保留原因**：支撑“模型整体能力或表面表现不等于互动教学能力”。
- **官方链接**：https://aclanthology.org/2025.acl-long.1576/

#### Martynova et al. (2025), Can LLMs Effectively Simulate Human Learners?

- **当前 key**：`martynova2025simulate`
- **概要**：通过教师视角研究 LLM student simulation，指出模拟学生可能过度专注、语言复杂且逻辑不一致。
- **当前位置**：2.3 第二段。
- **保留原因**：直接限定本文生成课堂轨迹不能被当成真实学习者行为。
- **官方链接**：https://aclanthology.org/2025.bea-1.8/

#### Scarlatos et al. (2026), Simulated Students in Tutoring Dialogues

- **当前 key**：`scarlatos2026simulated`
- **概要**：定义 student simulation task，并用语言、行为和认知多维指标加人工评价系统比较多种模拟方法；简单 prompting 表现不足，SFT 和 preference optimization 更好但仍有限。
- **当前位置**：2.3 第二段。
- **保留原因**：为 simulation validity 提供最新、最系统的证据。
- **官方链接**：https://aclanthology.org/2026.acl-long.1960/

## 5. 建议的正文插入草案

以下草案只改 Related Work，不触碰四个冻结锚点。

### 5.1 2.1 Interaction-Strategy Learning in Pedagogical Dialogue

建议放在 ScaffoldLM 之后、`Together, these systems...` 之前：

> A complementary HCI system gives teachers direct control over five speech acts---expand, probe, summarize, lighten, and incorrect answer---before an LLM realizes the selected act for a classroom virtual peer~\citep{tokida2026virtualpeer}. Recent work also derives tutor-specific steering directions from authentic tutor--student dialogue, capturing variation in scaffolding, directiveness, feedback, and affective support~\citep{lee2026tutorpersonas}. These systems reinforce the value of separating behavioral control from surface wording. LA-IQL targets a different learning problem: it recovers an explicit policy over discrete, human-readable interaction acts from fixed human trajectories, without requiring deployment-time teacher selection or reducing strategy to a latent persona direction.

### 5.2 2.2 Interactive Agency and Control Allocation

建议放在 Inner Thoughts 后：

> Proactivity also requires deciding not only when to speak but which intervention to make. In online team collaboration, AI voice agents use different strategies to resolve, mitigate, redirect, or promote discussion, while suggestive realization helps preserve user autonomy~\citep{chen2025balanced}. This further frames interactive agency as a structured allocation of initiative and action support rather than a uniformly desirable increase in autonomy.

### 5.3 2.3 Evaluating Interactive Behavior

建议把当前开头扩充为：

> Evaluation must distinguish local response quality, interaction-level organization, and outcomes for people. Dialogue assessment work decomposes interactivity into higher-level properties such as topic management and lower-level realizations such as backchannels~\citep{gao2025interaction}. Multi-turn benchmarks likewise show that strong single-turn performance does not guarantee robust behavior under cross-turn dependencies~\citep{deshpande2025multichallenge}. In user studies of proactive coaching agents, first-person feedback, expert judgments, and model-based evaluations can also disagree~\citep{srinivas2025substance}.

建议在本 subsection 末尾加入：

> Automatic evaluators introduce an additional validity risk. Human comparisons of multi-party dialogue judgments reveal systematic LLM-judge biases toward assistant-style verbosity and weak sensitivity to disrupted conversational order~\citep{samanta2026biasedjudges}. We therefore treat action, intervention, and evidence-grounded graph endpoints as bounded structural diagnostics rather than proxies for overall naturalness, engagement, or pedagogical quality.

## 6. 新增 BibTeX 候选

以下条目尚未写入 `references.bib`；采用前应保持 key 与正文一致。

```bibtex
@inproceedings{deshpande2025multichallenge,
  author    = {Deshpande, Kaustubh and Sirdeshmukh, Ved and Mols, Johannes Baptist and Jin, Lifeng and Hernandez-Cardona, Ed-Yeremai and Lee, Dean and Kritz, Jeremy and Primack, Willow E. and Yue, Summer and Xing, Chen},
  title     = {{MultiChallenge}: A Realistic Multi-Turn Conversation Evaluation Benchmark Challenging to Frontier {LLM}s},
  booktitle = {Findings of the Association for Computational Linguistics: ACL 2025},
  pages     = {18632--18702},
  year      = {2025},
  publisher = {Association for Computational Linguistics},
  doi       = {10.18653/v1/2025.findings-acl.958},
  url       = {https://aclanthology.org/2025.findings-acl.958/}
}

@inproceedings{srinivas2025substance,
  author    = {Srinivas, Vidya and Xu, Xuhai and Liu, Xin and Ayush, Kumar and Galatzer-Levy, Isaac and Patel, Shwetak and McDuff, Daniel and Althoff, Tim},
  title     = {Substance over Style: Evaluating Proactive Conversational Coaching Agents},
  booktitle = {Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  pages     = {20848--20880},
  year      = {2025},
  publisher = {Association for Computational Linguistics},
  doi       = {10.18653/v1/2025.acl-long.1017},
  url       = {https://aclanthology.org/2025.acl-long.1017/}
}

@inproceedings{gao2025interaction,
  author    = {Gao, Rena and Roever, Carsten and Lau, Jey Han},
  title     = {Interaction Matters: An Evaluation Framework for Interactive Dialogue Assessment on English Second Language Conversations},
  booktitle = {Proceedings of the 31st International Conference on Computational Linguistics},
  pages     = {10977--11012},
  year      = {2025},
  publisher = {Association for Computational Linguistics},
  url       = {https://aclanthology.org/2025.coling-main.729/}
}

@inproceedings{chen2025balanced,
  author    = {Chen, XinHui and Yuan, Xiang and Zhang, Hui and Zheng, Ruixiao and Wei, Wanyi},
  title     = {Maintaining ``Balanced'' Conflict: Proactive Intervention Strategies of {AI} Voice Agents in Online Collaboration of Temporary Design Teams},
  booktitle = {Proceedings of the 2025 CHI Conference on Human Factors in Computing Systems},
  pages     = {1--19},
  year      = {2025},
  publisher = {Association for Computing Machinery},
  doi       = {10.1145/3706598.3713457},
  url       = {https://doi.org/10.1145/3706598.3713457}
}

@inproceedings{lee2026tutorpersonas,
  author    = {Lee, Jaewook and Scarlatos, Alexander and Woodhead, Simon and Lan, Andrew},
  title     = {Letting Tutor Personas Speak Up for {LLM}s: Learning Steering Vectors from Dialogue via Preference Optimization},
  booktitle = {Proceedings of the 21st Workshop on Innovative Use of NLP for Building Educational Applications (BEA 2026)},
  pages     = {78--92},
  year      = {2026},
  publisher = {Association for Computational Linguistics},
  doi       = {10.18653/v1/2026.bea-1.7},
  url       = {https://aclanthology.org/2026.bea-1.7/}
}

@inproceedings{tokida2026virtualpeer,
  author    = {Tokida, Satomi and Usui, Koki and Tanaka, Godai and Osuga, Shin and Kayano, Masanori and Itoh, Yuta and Ishiguro, Yoshio},
  title     = {Design and Evaluation of a Photorealistic {AI} Virtual Peer in Elementary Collaborative Classroom},
  booktitle = {Proceedings of the 2026 CHI Conference on Human Factors in Computing Systems},
  pages     = {1--15},
  year      = {2026},
  publisher = {Association for Computing Machinery},
  doi       = {10.1145/3772318.3791450},
  url       = {https://doi.org/10.1145/3772318.3791450}
}

@inproceedings{samanta2026biasedjudges,
  author    = {Samanta, Kunal and Shohan, Faisal Tareque and Trabelsi, Amine and Khoury, Richard},
  title     = {Simple Agents, Biased Judges: Efficient Multi-Party Dialogue Generation {\&} The Evaluation Gap},
  booktitle = {Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  pages     = {43326--43345},
  year      = {2026},
  publisher = {Association for Computational Linguistics},
  doi       = {10.18653/v1/2026.acl-long.2006},
  url       = {https://aclanthology.org/2026.acl-long.2006/}
}
```

## 7. 不建议作为核心引用的候选

- 只讨论单轮生成质量、一般 agent tool use 或模型推理能力，而不涉及互动策略、主动权或跨轮组织的工作，不应为了年份新而加入。
- 仅有 arXiv、尚无正式发表信息且与现有正式论文主张重复的 2026 工作，暂不作为 Related Work 核心支柱。
- 讨论用户 engagement、trust 或 pedagogical effectiveness 的文献只能支撑这些概念的重要性，不能替代本文缺少的用户研究，也不能把结构端点解释成用户效果。

## 8. 落稿后的检查清单

- [ ] 新增 7 个 BibTeX 条目并通过 DOI/ACL Anthology 元数据复核。
- [ ] 2.1 明确 Tokida、Lee 与 LA-IQL 的 nearest-work difference。
- [ ] 2.2 使用 `interactive agency`，但不把 user control 与内部 policy--role-model control 混为一谈。
- [ ] 2.3 同时覆盖 multi-turn challenge、第一人称评价和 LLM Judge validity。
- [ ] Introduction 若保持冻结，仅调整 citation，不新增结果或重写论证。
- [ ] 不在 Abstract、Results 或 Conclusion 中引入这些文献的外部结果。
- [ ] 编译检查无 undefined citations，并同步中文翻译。
