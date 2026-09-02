#!/usr/bin/env python3
"""Build a blinded G4 teacher-evaluation item bank and sample questionnaire.

The implementation follows todo/G4_TEACHER_HUMAN_EVALUATION_PLAN.md.  It uses
only Python's standard library so the frozen bank can be rebuilt without adding
project dependencies.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import random
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


SYSTEM_DIRS = {
    "full_direct": "sft_stage3_direct",
    "full_candidate": "sft_stage3",
    "wotd_direct": "sft_stage3_woTD_direct",
}
FAMILIES = {
    "A": ("full_direct", "full_candidate", 15, {42: 5, 43: 5, 44: 5}),
    "B": ("full_direct", "wotd_direct", 10, {42: 3, 43: 3, 44: 4}),
}
ASSIGNMENT = {
    "P01": ([1, 2, 3], [1, 2]),
    "P02": ([1, 4, 5], [1, 3]),
    "P03": ([2, 4, 6], [2, 4]),
    "P04": ([3, 5, 6], [3, 4]),
    "P05": ([7, 8, 9], [5, 6]),
    "P06": ([7, 10, 11], [5, 7]),
    "P07": ([8, 10, 12], [6, 8]),
    "P08": ([9, 11, 13], [7, 9]),
    "P09": ([12, 14, 15], [8, 10]),
    "P10": ([13, 14, 15], [9, 10]),
}
ANCHORS = (("前段", 0.20), ("中段", 0.50), ("后段", 0.80))
SCHEMA_VERSION = "g4-teacher-bank-v1"
CSV_COLUMNS = [
    "题型", "题目", "选项1", "选项2", "选项3", "选项4", "选项5", "选项6",
    "答案", "答案解析", "分值",
]
PAIR_SCALE = ["A 好很多", "A 好一点", "两段差不多", "B 好一点", "B 好很多", "看不出来"]


@dataclass(frozen=True)
class Trajectory:
    system: str
    lesson_id: int
    seed: int
    subject: str
    grade: str
    stage: str
    topic: str
    source_path: Path
    utterances: tuple[dict[str, str], ...]


def stable_digest(*parts: object) -> str:
    raw = "|".join(str(p) for p in parts).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_role(value: Any) -> str:
    role = str(value or "").strip()
    if role in {"老师", "教师", "teacher", "Teacher"}:
        return "老师"
    if role in {"学生", "student", "Student"}:
        return "学生"
    return role or "未知说话人"


def clean_utterance(value: Any) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    text = re.sub(r"^(老师|教师|学生)\s*[：:]\s*", "", text)
    return text


def load_trajectory(path: Path, system: str) -> Trajectory:
    data = json.loads(path.read_text(encoding="utf-8"))
    meta = data.get("meta") or {}
    turns: list[dict[str, str]] = []
    for record in data.get("turn_records") or []:
        utterance = clean_utterance(record.get("selected_utterance"))
        role = normalize_role(record.get("role"))
        if not utterance or utterance.upper() == "END":
            continue
        # Exclude obvious serialization leakage while retaining ordinary failures.
        if "<ACTION>" in utterance or "<RATIONALE>" in utterance:
            continue
        turns.append({"role": role, "text": utterance})
    if len(turns) < 8:
        raise ValueError(f"Too few valid turns in {path}: {len(turns)}")
    return Trajectory(
        system=system,
        lesson_id=int(data["lesson_id"]),
        seed=int(data.get("generation_seed", data.get("model_seed"))),
        subject=str(meta.get("subject") or "未知学科"),
        grade=str(meta.get("grade") or "未知年级"),
        stage=str(meta.get("stage") or "未知学段"),
        topic=str(meta.get("name") or f"课程 {data['lesson_id']}"),
        source_path=path,
        utterances=tuple(turns),
    )


def discover(root: Path) -> dict[tuple[str, int, int], Trajectory]:
    found: dict[tuple[str, int, int], Trajectory] = {}
    for system, dirname in SYSTEM_DIRS.items():
        directory = root / dirname
        if not directory.is_dir():
            raise FileNotFoundError(f"Missing trajectory directory: {directory}")
        for path in sorted(directory.glob("seed*/*.json")):
            traj = load_trajectory(path, system)
            key = (system, traj.lesson_id, traj.seed)
            if key in found:
                raise ValueError(f"Duplicate trajectory key: {key}")
            found[key] = traj
    return found


def nearest_exchange(turns: tuple[dict[str, str], ...], fraction: float) -> list[dict[str, str]]:
    target = round(fraction * (len(turns) - 1))
    candidates = [i for i in range(len(turns) - 1) if turns[i]["role"] != turns[i + 1]["role"]]
    if not candidates:
        raise ValueError("Trajectory has no adjacent cross-role exchange")
    start = min(candidates, key=lambda i: (abs(i - target), i))
    indices = [start, start + 1]
    if start > 0:
        indices.insert(0, start - 1)
    return [dict(turns[i]) for i in indices]


def cap_window_text(windows: list[dict[str, Any]], limit: int) -> None:
    utterances = [u for w in windows for u in w["utterances"]]
    total = sum(len(u["text"]) for u in utterances)
    if total <= limit:
        return
    cap = max(18, limit // len(utterances))
    for utterance in utterances:
        text = utterance["text"]
        if len(text) > cap:
            utterance["text"] = text[: cap - 1].rstrip() + "…"
            utterance["truncated"] = True


def extract_windows(traj: Trajectory, char_limit: int) -> list[dict[str, Any]]:
    windows = [
        {"stage": label, "anchor_fraction": fraction, "utterances": nearest_exchange(traj.utterances, fraction)}
        for label, fraction in ANCHORS
    ]
    cap_window_text(windows, char_limit)
    return windows


def balanced_seed_map(lessons: list[int], counts: dict[int, int], salt: str) -> dict[int, int]:
    if sum(counts.values()) != len(lessons):
        raise ValueError("Seed counts must equal number of lessons")
    ordered_lessons = sorted(lessons, key=lambda lesson: stable_digest(salt, "lesson", lesson))
    seed_slots = [seed for seed, count in sorted(counts.items()) for _ in range(count)]
    # A local RNG gives a stable balanced assignment without touching global state.
    random.Random(int(stable_digest(salt)[:16], 16)).shuffle(seed_slots)
    return dict(zip(ordered_lessons, seed_slots))


def select_pairs(
    trajectories: dict[tuple[str, int, int], Trajectory], family: str, salt: str
) -> list[tuple[int, int]]:
    target, control, count, seed_targets = FAMILIES[family]
    available = sorted(
        (lesson, seed)
        for system, lesson, seed in trajectories
        if system == target and (control, lesson, seed) in trajectories
    )
    lessons = sorted({lesson for lesson, _ in available})
    if len(lessons) != 10:
        raise ValueError(f"Family {family} requires 10 paired lessons; found {len(lessons)}")
    if family == "B":
        mapping = balanced_seed_map(lessons, seed_targets, f"{salt}-B-base")
        selected = [(lesson, mapping[lesson]) for lesson in lessons]
    else:
        base_counts = {42: 3, 43: 3, 44: 4}
        base = balanced_seed_map(lessons, base_counts, f"{salt}-A-base")
        selected = [(lesson, base[lesson]) for lesson in lessons]
        remaining = {seed: seed_targets[seed] - base_counts[seed] for seed in seed_targets}
        extra_seeds = [seed for seed, n in sorted(remaining.items()) for _ in range(n)]
        extra_seeds.sort(key=lambda seed: stable_digest(salt, "A-extra-seed", seed))
        eligible = sorted(lessons, key=lambda lesson: stable_digest(salt, "A-extra-lesson", lesson))
        used_lessons: set[int] = set()
        for seed in extra_seeds:
            lesson = next(
                lesson for lesson in eligible if lesson not in used_lessons and base[lesson] != seed
            )
            used_lessons.add(lesson)
            selected.append((lesson, seed))
    selected.sort(key=lambda pair: stable_digest(salt, family, pair[0], pair[1]))
    if len(selected) != count or len(set(selected)) != count:
        raise AssertionError(f"Invalid selection for family {family}")
    actual_counts = {seed: sum(s == seed for _, s in selected) for seed in seed_targets}
    if actual_counts != seed_targets:
        raise AssertionError(f"Unbalanced seeds for family {family}: {actual_counts}")
    return selected


def build_item(
    trajectories: dict[tuple[str, int, int], Trajectory], family: str, ordinal: int,
    lesson: int, seed: int, salt: str, char_limit: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    target, control, _, _ = FAMILIES[family]
    systems = [target, control]
    left_target = int(stable_digest(salt, family, lesson, seed, "side")[:8], 16) % 2 == 0
    left_system, right_system = (target, control) if left_target else (control, target)
    exemplar = trajectories[(target, lesson, seed)]
    item_id = f"{family}{ordinal:02d}"
    public = {
        "schema_version": SCHEMA_VERSION,
        "item_id": item_id,
        "comparison_family": family,
        "lesson_id": lesson,
        "generation_seed": seed,
        "grade_band": exemplar.stage,
        "grade": exemplar.grade,
        "subject": exemplar.subject,
        "topic": exemplar.topic,
        "left_blind_id": f"{item_id}-A",
        "right_blind_id": f"{item_id}-B",
        "dialogue_A": extract_windows(trajectories[(left_system, lesson, seed)], char_limit),
        "dialogue_B": extract_windows(trajectories[(right_system, lesson, seed)], char_limit),
    }
    private = {
        "item_id": item_id,
        "comparison_family": family,
        "lesson_id": lesson,
        "generation_seed": seed,
        "target_system": target,
        "control_system": control,
        "dialogue_A_system": left_system,
        "dialogue_B_system": right_system,
        "order_code": "target-left" if left_system == target else "target-right",
        "target_source": "/".join(trajectories[(target, lesson, seed)].source_path.parts[-3:]),
        "control_source": "/".join(trajectories[(control, lesson, seed)].source_path.parts[-3:]),
    }
    assert set(systems) == {left_system, right_system}
    return public, private


def questionnaire_questions() -> list[tuple[str, str]]:
    return [
        ("Q1", "总的来看，哪段对话更能把知识点讲开、讲清楚，并把前后的内容连起来？"),
        ("Q2", "哪段对话后面说的话更能接住前面的内容，并继续往下讲？"),
        ("Q3", "哪段对话更符合这个年级、学科和主题，也更少出现明显错误或跑题？"),
        ("Q4", "哪段对话较少反复说同样的话，而且能继续增加有用的新内容？"),
        ("Q5", "您对刚才的判断有多大把握？（没太大把握 / 有一些把握 / 很有把握）"),
    ]


def dialogue_markdown(label: str, windows: list[dict[str, Any]]) -> str:
    lines = [f"#### 对话 {label}"]
    for window in windows:
        lines.append(f"\n**{window['stage']}**")
        for utterance in window["utterances"]:
            lines.append(f"- {utterance['role']}：{utterance['text']}")
    return "\n".join(lines)


def dialogue_plain(label: str, windows: list[dict[str, Any]]) -> str:
    lines = [f"【对话 {label}】"]
    for window in windows:
        lines.append(f"［{window['stage']}］")
        lines.extend(f"{u['role']}：{u['text']}" for u in window["utterances"])
    return "\n".join(lines)


def stimulus_plain(item: dict[str, Any], display_name: str) -> str:
    return "\n".join([
        f"【{display_name}】",
        f"年级阶段：{item['grade_band']}（{item['grade']}）",
        f"学科：{item['subject']}",
        f"主题：{item['topic']}",
        "",
        dialogue_plain("A", item["dialogue_A"]),
        "",
        dialogue_plain("B", item["dialogue_B"]),
    ])


def csv_row(
    question_type: str, question: str, options: Iterable[str] = (), answer: str = "",
    explanation: str = "", score: str = "0",
) -> dict[str, str]:
    values = list(options)
    if len(values) > 6:
        raise ValueError("CSV import format supports at most six options")
    row = {column: "" for column in CSV_COLUMNS}
    row.update({"题型": question_type, "题目": question, "答案": answer, "答案解析": explanation, "分值": score})
    for index, option in enumerate(values, 1):
        row[f"选项{index}"] = option
    return row


def formal_csv_rows(items: list[dict[str, Any]], labels: list[str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    questions = questionnaire_questions()
    for item, label in zip(items, labels):
        stimulus = stimulus_plain(item, label)
        for index, (qid, question) in enumerate(questions):
            if index == 0:
                stem = f"{stimulus}\n\n{qid}　{question}"
            else:
                stem = f"【{label}：继续评价上述同一组对话】\n{qid}　{question}"
            options = ["没太大把握", "有一些把握", "很有把握"] if qid == "Q5" else PAIR_SCALE
            rows.append(csv_row("单选题", stem, options))
    return rows


def write_import_csv(path: Path, rows: list[dict[str, str]]) -> None:
    # utf-8-sig lets Excel and common Chinese survey platforms detect UTF-8.
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sample_questionnaire_csv_rows(items: list[dict[str, Any]]) -> list[dict[str, str]]:
    rows = [
        csv_row("单选题", "参与同意：我愿意参加这项匿名问卷。选择“不愿意”后应由问卷平台结束问卷。", ["愿意", "不愿意"]),
        csv_row("单选题", "您教书多少年了？", ["8–10 年", "11–15 年", "16–20 年", "20 年以上"]),
        csv_row("单选题", "您主要教哪个阶段？", ["小学", "初中", "高中", "多个阶段"]),
        csv_row("多选题", "您主要教什么学科？", ["语文", "数学", "物理", "化学", "其他"]),
        csv_row("单选题", "您现在主要从事什么工作？", ["课堂教学", "教研并兼任教学", "教学管理并兼任教学", "其他"]),
        csv_row("单选题", "您平时使用 AI 工具帮助教学吗？", ["从不", "偶尔", "每月几次", "每周或更频繁"]),
        csv_row(
            "单选题",
            "练习题：对话 A 反复问答而没有继续解释；对话 B 从温度升高继续讲到水分子运动、气泡形成并给出烧水实例。哪段对话较少重复，而且能继续增加有用的新内容？",
            PAIR_SCALE, answer="E", explanation="练习反馈：应选择‘B 好很多’，本题不计入正式结果。",
        ),
    ]
    for index, item in enumerate(items, 1):
        rows.extend(formal_csv_rows([item], [f"正式题 {index}"]))
        if index == 3:
            rows.append(csv_row(
                "单选题",
                "注意力题（不计分）：对话 A 连续两次重复同一句话；对话 B 紧扣主题补充了解释和例子。哪段对话较少重复？",
                PAIR_SCALE, answer="E", explanation="应选择‘B 好很多’；本题仅用于注意力检查。",
            ))
    rows.extend([
        csv_row("单选题", "这些对话片段够不够您作出判断？", ["完全不够", "不太够", "基本够", "比较够", "完全够"]),
        csv_row("问答题", "可选：您主要根据什么作出判断？还有什么想告诉我们？（最多 100 字）"),
    ])
    return rows


def build_markdown(participant: str, items: list[dict[str, Any]]) -> str:
    lines = [
        f"# G4 教师评价样例问卷（{participant}）",
        "",
        "> 这是由冻结题库自动生成的预览。正式发放时应由问卷平台记录同意、背景、答案和用时。",
        "",
        "## 首页与同意",
        "",
        "您将看到几组匿名中小学课堂对话，请比较哪一段讲得更清楚、更连贯，也更少跑题或重复。问卷约需 10–15 分钟，不收集姓名、学校名称或学生信息。",
        "",
        "- [ ] 我愿意参加这项匿名问卷。",
        "",
        "## 背景信息",
        "",
        "1. 教学年限：8–10 年 / 11–15 年 / 16–20 年 / 20 年以上；",
        "2. 主要学段：小学 / 初中 / 高中 / 多个阶段；",
        "3. 主要学科：语文 / 数学 / 物理 / 化学 / 其他；",
        "4. 当前工作：课堂教学 / 教研并兼任教学 / 教学管理并兼任教学 / 其他；",
        "5. AI 教学工具使用：从不 / 偶尔 / 每月几次 / 每周或更频繁。",
        "",
        "## 作答说明",
        "",
        "每题两段对话来自同一年级、学科和主题。文本较长或专业词较多不一定更好；若材料不足，请选择“看不出来”。",
        "",
        "## 练习题",
        "",
        "**对话 A**：老师反复问“水为什么会沸腾？”，学生反复回答“因为温度高了”，没有继续解释。",
        "",
        "**对话 B**：老师从温度升高追问到水分子运动和气泡形成，学生用生活中的烧水现象举例说明。",
        "",
        "练习问题：哪段对话较少重复，而且能接着前面的内容继续解释？",
        "",
        "> 练习反馈：通常应选择对话 B；本题不计入正式结果。",
    ]
    for number, item in enumerate(items, 1):
        lines += [
            "",
            f"## 正式题 {number}",
            "",
            f"年级阶段：{item['grade_band']}（{item['grade']}）",
            f"学科：{item['subject']}",
            f"这节课讲什么：{item['topic']}",
            "",
            dialogue_markdown("A", item["dialogue_A"]),
            "",
            dialogue_markdown("B", item["dialogue_B"]),
            "",
        ]
        for qid, text in questionnaire_questions():
            if qid == "Q5":
                lines.append(f"- **{qid}** {text}")
            else:
                lines.append(f"- **{qid}** {text}")
                lines.append("  A 好很多 / A 好一点 / 两段差不多 / B 好一点 / B 好很多 / 看不出来")
        if number == 3:
            lines += [
                "", "### 注意力题（不计分）", "",
                "对话 A 连续两次重复同一句话；对话 B 紧扣主题补充了解释和例子。哪段对话较少重复？",
                "", "A 好很多 / A 好一点 / 两段差不多 / B 好一点 / B 好很多 / 看不出来",
            ]
    lines += [
        "",
        "## 末页",
        "",
        "1. 这些对话片段够不够您作出判断？",
        "2. 可选：您主要根据什么作出判断？还有什么想告诉我们？（最多 100 字）",
    ]
    return "\n".join(lines) + "\n"


def render_dialogue_html(label: str, windows: list[dict[str, Any]]) -> str:
    sections = []
    for window in windows:
        utterances = "".join(
            f'<p><strong>{html.escape(u["role"])}</strong>：{html.escape(u["text"])}</p>'
            for u in window["utterances"]
        )
        sections.append(f'<section class="window"><h4>{html.escape(window["stage"])}</h4>{utterances}</section>')
    return f'<article class="dialogue"><h3>对话 {label}</h3>{"".join(sections)}</article>'


def build_html(participant: str, items: list[dict[str, Any]]) -> str:
    scale = ["A 好很多", "A 好一点", "两段差不多", "B 好一点", "B 好很多", "看不出来"]
    cards = []
    for number, item in enumerate(items, 1):
        questions = []
        for qid, question in questionnaire_questions()[:4]:
            radios = "".join(
                f'<label><input type="radio" name="item{number}-{qid}" value="{html.escape(option)}"> {html.escape(option)}</label>'
                for option in scale
            )
            questions.append(f'<fieldset><legend>{qid} {html.escape(question)}</legend><div class="scale">{radios}</div></fieldset>')
        questions.append(
            f'<fieldset><legend>Q5 您对刚才的判断有多大把握？</legend><div class="scale">'
            + "".join(f'<label><input type="radio" name="item{number}-Q5"> {x}</label>' for x in ["没太大把握", "有一些把握", "很有把握"])
            + "</div></fieldset>"
        )
        cards.append(
            f'<section class="item"><h2>正式题 {number}</h2><p class="meta">年级阶段：{html.escape(item["grade_band"])}（{html.escape(item["grade"])}） · 学科：{html.escape(item["subject"])} · 主题：{html.escape(item["topic"])}</p>'
            f'<div class="pair">{render_dialogue_html("A", item["dialogue_A"])}{render_dialogue_html("B", item["dialogue_B"])}</div>{"".join(questions)}</section>'
        )
        if number == 3:
            attention_radios = "".join(
                f'<label><input type="radio" name="attention" value="{html.escape(option)}"> {html.escape(option)}</label>'
                for option in scale
            )
            cards.append(
                '<section class="item"><h2>注意力题（不计分）</h2>'
                '<p><strong>对话 A</strong> 连续两次重复同一句话；<strong>对话 B</strong> 紧扣主题补充了解释和例子。</p>'
                f'<fieldset><legend>哪段对话较少重复？</legend><div class="scale">{attention_radios}</div></fieldset></section>'
            )
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>G4 教师评价样例问卷 {html.escape(participant)}</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif;max-width:1100px;margin:auto;padding:24px;color:#202124;line-height:1.55;background:#f7f8fa}}
header,.item{{background:white;border:1px solid #dfe3e8;border-radius:12px;padding:22px;margin:18px 0}} .pair{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.dialogue{{border:1px solid #c9d2dc;border-radius:9px;padding:14px}} .window{{border-top:1px solid #edf0f2}} .window:first-of-type{{border-top:0}}
.meta{{color:#465364}} fieldset{{border:0;border-top:1px solid #e6e8eb;margin-top:18px;padding:16px 0}} legend{{font-weight:600}}
.scale{{display:flex;flex-wrap:wrap;gap:12px;margin-top:10px}} label{{background:#f1f4f7;padding:7px 10px;border-radius:7px}}
@media(max-width:760px){{.pair{{grid-template-columns:1fr}} body{{padding:10px}}}}
</style></head><body>
<header><h1>G4 教师评价样例问卷</h1><p>参与者版本：{html.escape(participant)}。本页仅供预览，不会保存答案。</p>
<p>您将看到几组匿名中小学课堂对话。问卷约需 10–15 分钟，不收集姓名、学校名称或学生信息，您可以随时退出。</p>
<fieldset><legend>参与同意</legend><label><input type="radio" name="consent" value="yes"> 我愿意参加</label> <label><input type="radio" name="consent" value="no"> 我不愿意参加</label></fieldset></header>
<section class="item"><h2>背景信息</h2>
<p><label>教学年限：<select><option>请选择</option><option>8–10 年</option><option>11–15 年</option><option>16–20 年</option><option>20 年以上</option></select></label></p>
<p><label>主要学段：<select><option>请选择</option><option>小学</option><option>初中</option><option>高中</option><option>多个阶段</option></select></label></p>
<p><label>主要学科：<input type="text" placeholder="如：语文、数学、物理"></label></p>
<p><label>当前工作：<select><option>课堂教学</option><option>教研并兼任教学</option><option>教学管理并兼任教学</option><option>其他</option></select></label></p>
<p><label>AI 教学工具使用：<select><option>从不</option><option>偶尔</option><option>每月几次</option><option>每周或更频繁</option></select></label></p></section>
<section class="item"><h2>作答说明与练习</h2><p>每题两段对话来自同一年级、学科和主题。文本更长、专业词更多不一定更好；如果材料不足，请选择“看不出来”。</p>
<div class="pair"><article class="dialogue"><h3>练习对话 A</h3><p>老师反复询问“水为什么会沸腾？”，学生反复回答“因为温度高了”，没有继续解释。</p></article>
<article class="dialogue"><h3>练习对话 B</h3><p>老师从温度升高追问到水分子运动和气泡形成，学生用生活中的烧水现象举例说明。</p></article></div>
<p><strong>练习反馈：</strong>通常应选择对话 B；练习题不计入正式结果。</p></section>
{"".join(cards)}
<section class="item"><h2>末页</h2><fieldset><legend>这些对话片段够不够您作出判断？</legend><div class="scale">{''.join(f'<label><input type="radio" name="sufficiency"> {x}</label>' for x in ['完全不够','不太够','基本够','比较够','完全够'])}</div></fieldset>
<p><label>可选：您主要根据什么作出判断？还有什么想告诉我们？<br><textarea maxlength="100" rows="4" style="width:100%"></textarea></label></p></section>
</body></html>"""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate(items: list[dict[str, Any]], assignments: list[dict[str, str]]) -> dict[str, Any]:
    errors: list[str] = []
    ids = [item["item_id"] for item in items]
    if len(ids) != 25 or len(set(ids)) != 25:
        errors.append("Expected 25 unique items")
    for family, expected in (("A", 15), ("B", 10)):
        subset = [item for item in items if item["comparison_family"] == family]
        if len(subset) != expected:
            errors.append(f"Family {family}: expected {expected}, got {len(subset)}")
        if len({item["lesson_id"] for item in subset}) != 10:
            errors.append(f"Family {family}: does not cover 10 lessons")
    counts: dict[str, int] = {}
    for row in assignments:
        counts[row["item_id"]] = counts.get(row["item_id"], 0) + 1
    if any(counts.get(item_id) != 2 for item_id in ids):
        errors.append("Every item must be assigned exactly twice")
    participant_counts: dict[str, int] = {}
    for row in assignments:
        participant_counts[row["participant_id"]] = participant_counts.get(row["participant_id"], 0) + 1
    if any(value != 5 for value in participant_counts.values()) or len(participant_counts) != 10:
        errors.append("Every one of 10 participants must receive five items")
    for item in items:
        for side in ("dialogue_A", "dialogue_B"):
            windows = item[side]
            if [w["stage"] for w in windows] != ["前段", "中段", "后段"]:
                errors.append(f"{item['item_id']} {side}: invalid stages")
            chars = sum(len(u["text"]) for w in windows for u in w["utterances"])
            if chars > 450:
                errors.append(f"{item['item_id']} {side}: {chars} chars exceeds 450")
    return {"valid": not errors, "errors": errors, "items": len(items), "assignments": len(assignments)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trajectory-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--salt", default="g4-teacher-eval-v1-20260902")
    parser.add_argument("--sample-participant", default="P01", choices=sorted(ASSIGNMENT))
    parser.add_argument("--char-limit", type=int, default=450)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    trajectories = discover(args.trajectory_root)

    items: list[dict[str, Any]] = []
    private_rows: list[dict[str, Any]] = []
    for family in ("A", "B"):
        for ordinal, (lesson, seed) in enumerate(select_pairs(trajectories, family, args.salt), 1):
            public, private = build_item(trajectories, family, ordinal, lesson, seed, args.salt, args.char_limit)
            items.append(public)
            private_rows.append(private)
    items.sort(key=lambda item: item["item_id"])
    by_id = {item["item_id"]: item for item in items}

    bank_path = args.output_dir / "sample_item_bank.jsonl"
    with bank_path.open("w", encoding="utf-8") as handle:
        for item in items:
            handle.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")
    private_path = args.output_dir / "sample_blind_mapping_private.csv"
    with private_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(private_rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(private_rows)

    assignment_rows: list[dict[str, str]] = []
    for participant, (a_numbers, b_numbers) in ASSIGNMENT.items():
        item_ids = [*(f"A{x:02d}" for x in a_numbers), *(f"B{x:02d}" for x in b_numbers)]
        rng = random.Random(int(stable_digest(args.salt, participant, "question-order")[:16], 16))
        rng.shuffle(item_ids)
        for order, item_id in enumerate(item_ids, 1):
            assignment_rows.append({"participant_id": participant, "question_order": str(order), "item_id": item_id})
    assignment_path = args.output_dir / "sample_assignment_manifest.csv"
    with assignment_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["participant_id", "question_order", "item_id"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(assignment_rows)

    sample_ids = [
        row["item_id"] for row in sorted(assignment_rows, key=lambda row: int(row["question_order"]))
        if row["participant_id"] == args.sample_participant
    ]
    sample_items = [by_id[item_id] for item_id in sample_ids]
    (args.output_dir / "sample_questionnaire.md").write_text(
        build_markdown(args.sample_participant, sample_items), encoding="utf-8"
    )
    (args.output_dir / "sample_questionnaire.html").write_text(
        build_html(args.sample_participant, sample_items), encoding="utf-8"
    )
    write_import_csv(
        args.output_dir / "sample_item_bank_import.csv",
        formal_csv_rows(items, [f"题库材料 {item['item_id']}" for item in items]),
    )
    write_import_csv(
        args.output_dir / f"sample_questionnaire_{args.sample_participant}_import.csv",
        sample_questionnaire_csv_rows(sample_items),
    )

    report = validate(items, assignment_rows)
    report.update({
        "schema_version": SCHEMA_VERSION,
        "salt": args.salt,
        "trajectory_root_name": args.trajectory_root.name,
        "trajectory_count_loaded": len(trajectories),
        "sample_participant": args.sample_participant,
        "item_bank_sha256": sha256_file(bank_path),
    })
    write_json(args.output_dir / "validation_report.json", report)
    if not report["valid"]:
        raise SystemExit("Validation failed: " + "; ".join(report["errors"]))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
