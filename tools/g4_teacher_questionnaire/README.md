# G4 教师评价题库生成器

本目录独立实现 `todo/G4_TEACHER_HUMAN_EVALUATION_PLAN.md` 中的题库构造、盲化、任务分配和样例问卷生成。脚本只依赖 Python 3.9+ 标准库，不调用模型，也不重新生成轨迹。

## 生成命令

在论文仓库根目录运行：

```bash
python3 tools/g4_teacher_questionnaire/build_question_bank.py \
  --trajectory-root /path/to/traj_rd/formal_100 \
  --output-dir tools/g4_teacher_questionnaire/example_output
```

若要生成另一个参与者版本的样例问卷，可增加 `--sample-participant P02`。`--salt` 控制可复现的题目选择、左右盲化和题序；正式冻结后不得更改。

## 输入系统

- Family A：`sft_stage3_direct` vs. `sft_stage3`；
- Family B：`sft_stage3_direct` vs. `sft_stage3_woTD_direct`；
- 三者必须在相同的 `lesson_id × generation_seed` 上配对。

## 输出

- `sample_item_bank.jsonl`：不含系统身份的 25 个公开题目；
- `sample_blind_mapping_private.csv`：系统身份与源文件映射，必须私下保存；
- `sample_assignment_manifest.csv`：10 位参与者的平衡不完全区组分配；
- `sample_questionnaire.md`：便于审核内容的样例问卷；
- `sample_questionnaire.html`：浏览器可直接预览的响应式样例问卷；
- `sample_item_bank_import.csv`：按“题型、题目、选项1--6、答案、答案解析、分值”编排的完整 25-item 题库，共 125 个正式评分题；
- `sample_questionnaire_P01_import.csv`：同一格式的 P01 完整样例问卷，含同意、背景、练习、25 个正式评分题、注意力题和末页；
- `validation_report.json`：数量、覆盖、分配、文本上限和题库哈希校验。

CSV 使用带 BOM 的 UTF-8 编码，可直接用 Excel 打开，也便于复制到支持图示格式的中文问卷平台。正式判断题没有标准答案，因此“答案”和“答案解析”留空、分值为 0；只有练习题和注意力题给出用于界面反馈的参考答案。每组材料的完整对话只放在 Q1，紧随其后的 Q2--Q5 使用“继续评价上述同一组对话”，导入后不要打乱这五行的相邻顺序。

## 已实现的冻结规则

1. Family A 15 题，覆盖 10 个 lesson，seed 42/43/44 各 5 题；
2. Family B 10 题，每个 lesson 一题，seed 分布为 3/3/4；
3. 每侧分别在有效轨迹 20%、50%、80% 附近寻找最近的跨角色相邻交换；
4. 每个窗口最多包含前置语境加一组相邻交换，每侧最多 9 条话语、450 个中文字符；
5. 系统匿名为对话 A/B，左右位置和参与者题序由固定 salt 决定；
6. 每个 item 恰好由两名参与者评价，每位参与者得到 3 个 A 类和 2 个 B 类题目；
7. 公开题库不包含 action、rationale、checkpoint、system ID 或源文件路径。

## 正式使用前

样例 HTML 不保存响应，它用于审核显示效果和迁移到问卷星、Qualtrics 等平台。正式发放前仍需：

- 录入方案中的人工练习题和注意力题；
- 完成手机/电脑界面 pilot；
- 冻结 salt、输入目录快照、题库哈希、问卷措辞与排除规则；
- 将 `sample_blind_mapping_private.csv` 与参与者作答数据分开保存；
- 按所在机构要求完成伦理审查或豁免确认。
