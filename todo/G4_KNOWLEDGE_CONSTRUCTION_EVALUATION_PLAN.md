# CHI 2027 G4：模拟课堂对话知识建构评测方案

更新日期：2026-08-27

适用主稿：`sigconf-authordraft.tex`

冻结轨迹根目录：`/Users/abracasora/Downloads/scripts/traj_rd/formal_100/`

评测代码根目录：`/Users/abracasora/Downloads/scripts/`

## 1. 决策摘要

本方案将原 action--utterance classifier G4 替换为对完整模拟课堂轨迹的**多视角自动知识建构诊断**：先由冻结的 LLM 抽取带逐字证据的课堂知识图谱，再用确定性算法计算图谱的知识丰富度、关系组织和随话轮推进的发展；同时用盲化 LLM judge 对内容聚焦、知识展开、跨轮连贯和停滞进行辅助评价。原 G4-v1 classifier 没有完成训练协议，其数值结果不再作为证据；仅选择性保留可复用材料和不依赖分类器训练的规则指标。

该方案原则上只消费已有 JSON 轨迹并新增离线评测产物，**不重新生成对话轨迹**。只有在输入完整性审计发现正式比较条件缺少匹配轨迹时，才另行决定是否生成；不得为改善结果而补跑或挑选轨迹。

本方案评价的是生成文本中可观察的知识结构，不评价真实学生的认知改变。因此全文使用 `knowledge-construction patterns in generated dialogue`、`automatically extracted knowledge development` 或“生成对话中的知识建构模式”，不得写成模型促进了学生知识建构、提升了课堂质量或改善了学习效果。

## 2. 新的 RQ4 与 G4

### 2.1 推荐 RQ4

正文使用：

```latex
\textbf{RQ4}: How does the allocation of action control between the learned
policy and the role model shape observable patterns of knowledge introduction,
connection, and development across long-horizon simulated classroom dialogues?
```

中文释义：

> 学习策略与角色模型之间的动作控制分配，如何影响长程模拟课堂对话中可观察的知识引入、关联和发展模式？

该问题把研究对象限定为：

- policy 与 role model 之间的 action-control allocation，而非笼统的模型优劣；
- 完整、长程的模拟课堂对话，而非孤立话轮；
- 可观察的知识引入、关联和发展模式，而非真实学习效果或教学质量；
- KG extraction 和 LLM judge 是操作化方法，不写入概念层 RQ。

### 2.2 新 G4

```latex
G4: Multi-view automatic knowledge-construction diagnostics
```

G4 包含三个互补层次：

1. **G4-KG（主要证据）**：证据约束的知识图谱抽取与确定性图指标。
2. **G4-Judge（辅助证据）**：盲化、多次运行的 LLM-as-Judge 分维度评价。
3. **G4-Rule（锚点证据）**：不依赖 LLM 的长度、重复、停滞和话轮结构指标。

不得把三层指标加权合成为单一“课堂质量分”。如果三层结果方向一致，可称为 convergent automatic evidence；若不一致，应把不一致本身作为结果报告。

## 3. 现有数据与比较范围

### 3.1 已核实的正式轨迹

`traj_rd/formal_100/` 当前包含以下正式配置，主要配置均覆盖 generation seeds 42、43、44 和 10 个冻结测试 lesson，每条轨迹最多 100 个生成步骤：

| 目录 | 论文名称 | 选择方式 | G4 角色 |
|---|---|---|---|
| `sft_stage3_direct/seed{42,43,44}` | Full Direct | full-space direct argmax | 主系统 |
| `sft_stage3/seed{42,43,44}` | Full Candidate | candidate re-ranking | 主对照 |
| `sft_stage3_woTD_direct/seed{42,43,44}` | w/o-TD Direct | direct argmax | 匹配 TD 消融 |
| `sft_stage3_woTD/seed{42,43,44}` | w/o-TD Candidate | candidate re-ranking | 可选附录 |
| `la_iql/seed{42,43,44}` | 旧/别名 Candidate 产物 | candidate re-ranking | 不进入正式表，除非 provenance 证明其唯一性 |
| `la_iql_direct/` | 旧 Direct 产物 | direct | 不进入正式表，除非完整性和 provenance 审计通过 |

