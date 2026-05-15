# Community Schema

## Domain: SeeDAO

## Conventions
- File names: lowercase, hyphens, no spaces
- Every page starts with YAML frontmatter
- Use [[wikilinks]] to link between pages
- _data/ is machine-generated; edit Markdown files instead
- log.md is append-only

## Page Types
- `community` — 社区主页
- `person` — 成员页
- `event` — Event 页
- `graph` — 关系图谱
- `state` — 状态记录
- `log` — 操作日志

## Digital Twin（数字分身）

### Person JSON 扩展字段
每个 `_data/people/<id>.json` 可包含以下可选字段用于数字分身：

```json
{
  "style": {
    "writing_style": ["标签1", "标签2"],
    "core_themes": ["主题1", "主题2"],
    "tone": "语气描述",
    "signature_metaphors": ["常用比喻1"],
    "typical_openings": "典型开头方式",
    "influence": ["影响力来源"],
    "source_articles": ["来源文章ID1"]
  },
  "speech_samples": [
    {
      "source": "来源描述",
      "text": "原文片段",
      "features": ["风格特征标签"]
    }
  ]
}
```

### Persona Prompt 模板
数字分身的使用方式：在 AstrBot 人格系统提示词中引用。
模板路径：`_data/personas/<id>.prompt.md`

### 文件结构
- `_data/people/<id>.json` — 含 style 字段的成员档案
- `_data/personas/<id>.prompt.md` — 数字分身人格提示词
- `_data/personas/<id>.samples.json` — 风格示例数据集

