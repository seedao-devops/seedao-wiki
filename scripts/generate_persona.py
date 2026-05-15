#!/usr/bin/env python3
"""
数字分身生成器 — 为社区成员生成数字分身（Persona）
使用方法：
  python3 generate_persona.py --person 唐晗          # 为指定成员生成
  python3 generate_persona.py --list                   # 列出已有分身的成员
  python3 generate_persona.py --all                    # 为所有有 style 字段的成员生成
"""

import json
import os
import sys
from pathlib import Path

# 路径
WIKI_DIR = Path("/AstrBot/data/seedao-wiki")
PEOPLE_DIR = WIKI_DIR / "_data" / "people"
PERSONAS_DIR = WIKI_DIR / "_data" / "personas"

PERSONA_TEMPLATE = """# {name}数字分身人格提示词

## 身份设定

你是**{name}** — {role}
{bio}

## 核心信念

{beliefs}

## 语言风格

{style_points}

## 表达习惯

{habits}

## 知识领域

{knowledge}

## 对话禁忌

{taboos}

## Few-shot 示例

{few_shots}

## 调用方式

在 AstrBot 人格系统提示词中直接引用此文件内容。
"""


def load_person(person_id: str) -> dict | None:
    """加载成员数据"""
    path = PEOPLE_DIR / f"{person_id}.json"
    if not path.exists():
        print(f"❌ 未找到成员: {person_id}")
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def list_personas() -> list[str]:
    """列出已有数字分身的成员"""
    if not PERSONAS_DIR.exists():
        return []
    return sorted([
        f.stem.replace(".prompt", "")
        for f in PERSONAS_DIR.glob("*.prompt.md")
    ])


def has_style_data(person: dict) -> bool:
    """检查成员是否有 style 数据"""
    return bool(person.get("style")) or bool(person.get("speech_samples"))


def generate_persona(person_id: str, force: bool = False) -> bool:
    """为指定成员生成数字分身"""
    person = load_person(person_id)
    if not person:
        return False

    if not has_style_data(person) and not force:
        print(f"⚠️  {person_id} 缺少 style 数据，跳过。使用 --force 强制生成基础版。")
        return False

    profile = person.get("profile", {})
    style = person.get("style", {})
    samples = person.get("speech_samples", [])

    name = profile.get("name", person_id)
    role = profile.get("role", "社区成员")
    bio = profile.get("bio", f"{name} 是 SeeDAO 社区成员。")

    # 构建核心信念
    beliefs = style.get("core_themes", [])
    if beliefs:
        beliefs_text = "\n".join([f"- {b}" for b in beliefs[:5]])
    else:
        beliefs_text = "- 参与 SeeDAO 社区建设\n- Web3 与数字城邦"

    # 构建风格描述
    style_points = style.get("writing_style", [])
    if style_points:
        style_text = "\n".join([f"- {s}" for s in style_points[:6]])
    else:
        style_text = "- 暂无详细风格分析"

    # 构建表达习惯
    tone = style.get("tone", "真诚的表达者")
    metaphors = style.get("signature_metaphors", [])
    habits = [f"- 语气：{tone}"]
    if metaphors:
        habits.append(f"- 常用比喻：{', '.join(metaphors[:4])}")
    habits_text = "\n".join(habits)

    # 构建知识领域
    skills = person.get("skills", [])
    interests = person.get("interests", [])
    knowledge = skills + interests
    if knowledge:
        knowledge_text = "\n".join([f"- {k}" for k in knowledge[:6]])
    else:
        knowledge_text = "- 社区参与者"

    # 构建 few-shot 示例
    if samples:
        few_shots = ""
        for i, s in enumerate(samples[:3]):
            few_shots += f"""用户问相关问题时的回答示例（来源：{s['source']}）：

"{s['text']}"

风格特征：{', '.join(s.get('features', ['待分析']))}

"""
    else:
        few_shots = "（暂无示例数据，建议补充 speech_samples）"

    # 构建对话禁忌
    taboos = "- 不要表现得像一个纯粹的技术专家\n- 不要忽视人的情感和心灵层面"

    # 渲染模板
    content = PERSONA_TEMPLATE.format(
        name=name,
        role=role,
        bio=bio,
        beliefs=beliefs_text,
        style_points=style_text,
        habits=habits_text,
        knowledge=knowledge_text,
        taboos=taboos,
        few_shots=few_shots,
    )

    # 写入文件
    PERSONAS_DIR.mkdir(parents=True, exist_ok=True)
    prompt_path = PERSONAS_DIR / f"{person_id}.prompt.md"
    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ 已生成数字分身: {name}")
    print(f"   提示词: {prompt_path}")
    if samples:
        print(f"   风格示例: {len(samples)} 条")
    return True


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 generate_persona.py --person <ID>")
        print("  python3 generate_persona.py --list")
        print("  python3 generate_persona.py --all")
        print("  python3 generate_persona.py --force --person <ID>")
        return

    if "--list" in sys.argv:
        personas = list_personas()
        if personas:
            print("已有数字分身的成员:")
            for p in personas:
                print(f"  ✅ {p}")
        else:
            print("暂无数字分身。")
        return

    if "--all" in sys.argv:
        force = "--force" in sys.argv
        generated = 0
        skipped = 0
        for f in sorted(PEOPLE_DIR.glob("*.json")):
            pid = f.stem
            if generate_persona(pid, force):
                generated += 1
            else:
                skipped += 1
        print(f"\n📊 总计: {generated} 生成, {skipped} 跳过")
        return

    if "--person" in sys.argv:
        idx = sys.argv.index("--person")
        if idx + 1 < len(sys.argv):
            person_id = sys.argv[idx + 1]
            force = "--force" in sys.argv
            generate_persona(person_id, force)
            return

    print("❌ 参数错误，请使用 --help 查看用法。")


if __name__ == "__main__":
    main()
