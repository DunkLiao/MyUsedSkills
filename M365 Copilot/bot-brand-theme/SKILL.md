---
name: bot-brand-theme
description: |
  Generates the Bank of Taiwan (臺灣銀行) brand Office theme file (.thmx) so the
  user can one-click apply the BOT wine-red + gold color scheme and fonts across
  Word, PowerPoint, and Excel. Produces a validated .thmx in output/.
  Use when the user asks to "做臺銀佈景主題", "臺灣銀行色票 thmx", "產生品牌主題檔",
  "Bank of Taiwan Office theme", "套臺銀配色到 Word/PPT/Excel", "重做這個 thmx",
  "generate the BOT brand theme", or "give me the brand color theme file".
  Do NOT use for: building actual content documents/slides/workbooks (use docx,
  pptx, xlsx), extracting specs from the brand manual PDF (read the PDF directly),
  or non-BOT/generic Office themes.
cowork:
  category: productivity
  icon: Color
---

# 臺灣銀行品牌 Office 佈景主題（.thmx）產生器

Produces a ready-to-apply Office theme carrying the Bank of Taiwan brand colors
and fonts. The same `.thmx` applies to Word, PowerPoint, and Excel.

## When NOT to Use

- The user wants an actual document, deck, or workbook with content → use `docx` / `pptx` / `xlsx`.
- The user wants to read or extract specs from the brand manual PDF → read the PDF directly.
- The user wants a generic, non-BOT theme → build it directly, not via this skill.

## Color Scheme (theme slots)

| Theme slot | Brand color | HEX |
|------------|-------------|-----|
| Accent 1 | 紅 (primary) | `#9A0036` |
| Accent 2 | 淺紅 | `#D93657` |
| Accent 3 | 金棕 | `#9C7625` |
| Accent 4 | 黃 (gold) | `#F7C84D` |
| Accent 5 | 深紫 | `#591A4A` |
| Accent 6 | 淺灰 | `#8398B2` |
| Dark 2 | 深紫 | `#591A4A` |
| Light 2 | 暖紅白底 | `#F6E8E8` |
| Hyperlink / Followed | 紅 / 紫 | `#9A0036` / `#6C1F76` |
| Text / Background | 黑 / 白 | `#000000` / `#FFFFFF` |

**Fonts:** headings **Poppins**, body **Arial**, CJK **Microsoft JhengHei (微軟正黑體)**.
These are the brand manual's designated Office fallback fonts, chosen for reliable
cross-machine display. All hex values come from the BOT brand identity manual.

## Workflow

1. Run the generator (writes a validated `.thmx` and self-checks every XML part):
   ```bash
   python scripts/make_thmx.py output
   ```
   It prints `OK -> output/臺灣銀行品牌色票.thmx` on success. To regenerate after a
   color/font edit, change the `CLR_SCHEME` / `FONT_SCHEME` constants at the top of
   `scripts/make_thmx.py` and re-run.
2. Confirm the file exists with `Glob output/**/*` before telling the user it is ready
   (delivery gate).
3. Tell the user the file is ready and how to apply it (see below).

## How to apply (tell the user)

- **PowerPoint:** 設計 → 佈景主題 → 下拉箭頭 → 瀏覽佈景主題 → 選此檔
- **Word:** 設計 → 佈景主題 → 瀏覽佈景主題
- **Excel:** 版面配置 → 佈景主題 → 瀏覽佈景主題

After applying, the standard color palette and default chart series colors become the
BOT brand colors, with the primary red as Accent 1.

## Output Format

A single file `output/臺灣銀行品牌色票.thmx`. Report: what was generated, the primary
color (`#9A0036`), the fonts, and the three apply paths. Do not paste raw XML.

## Guardrails

- **Never fabricate colors.** Only use the hex values defined in this skill (which trace
  to the brand manual). If the user wants different colors, edit the constants in
  `scripts/make_thmx.py` — do not invent values.
- **Technical correctness:** the `.thmx` must (a) start from Office's valid theme1.xml and
  swap only the color/font schemes, and (b) declare the start part with the `officeDocument`
  relationship type. A hand-written theme body or the `theme` relationship type causes
  PowerPoint's "無法讀取" (cannot read) error.
- **Always self-validate:** the script parses every XML part and asserts the brand red is
  present before reporting success. If it fails, fix before delivering.
- **Do not send/post the file anywhere** — just save it to `output/` for the user to download.