冻结 expert test transcripts 位于：

```text
/Users/abracasora/Downloads/scripts/artifacts/g1_formal/splits/test/expert_data/
```

它们与生成轨迹共享 10 个 lesson，可作为 **held-out expert-dialogue reference**。它不是教材知识的完整真值；没有逐课教材或课程标准时，不得将其称为 curriculum ground truth。

### 3.2 主比较与解释边界

按以下优先级报告：

1. **Full Direct vs. Full Candidate**：回答 action-control allocation 与知识建构模式的关系。由于两者还存在 rationale temperature 0.0 vs. 0.6 的混杂，只能作为 descriptive system-level contrast，不能归因于 decoding mode 单因素。
2. **Full Direct vs. w/o-TD Direct**：相同 direct decoding 下的 fixed-checkpoint TD comparison。由于当前没有独立训练重复，只能说明所评估 checkpoints 的差异，不能外推 TD 的一般训练效果。
3. **Full Direct/Candidate vs. held-out expert dialogue**：报告相对 expert-dialogue reference 的描述性距离，不做“达到人类教学质量”的结论。
4. **语言生成基线**（可选次级分析）：仅在 `traj_baselines/formal_100/` 中 source audit 通过后加入 `direct_role_llm` 与 `constrained_teacher_prompt`。纯 action-only baseline 若没有真实 utterance，不适用于 G4。

统计单位为 `system × generation_seed × lesson_id`。同一固定 checkpoint 的 42/43/44 是 generation seeds，不是训练重复。

## 4. G4-KG：知识图谱评测方法

### 4.1 总体流程

```text
冻结完整轨迹
  → 统一文本清洗与话轮编号
  → 冻结 LLM 抽取节点、关系和逐字证据
  → schema/evidence 自动验收
  → 实体与关系规范化
  → 确定性代码计算完整图和动态图指标
  → lesson 内聚合 generation seeds
  → lesson-cluster 配对推断
```

工作区已有可复用基础：

- 抽取及统计代码：`scripts/evaluation/evaluate_g4_knowledge_graph.py`
- 冻结协议：`baselines/contracts/g4_knowledge_graph_v1.json`
- smoke 产物：`artifacts/g4_kg_smoke/`
- 运行入口：`baselines/run_g4_knowledge_graph.ps1`

现有实现已经做到：固定 node/relation 枚举、节点和边均需逐字 evidence quote、拒绝未知关系与重复实体、LLM 只抽取而不做数值计算、lesson-cluster bootstrap、配对 sign-flip test 和 Holm correction。这些设计应保留。

### 4.2 抽取对象与 schema

每条完整 lesson trajectory 独立抽取一张有向、有类型知识图谱：

\[
G_{s,l,r}=(V,E),
\]

其中 \(s\) 为系统、\(l\) 为 lesson、\(r\) 为 generation seed。

节点至少包含：

```text
id, canonical_name, node_type, scope, discipline, evidence[]
```

边至少包含：

```text
source, target, relation_type, evidence[]
```

每条 evidence 必须包含 `utterance_id` 和该话轮中的逐字 substring。LLM 不得凭借外部常识添加对话中没有表达的知识关系。

建议沿用现有 node types：`concept`、`fact`、`method`、`example`、`textual_element`、`person`、`place`、`event`；沿用现有关系枚举，包括 `is_a`、`part_of`、`has_property`、`causes`、`contrasts_with`、`prerequisite_of`、`applies_to`、`example_of`、`supports` 等。

### 4.3 抽取器独立性

正式 G4 不应只使用与 role realization 相同的 `deepseek-chat` 作为唯一抽取器或 judge，否则可能存在同模型家族偏好。推荐：

