---
name: bot-brand-styling
description: |
  Applies the Bank of Taiwan (臺灣銀行) brand color palette and fonts to the CONTENT
  of documents being generated — Word reports, PowerPoint decks, and Excel workbooks —
  so titles, headers, table headers, accents, and chart series use the BOT wine-red +
  gold palette. This styles the actual deliverable's content, it does NOT produce a
  theme file.
  Use when the user asks to "用臺銀配色做這份文件/簡報/報表", "套臺銀色做 Word/PPT/Excel",
  "做一份臺銀風格的簡報", "把這份報表改成臺銀配色", "BOT brand colors in this deck",
  "style this document with Bank of Taiwan colors", or generates any docx/pptx/xlsx
  that should follow the BOT brand.
  Do NOT use for: producing the reusable .thmx theme file (use bot-brand-theme instead),
  extracting specs from the brand manual PDF (read the PDF directly), or non-BOT/generic
  styling.
cowork:
  category: productivity
  icon: PaintBrush
---

# 臺灣銀行品牌配色套用（文件內容）

When you build a Word / PowerPoint / Excel deliverable, apply the Bank of Taiwan brand
palette and fonts to the **content itself** (titles, section headers, table header rows,
accent shapes, chart series). This is the companion to `bot-brand-theme`: that skill makes
a reusable `.thmx`; **this skill paints the brand colors directly into the document you are
generating right now.**

## When NOT to Use

- The user wants the reusable theme file (`.thmx`) → use **bot-brand-theme**.
- The user wants to read/extract specs from the brand manual PDF → read the PDF directly.
- The user wants generic, non-BOT styling → just build it; don't apply this palette.

## Brand Palette (use these exact values)

All hex values trace to the BOT brand identity manual. Do not invent colors.

**Primary (use as the dominant color):**

| Role | Color | HEX | RGB |
|------|-------|-----|-----|
| Primary | 紅 | `#9A0036` | 154, 0, 54 |
| Primary light | 淺紅 | `#D93657` | 217, 54, 87 |

**Accents (chart series / highlights, in this order):**

| # | Color | HEX |
|---|-------|-----|
| 1 | 紅 | `#9A0036` |
| 2 | 淺紅 | `#D93657` |
| 3 | 金棕 | `#9C7625` |
| 4 | 黃 (金) | `#F7C84D` |
| 5 | 深紫 | `#591A4A` |
| 6 | 淺灰 | `#8398B2` |

**Neutrals:** 深灰 `#4A4D53` (body text emphasis / table gridlines) · 淺灰底 `#F3F5F7` or 暖紅白底 `#F6E8E8` (zebra rows / fills) · 黑 `#000000` · 白 `#FFFFFF`.

**Fonts:** headings **Poppins** (Latin) / **微軟正黑體 Microsoft JhengHei** (CJK); body **Arial** (Latin) / **微軟正黑體** (CJK). These are the manual's designated Office fonts for reliable cross-machine display.

## Application Rules

- **Primary dominant:** 紅 `#9A0036` is the lead color — document/slide titles, section
  headers, Excel table header fill, the first chart series. Accents are secondary.
- **Header text on red fill:** use white `#FFFFFF` text on `#9A0036` (and on 淺紅 / 漸層紅).
- **Chart series:** assign accent colors in the order listed above.
- **Tables:** header row fill `#9A0036` + white text; optional zebra rows in `#F6E8E8`;
  gridlines in 深灰 `#4A4D53` or 淺灰.
- **Gradients:** linear only (紅→淺紅), never radial.
- **Don't rainbow everything:** keep the piece red-dominant with sparing accents.

## Workflow

1. Identify the target format (Word / PowerPoint / Excel) from the user's request.
2. Invoke the matching built-in skill with the **Skill** tool — **docx**, **pptx**, or
   **xlsx** — to do the actual file construction. This skill supplies the palette/fonts;
   those skills build the file.
3. While generating, apply the **Brand Palette** + **Application Rules** above: set title /
   header colors to `#9A0036`, white text on red fills, chart series in accent order, and
   the brand fonts. Use the **Edit** / **Bash** tools as needed to set colors in the
   generation script (python-docx / python-pptx / openpyxl).
4. Compute any embedded numbers with code (do not hand-calculate), then build the file.
5. Confirm the deliverable exists with the **Glob** tool (`Glob output/**/*`) before
   reporting — blocking delivery gate.
6. Report using the **Output Format** below.

## Output Format

Deliverable: the requested file in `output/` (e.g. `output/<name>.docx|pptx|xlsx`), styled
in BOT brand colors. Report to the user in plain language (no raw XML/code, no tool names):
what was produced, that it uses the BOT palette (primary `#9A0036`) and fonts, and the
filename. Do not paste color tables unless asked.

## Guardrails

- **Never fabricate colors or content.** Use only the hex values above; never invent facts,
  numbers, or figures for the document — leave clearly-marked placeholders (e.g.
  `[填入 Q3 數據]`) when data is missing.
- **Delegate file building:** this skill styles content; the docx/pptx/xlsx skills construct
  the file. Do not reimplement document generation here.
- **Do not produce a .thmx** — that is bot-brand-theme's job. If the user actually wants the
  reusable theme file, hand off to bot-brand-theme.
- **Numeric accuracy:** compute any totals/percentages with code before embedding them.
- **Save to `output/` only;** do not send or post the file anywhere.
