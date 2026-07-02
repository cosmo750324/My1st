import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt

# Define output path for the PPTX
output_dir = Path(__file__).parent
output_path = output_dir / "Zoo_Code_Weekly_Report_v2.pptx"

# Create a presentation object using optional template
template_path = Path(__file__).parent / "範本.pptx"
prs = Presentation(template_path) if template_path.is_file() else Presentation()
# Define layout for bullet slides (agenda, overview, etc.)
bullet_slide_layout = prs.slide_layouts[1] if len(prs.slide_layouts) > 1 else prs.slide_layouts[0]

# Title slide
title_slide_layout = prs.slide_layouts[0]
slide = prs.slides.add_slide(title_slide_layout)
# Set a light gray background for the slide
from pptx.dml.color import RGBColor
fill = slide.background.fill
fill.solid()
fill.fore_color.rgb = RGBColor(0xE0, 0xE0, 0xE0)
title = slide.shapes.title
subtitle = slide.placeholders[1]
title.text = "Zoo Code 週會報告"
title.text_frame.paragraphs[0].font.size = Pt(32)
subtitle.text = "介紹 Zoo Code 功能與應用"
subtitle.text_frame.paragraphs[0].font.size = Pt(16)

# Agenda slide
blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]
slide = prs.slides.add_slide(blank_layout)
# Set a light gray background for the slide
fill = slide.background.fill
fill.solid()
fill.fore_color.rgb = RGBColor(0xE0, 0xE0, 0xE0)
# Title textbox
title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(1))
title_tf = title_box.text_frame
title_tf.text = "議程"
title_tf.paragraphs[0].font.size = Pt(32)
# Body textbox
body_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(9), Inches(5))
body = body_box.text_frame
for point in [
    "Zoo Code 簡介",
    "核心功能與特性",
    "使用案例展示",
    "未來路線圖",
    "問答環節"
]:
    p = body.add_paragraph()
    p.font.size = Pt(16)
    p.text = point
    p.level = 0

# Zoo Code Overview slide
blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]
slide = prs.slides.add_slide(blank_layout)
# Set a light gray background for the slide
fill = slide.background.fill
fill.solid()
fill.fore_color.rgb = RGBColor(0xE0, 0xE0, 0xE0)
# Title textbox
title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(1))
title_tf = title_box.text_frame
title_tf.text = "Zoo Code 簡介"
title_tf.paragraphs[0].font.size = Pt(32)
# Body textbox
body_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(9), Inches(5))
body = body_box.text_frame
overview = [
    "一個高階的 AI 助手框架，支援多種模型與工具呼叫",
    "提供可重用的 Skill 與 Agent，快速建置 AI 應用",
    "整合 LLM、MCP、工具鏈，支援 Python、TypeScript 等語言",
    "可自訂 Prompt、情境管理與記憶功能"
]
for line in overview:
    p = body.add_paragraph()
    p.font.size = Pt(16)
    p.text = line
    p.level = 0