- 选择一个与生成 role model 不同家族的冻结模型作为主 KG extractor；
- `temperature=0`，固定 prompt、schema、模型 snapshot/调用日期；
- 在预先冻结的小样本上用第二家族 extractor 做敏感性复核；
- 不根据正式结果选择“更有利”的 extractor。

若预算只允许使用已有 `deepseek-chat` pipeline，G4-KG 必须标记为 single-extractor automatic analysis，并把跨 extractor 稳健性列为限制。

### 4.4 实体规范化

现有实现只在单张图内合并同义实体，跨系统比较仍可能受命名差异影响。正式运行前增加两步：

1. **图内规范化**：全半角、大小写、空白、数学符号和常见同义词归并。
2. **lesson 内跨图对齐**：先从 held-out expert transcript 抽取 lesson reference lexicon，再把各系统实体映射为 `reference entity` 或 `extension entity`；保存原名、规范名、映射置信度和规则/模型来源。

低置信度映射不得强制合并。需要同时报告未映射实体率，以免 coverage 的变化仅来自命名差异。

### 4.5 不重新抽取前缀的动态图构建

每个节点和边已有 evidence utterance ID。定义其首次出现时间：

\[
t(v)=\min\{t: v\text{ 的证据出现在 }U_t\},
\qquad
t(e)=\min\{t: e\text{ 的证据出现在 }U_t\}.
\]

由一次完整图抽取即可确定前缀图：

\[
G^{(k)}=(\{v:t(v)\le k\},\{e:t(e)\le k\}),
\quad k\in\{20,40,60,80,100\}.
\]

这样既不重新生成轨迹，也不需要对每个前缀重复调用抽取器，避免额外成本和前缀间抽取漂移。

## 5. G4-KG 指标

### 5.1 预注册的主要指标

为控制多重比较和叙述空间，正文预先指定三个主要端点。

#### P1. Evidence-grounded unique entity rate（知识丰富度）

\[
\mathrm{UER}_{100}=100\frac{|V|}{T},
\]

其中 \(T\) 为非 `END` utterance 数。它表示每 100 个话轮出现多少个有逐字证据的唯一知识实体。正文不得简称为“知识质量”。

#### P2. Mean relational degree（知识连接广度）

\[
\mathrm{MRD}=\frac{2|E_{simple}|}{|V|}.
\]

这对应现有代码中的 `entity_density`，但正式论文和输出中应改名为 `mean_relational_degree`，因为它不是标准意义上以 \(|V|(|V|-1)\) 为分母的 graph density。值更高表示平均每个实体参与更多直接关系，但并不自动代表更好。

#### P3. Late-stage knowledge growth（长程知识发展）

\[
\mathrm{LKG}=\frac{|E^{(100)}|-|E^{(50)}|}{\max(1,|E^{(100)}|)}.
\]

它表示后半程才首次得到证据支持的关系占最终关系的比例，用于区分“早期引入后不断重复”和“长程持续建立新关系”。考虑正式轨迹被强制至少运行到 step 50，LKG 必须与完整图规模、重复率共同解释，不能单独视为越高越好。

如果不同轨迹实际长度不全为 100，应按各轨迹有效长度的 50% 分位切分，而不是固定 U50。

### 5.2 正文次要指标

1. **Relation-type density**：每个实体关联的不同 canonical relation type 数量均值，衡量关系组织的类型丰富度。
2. **Largest-component ratio**：最大连通分量节点数占比，衡量知识是否形成主体结构。
3. **Reachable-pair ratio**：可连通节点对占全部节点对比例，辅助解释 shortest path。
4. **Reference entity coverage**：生成图覆盖 held-out expert reference entities 的比例。
5. **Reference relation coverage**：生成图覆盖 expert reference relations 的比例。
6. **Extension entity ratio**：未映射到 expert reference、但在生成文本中有证据的相关实体比例。它是“拓展候选”，不是自动认定的有效拓展。
7. **Duplicate-relation rate**：语义规范化后重复表达相同关系的 evidence 次数占比，用于连接 G1 的语言/动作重复与知识层重复。

