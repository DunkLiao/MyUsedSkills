---
name: credit-risk-briefing
description: |
  Filters a daily news digest (e.g. 今日新聞彙整) for credit-risk-relevant content
  and produces a one-page, Word-ready plain-text briefing for a credit risk manager,
  with key figures arranged in plain-text tables.
  Use when the user uploads or references a news digest / 新聞彙整 / 剪報 file and asks
  to "整理信用風險新聞", "篩選信用風險相關內容", "做成一頁式簡報", "給高層的信用風險摘要",
  "extract credit-risk news", "credit risk news briefing", or "彙整授信/放款/逾放新聞".
  Do NOT use for general news summaries unrelated to credit risk, for market-risk or
  insurance-only digests, for building Word/.docx files (this outputs copy-ready plain
  text, not a file), or for sending email/Teams messages.
cowork:
  category: analysis
  icon: DocumentBulletList
---

# Credit Risk News Briefing

Turn a raw daily news digest into a one-page, Word-ready plain-text credit-risk briefing.

## When NOT to Use

- The digest has no banking/credit content (pure markets, ESG, lifestyle).
- The user wants an actual Word `.docx` file generated → use the `docx` skill instead.
- The user wants the full digest summarized (all topics) → this skill keeps ONLY credit-risk items.
- The user wants it sent somewhere → this skill only produces copy-ready text.

## What Counts as "Credit Risk"

Keep an item if it touches any of these. Discard everything else.

- Lending / credit extension (授信、放款、聯貸、企金、房貸、車貸、信貸)
- Loan quality & default (逾放比、逾期繳款、違約、不良債權、NPL、備抵呆帳、預期信用減損)
- Credit concentration & exposure (產業集中度、不動產放款集中度、單一客戶/產業曝險)
- Borrower / counterparty creditworthiness & credit policy (授信5P、信用審核、信用評等)
- Credit / mortgage regulation (選擇性信用管制、房市信用管制、寬限期、成數)
- Leverage & systemic credit risk (過度槓桿、四貸同堂、系統性風險)
- Leasing / financing credit risk (融資租賃、應收帳款、延滯)
- Bank capital adequacy tied to lending/loss (資本適足率、減資彌補虧損、銀行法第64條)
- Debt / bond credit & sovereign credit (公司債、發債、政府/主權債信、信用利差)

Exclude: pure equity-market moves, FX/gold price, insurance product/claims, AML/fraud
internal-control, HR, tax-collection, ESG, travel, unless they explicitly carry a credit angle.

## Workflow

1. **Locate the source.** Read the attached/uploaded digest file with `Read` (check `input/`
   via `Glob input/**/*` if no path is given). If it exceeds the read limit, read it in
   sequential page ranges until the whole file is covered — do not stop at page one.
2. **Filter.** Scan every article and keep only credit-risk-relevant items per the list above.
   Note the digest's own date for the title.
3. **Extract key figures.** Pull every concrete number tied to credit risk (loan balances,
   growth, 逾放率, 達成率, 戶數, 金額, 占比, 補貼碼數) for the tables.
4. **Organize** into the section structure in Output Format. Group by theme, not by source order.
   Merge duplicate articles covering the same event into one bullet set.
5. **Output** the briefing inside a single fenced code block (so it has a one-click copy button
   and pastes cleanly into Word). One page: aim for concise bullets and tight tables.

## Output Format

Emit ONLY the briefing, inside one fenced code block. No preface, no closing remark, no meta.

- Title line: `信用風險重點摘要報告（<digest date>）`
- Themed sections (include only those with content), e.g.:
  一、銀行授信與產業放款 / 二、房貸授信與相關政策 / 三、信用管制與系統性風險 /
  四、租賃業信用風險 / 五、其他信用相關
- Bullets use `‧` and stay one-to-two lines each.
- Put important figures in plain-text tables drawn with box characters
  (`┌─┬─┐ │ ├─┼─┤ └─┴─┘`), columns padded with spaces so they align in a monospace/Word view.
- Keep the whole thing to roughly one printed page.

## Example

Input: an uploaded `今日新聞彙整` digest covering 樂齡獎、台銀人壽增資、五大信賴產業放款、
新青安、選擇性信用管制、金價、台股等數十則新聞.
Output: a fenced code block titled `信用風險重點摘要報告（2026/06/11）` containing ONLY the
授信/放款、房貸、信用管制、租賃信用風險 items, with a 五大信賴產業放款 figures table and a
新青安授信品質 table — and nothing about gold prices, 台股, or AML cases.

## Guardrails

- **Source-only, no fabrication, fully grounded.** Use only the content of the supplied digest.
  Every figure and claim must trace to the source text. Never add outside facts, figures, names,
  or commentary, and never infer or estimate numbers not present in the text.
- **No hyperlinks / URLs / source links** in the output (strip the 來源 lines).
- **No preface, no meta, no questions.** Do not write "以下為整理內容…" or explain what you did.
- **No fabrication.** If a figure is missing for a table cell, leave it as `—`.
- **No file creation or sending.** Output copy-ready plain text only, in a code block.
- If no credit-risk content is found, say so in one plain line — do not pad with unrelated items.