# Core Features slide
blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]
slide = prs.slides.add_slide(blank_layout)
# Set a light gray background for the slide
fill = slide.background.fill
fill.solid()
fill.fore_color.rgb = RGBColor(0xE0, 0xE0, 0xE0)
# Title textbox
title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(1))
title_tf = title_box.text_frame
title_tf.text = "核心功能與特性"
title_tf.paragraphs[0].font.size = Pt(32)
# Body textbox
body_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(9), Inches(5))
body = body_box.text_frame
features = [
    "多模型支援 (Anthropic, OpenAI, etc.)",
    "工具使用 (pip、git、docker 等) 自動化",
    "Skill 目錄，快速載入與組合",
    "記憶與上下文管理",
    "可視化與報告生成 (PDF, PPTX)"
]
for f in features:
    p = body.add_paragraph()
    p.font.size = Pt(16)
    p.text = f
    p.level = 0
    # Skill List slide
    blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]
    slide = prs.slides.add_slide(blank_layout)
    # Set a light gray background for the slide
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(0xE0, 0xE0, 0xE0)
    # Title textbox
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(1))
    title_tf = title_box.text_frame
    title_tf.text = "Skill 列表"
    title_tf.paragraphs[0].font.size = Pt(32)
    # Body textbox
    body_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(9), Inches(5))
    body = body_box.text_frame
    skills = [
        "claude-api: 提供與 Anthropic Claude 互動的 API 包裝與管理工具",
        "docx: 操作與轉換 Word 文件的腳本與工具",
        "frontend-design: 前端 UI/UX 設計資源與範例",
        "internal‑comms: 內部溝通與公告自動化範本",
        "mcp-builder: 建置 Model Context Protocol 伺服器與工具",
        "pdf: PDF 解析、填寫與驗證的腳本集合",
        "pptx: 產生與編輯 PowerPoint 簡報的工具",
        "skill-creator: 建立自訂 Skill 的腳本與範例",
        "slack‑gif‑creator: 產生 Slack 用 GIF 動畫的工具",
        "theme‑factory: 提供多種視覺主題樣式與範例",
        "web‑artifacts‑builder: 打包前端資產的腳本",
        "webapp‑testing: 網頁應用測試腳本與範例",
        "xlsx: 處理 Excel 檔案的工具與腳本"
    ]
    for s in skills:
        p = body.add_paragraph()
        p.font.size = Pt(16)
        p.text = s
        p.level = 0

# Usage Example slide
blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]
slide = prs.slides.add_slide(blank_layout)
# Set a light gray background for the slide
fill = slide.background.fill
fill.solid()
fill.fore_color.rgb = RGBColor(0xE0, 0xE0, 0xE0)
# Title textbox
title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(1))
title_tf = title_box.text_frame
title_tf.text = "使用案例展示"
title_tf.paragraphs[0].font.size = Pt(32)
# Body textbox
body_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(9), Inches(5))
body = body_box.text_frame
example = [
    "透過簡單的 SKILL.md 定義，即可產生 PDF/PowerPoint 報告",
    "結合 `zoo/skills-main/skills/pptx` 產生會議簡報",
    "結合 `zoo/skills-main/skills/pdf` 產生 PDF 文件"
]
for e in example:
    p = body.add_paragraph()
    p.font.size = Pt(16)
    p.text = e
    p.level = 0

# Future Roadmap slide
blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]
slide = prs.slides.add_slide(blank_layout)
# Set a light gray background for the slide
fill = slide.background.fill
fill.solid()
fill.fore_color.rgb = RGBColor(0xE0, 0xE0, 0xE0)
# Title textbox
title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(1))
title_tf = title_box.text_frame
title_tf.text = "未來路線圖"
title_tf.paragraphs[0].font.size = Pt(32)
# Body textbox
body_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(9), Inches(5))
body = body_box.text_frame
roadmap = [
    "擴充更多模型支援",
    "提升工具自動化能力",
    "增強安全與合規功能",
    "提供圖形化 UI 管理介面"
]
for r in roadmap:
    p = body.add_paragraph()
    p.font.size = Pt(16)
    p.text = r
    p.level = 0

# Q&A slide
blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]
slide = prs.slides.add_slide(blank_layout)
# Set a light gray background for the slide
fill = slide.background.fill
fill.solid()
fill.fore_color.rgb = RGBColor(0xE0, 0xE0, 0xE0)
# Title textbox
title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(1))
title_tf = title_box.text_frame
title_tf.text = "問答環節"
title_tf.paragraphs[0].font.size = Pt(32)
# Body textbox
body_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(9), Inches(5))
body = body_box.text_frame
p = body.add_paragraph()
p.font.size = Pt(16)
p.text = "感謝聆聽，歡迎提問！"

# Save the presentation
prs.save(output_path)
print(f"PPTX 已產生於 {output_path}")