### 5.3 附录探索指标

- 节点数、边数和 relation type 数；
- curriculum/extension ratio；
- cross-disciplinary edge ratio；
- 最大连通分量内 mean shortest path；
- prefix graph 的 node/edge growth curve 和 area under growth curve；
- 不同 node type、relation type 的完整分布；
- teacher-introduced、student-introduced、jointly-developed entity ratio。

`mean_shortest_path_length` 不作为主要端点：较短可能意味着紧密聚焦，也可能意味着结构简单；较长可能意味着有层次的发展，也可能意味着松散链条。必须与 reachable-pair ratio 和图规模联合报告。

## 6. G4-Judge：LLM-as-Judge 辅助评价

### 6.1 作用边界

LLM judge 不生成 KG 数值，也不提供 G4 的唯一主结论。它用于回答图指标难以覆盖的高层问题，并检查 KG/规则指标是否有相同方向的辅助信号。

采用分维度 rubric，不使用单一总体质量分：

| 维度 | Judge 问题 | 分数 |
|---|---|---|
| Topic grounding | 对话内容是否持续围绕该 lesson 的主题和给定 expert-reference 摘要？ | 1--5 |
| Knowledge elaboration | 是否对概念进行解释、关联、举例或应用，而非只提及术语？ | 1--5 |
| Cross-turn uptake | 后续话轮是否承接并发展前序知识贡献？ | 1--5 |
| Interaction coherence | 问答、回应和话题推进是否跨轮连贯？ | 1--5 |
| Stagnation | 是否反复循环、改写同一内容而缺少新发展？ | 1--5，越高越严重 |

不要让 judge 评价真实学生是否学会、教学是否有效、教师是否喜欢或课堂是否自然。

### 6.2 盲化与配对

- 按相同 `lesson_id × generation_seed` 形成 Direct--Candidate 与 TD--w/o-TD 配对；
- 隐藏 system、checkpoint、action、rationale、seed 和文件路径，只给 lesson metadata、必要的 expert-reference 摘要及完整生成对话；
- 采用 pairwise judgment 为主，pointwise 1--5 分为辅；
- 对每对执行 A/B 与 B/A 顺序交换，顺序翻转时结论不一致则记为 unstable；
- 每个 judge 至少独立重复 3 次；若预算允许，使用两个不同模型家族；
- `temperature=0` 仍需重复运行，因为服务端或模型版本可能引入非确定性；
- 保存逐项理由和引用话轮，但数值由本地代码解析计算。

### 6.3 Judge 指标

正文最多报告：

1. **Pairwise win/tie/loss rate**，每个 rubric dimension 分开报告；
2. **Order consistency**：A/B 与 B/A 是否给出同一相对结论；
3. **Within-judge repeat agreement**：同一项目重复评价的一致率或加权 Cohen's kappa；
4. **Cross-judge agreement**：不同 judge 的一致率与 Krippendorff's alpha/加权 kappa；
5. **Unstable-item rate**：因顺序或重复运行而改变结论的项目比例。

若 judge reliability gate 未通过，只把 judge 结果放附录，不进入摘要、主结果和结论。

## 7. G4-Rule：确定性锚点

对所有相同轨迹直接计算：

- 有效 utterance 数、中文字符/token 数；
- exact utterance repetition；
- local semantic near-duplication；
- 连续相同概念/关系 evidence 的最长停滞长度；
- 前 25%、中间 50%、后 25% 的新实体和新关系引入率；
- teacher/student 对知识实体首次引入的比例；
- 无节点或无边的空图率；
- KG schema 失败率、重试率和未映射实体率。

这些指标既帮助解释 G4，也用于检查“图更大”是否仅由对话更长、表达更冗余或抽取器失败造成。

## 8. 无人评条件下的 evaluator 验证

### 8.1 受控退化集

从冻结 expert test transcripts 中按 lesson 生成不替换正式轨迹的 synthetic validation variants：

1. **Turn shuffle**：保持话轮文本不变，打乱中段顺序；
2. **Knowledge deletion**：删除含关键节点或关系证据的话轮；
3. **Loop insertion**：重复一个连续问答片段直到长度相近；
4. **Off-topic transplant**：插入另一个 lesson 的主题片段；
5. **Relation corruption**：仅在合成文本中替换关系方向或关键数值；
6. **Role swap**：交换选定教师/学生话轮角色。

这些文本只验证 evaluator，不进入系统主比较。

### 8.2 预先冻结的方向性检查

最低要求：

- 原始 expert 的 topic grounding 高于 off-topic transplant；
- 原始 expert 的 coherence 高于 turn shuffle；
- loop insertion 的 stagnation 和 duplicate-relation rate 高于原始 expert；
- knowledge deletion 后 reference coverage 与图规模不升高；
- relation corruption 被支持性检查或 judge 明显降分；
- A/B 顺序交换后的 judge preference consistency 至少 80%；
- KG extractor 的合法 JSON/schema/evidence 验收率至少 95%，其余样本按预先规则重试，不允许人工改图。

80% 是操作性 gate，不是已验证的人类一致性阈值。若失败，应修订 evaluator 并在正式系统结果揭盲前重新冻结；不得查看哪种系统受益后再调 prompt。

### 8.3 抽取稳定性

从 10 个 lesson × 系统条件中按冻结 hash 规则抽取至少 10% 文档，以同一 extractor 重跑。报告：

- 节点名称匹配 F1；
- canonical edge matching F1；
- 三个主指标的 ICC 或绝对差；
- scope、discipline 和 relation-type 一致率。

若稳定性不足，主文只保留对重跑稳定的指标。

## 9. 统计分析协议

### 9.1 聚合顺序

不能把 30 条轨迹当作 30 个独立 lesson。按以下顺序：

1. 计算每个 `system × lesson × generation_seed` 的指标；
2. 在每个 `system × lesson` 内对 generation seeds 42--44 求均值；
3. 在匹配 lesson 上计算系统差值；
4. 以 lesson 为 cluster 做 10,000 次 percentile bootstrap 95% CI；
5. 配对 sign-flip randomization test；
6. 在每个预先冻结的 comparison family 内做 Holm correction。

### 9.2 两个比较 family

- Family A：Full Direct vs. Full Candidate 的三个 KG 主要端点和五个 judge dimensions；
- Family B：Full Direct vs. w/o-TD Direct 的相同端点。

Expert reference distance 以描述性 effect size 和 CI 为主，不与系统胜负检验混为一个 correction family。

### 9.3 报告格式

每项至少报告：目标系统均值、对照均值、paired difference、lesson-cluster 95% CI、原始 p、Holm-adjusted p，以及有效 lesson 数。重点解释 effect size 和跨 lesson 异质性，不以 `p<.05` 代替实质解释。

## 10. 推荐的正文展示

### 10.1 主表

正文 G4 表只放三个 KG 主端点：

| Comparison | Unique entities / 100 turns | Mean relational degree | Late-stage relation growth |
|---|---:|---:|---:|
| Direct | value [CI] | value [CI] | value [CI] |
| Candidate | value [CI] | value [CI] | value [CI] |
| Direct $-$ Candidate | effect [CI] | effect [CI] | effect [CI] |

TD--w/o-TD 可用第二个紧凑 panel；如果篇幅不足放附录，正文报告效应方向和 CI。

### 10.2 主图

优先使用一张 **knowledge growth curve**：横轴为归一化话轮进度，纵轴分别为累计唯一实体和累计唯一关系；展示 expert、Direct、Candidate 的 lesson-level mean 和 cluster CI。图的目的不是宣称谁“更好”，而是让读者看到知识引入、连接和停滞发生在何时。

### 10.3 定性案例

按预先冻结规则选择同一 lesson/seed 的一个案例，例如 Direct--Candidate 的 late-stage growth difference 绝对值最大者。展示：

- 同一早期上下文；
- 两条轨迹的关键 action sequence；
- 新节点/关系首次出现的话轮；
- 重复或停滞片段；
- 对应 KG 子图。

必须同时呈现优势与代价，不只挑选有利案例。

## 11. 论文措辞边界

### 11.1 可以写

```latex
Under a frozen evidence-grounded extraction pipeline, Direct and Candidate
produce different patterns of concept introduction and relational development.
```

```latex
The explicit action boundary allows long-horizon action patterns to be related
to observable changes in the knowledge structures expressed in generated
dialogue.
```

```latex
The KG, rule-based, and LLM-judge diagnostics provide convergent automatic
evidence on specified dialogue properties.
```

### 11.2 不可以写

- “LA-IQL improves students' knowledge construction.”
- “Candidate produces higher-quality teaching.”
- “The generated knowledge is correct.”（除非有独立 lesson source grounding）
- “LLM judges replace educators.”
- “The system improves learning outcomes.”
- “Higher graph density is pedagogically better.”

### 11.3 必须写入 Limitations

```latex
G4 measures knowledge structures expressed in generated text rather than
changes in learner knowledge. Both graph extraction and rubric scoring depend
on frozen LLM evaluators and may inherit model-specific biases. Controlled
perturbations and cross-evaluator checks test operational sensitivity but do
not establish agreement with educators or learners.
```

## 12. 对现有 KG pipeline 的必要修改

正式运行前需要在现有 `g4-kg-v1` 基础上完成以下改动；这些都是评测后处理，不要求重生成轨迹：

- [ ] 正式 source 使用 `sft_stage3_direct`、`sft_stage3`、`sft_stage3_woTD_direct` 和 expert，避免把 `la_iql` 旧别名误当主系统。
- [ ] 将输出字段 `entity_density` 改名或同时输出 `mean_relational_degree`，避免图论术语错误。
- [ ] 由 evidence utterance ID 计算节点/边首现时间及 prefix growth curve。
- [ ] 增加 `late_stage_knowledge_growth`、duplicate-relation rate 和未映射实体率。
- [ ] 加入 lesson 内跨图实体规范化与 expert-reference coverage。
- [ ] 增加 controlled-corruption evaluator validation，不把未完成的人评模板当作有效性证据。
- [ ] 正式抽取器尽量与 `deepseek-chat` role model 解耦；至少进行第二 extractor 敏感性检查。
- [ ] 将 KG extraction、LLM judging、metric computation 分别保存 immutable config、prompt、input hashes 和 outputs。
- [ ] 在揭盲正式系统结果前冻结主指标、比较 family、失败处理和 correction rule。

## 13. 实施阶段与停止规则

### Phase 0：输入冻结与审计

1. 对每个正式系统核对 3 seeds × 10 lessons；
2. 核对 `lesson_id`、`generation_seed`、`system_id`、`steps`、`ended_by`；
3. 保存轨迹 SHA-256 manifest；
4. 明确旧别名目录是否排除；
5. 不修改或重生成轨迹。

### Phase 1：小规模 evaluator validation

1. 使用 expert transcripts 和 controlled corruptions；
2. 检验 KG schema、evidence 和方向性 gates；
3. 检验 judge 的 order/repeat consistency；
4. 只有通过 gates 才冻结 protocol。

### Phase 2：正式 KG 抽取

1. 对 expert、Full Direct、Full Candidate、w/o-TD Direct 全量抽取；
2. 自动验收、重试并记录失败；
3. 一次抽取后由 evidence IDs 计算动态图；
4. 不因结果方向重新选择 extractor 或 prompt。

### Phase 3：LLM judge 与统计

1. 生成盲化配对；
2. 执行位置交换和重复评分；
3. 先报告 reliability，再报告 system comparison；
4. 完成 lesson-cluster CI、sign-flip test 和 Holm correction。

### Phase 4：论文落稿

1. 替换 RQ4、Evaluation Metrics、Results、Discussion、Conclusion；
2. 原 G4-v1 classifier 的未完成训练结果不进入论文数值证据；附录只保留协议、失败说明、可复用材料及独立规则指标；
3. 正文加入主表、growth curve 和一个规则化案例；
4. 明确无人评和无学习结果的主张边界。

停止规则：如果 KG extractor 不能通过 evidence/schema gate，或 controlled corruptions 上指标方向不符合预期，则 G4 不进入主文；保留为 exploratory appendix，并将 RQ4 收缩为未来工作。不得用正式系统排名来决定是否保留某项指标。

## 14. 预期产物

建议正式评测输出到新的版本目录，例如：

```text
artifacts/g4_knowledge_construction_v2/
  protocol.json
  input_manifest.csv
  extractor_config.json
  extraction_events.jsonl
  graphs/
  entity_alignment.csv
  graph_metrics.csv
  prefix_graph_metrics.csv
  rule_metrics.csv
  controlled_validation.csv
  judge_config.json
  blinded_pairs.jsonl
  llm_judgments.jsonl
  judge_reliability.csv
  lesson_metrics_seed_reduced.csv
  pairwise_lesson_differences.csv
  pairwise_summary.csv
  paper_g4_table.tex
  g4_report.md
```

## 15. 成功标准

只有满足以下条件，新 G4 才足以替换当前正文 G4：

1. 所有主系统与 expert 输入均有冻结 hash，正式比较不需重生成轨迹；
2. KG schema/evidence 验收率达到冻结 gate，失败与重试完全记录；
3. controlled corruptions 验证主要指标和 judge 对指定退化有正确方向敏感性；
4. 抽取稳定性、judge 顺序一致性和重复一致性均被报告；
5. 三个 KG 主要指标及比较 family 在查看正式排名前冻结；
6. 统计以 lesson 为 cluster，并明确 generation seed 与 training seed 的区别；
7. 结果措辞限定于自动抽取的生成对话知识结构；
8. 不声称课堂适切性、真实教学质量、学生学习或教育效果。

满足这些条件后，G4 的合理定位是：**关于 policy 与 role model 之间的 action-control allocation 如何关联到长程生成对话中可观察知识结构的多视角自动证据**，而不是无人评条件下对“课堂质量”的替代证明。

## 16. 原 G4 的选择性保留规则

### 16.1 继续使用

- `traj_rd/formal_100/` 中已冻结的完整生成轨迹；
- expert lesson split、generation seed 和 lesson pairing；
- 输入解析、source audit、hash manifest 和随机化基础设施；
- local trigram redundancy、exact repetition、schema leakage、role conflict 和 rule-defined severe violations；
- blinded item、rubric 和 randomization manifest 的生成逻辑，可按新 G4 rubric 改造；
- classifier training/audit artifacts 仅作为内部 provenance 和失败排查材料。

### 16.2 不进入当前论文证据

- Direct 1.30%、Candidate 2.63% 和 w/o-TD 1.01% classifier agreement；
- 同一未完成 classifier 产生的 Macro-F1、CI、$p$/$q$；
- Candidate 改善 action--utterance realization、TD 不影响 realization 等系统结论；
- 将分类器低 agreement 解释为真实 realization failure 的任何措辞。

### 16.3 未来恢复条件

只有完整训练协议和冻结 validity gates 全部通过，才允许以新的 metric version 作为**次级** action--utterance diagnostic 恢复。新结果不得与旧结果拼接、平均或声称复现；旧运行永久标为 `preliminary-invalidated-incomplete-training`。无论是否恢复，该分类器都不再回答新 RQ4。
