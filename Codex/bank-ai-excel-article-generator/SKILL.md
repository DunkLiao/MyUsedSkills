---
name: bank-ai-excel-article-generator
description: Use this skill when the user wants to inspect an article folder, brainstorm ten new banking-industry AI and Excel collaboration FAQ topics that do not duplicate existing files, then write each topic as a 500+ Chinese-character Markdown article saved as separate .md files without numeric prefixes in filenames.
metadata:
  short-description: Generate banking AI+Excel FAQ Markdown articles
---

# Banking AI + Excel Article Generator

Use this skill to generate new Chinese FAQ-style Markdown articles about AI and Excel collaboration in banking, based on the documents already present in a folder.

## Workflow

1. Inspect the folder
   - List all files in the current folder.
   - Read filenames first to understand existing topics.
   - Sample article contents when needed, especially headings, introductions, and repeated themes.
   - Treat existing `.md` and `.txt` files as source articles.

2. Identify covered themes
   - Summarize the current topic map before brainstorming.
   - Avoid producing questions that are only rephrased versions of existing articles.
   - Common duplicate risk areas include general Excel formula prompting, VBA generation, VBA debugging, Power Query basics, dashboard usefulness, data privacy, field-structure description, and beginner AI collaboration.

3. Brainstorm ten new questions
   - The questions must focus on banking-industry work scenarios.
   - Prioritize practical banking contexts such as branch reports, credit review, loan tracking, deposit analysis, risk control, compliance checks, suspicious transaction review, customer segmentation, KPI reporting, regulatory reporting, reconciliation, and internal management reports.
   - Each question should be specific enough to support a useful article.
   - Do not number the questions in filenames.

4. Write one Markdown file per question
   - Use the question itself, or a concise cleaned version of it, as the filename.
   - The filename must not begin with a number, Chinese numeral, list marker, or question index.
   - Use the `.md` extension.
   - Keep content in Traditional Chinese unless the user asks otherwise.
   - Each article must answer the question directly and contain at least 500 Chinese characters.
   - Write in an educational, practical tone for non-technical banking staff.
   - Include realistic banking examples, clear AI collaboration methods, useful prompt examples, and cautions where relevant.

5. Content quality rules
   - Do not suggest uploading sensitive customer data, account numbers, IDs, transaction details, credit records, or internal confidential reports to unapproved public AI tools.
   - When examples require data, use anonymized or fictional fields.
   - Distinguish between what AI can help draft, explain, classify, or check, and what must be verified by bank staff under internal policy.
   - Avoid presenting AI output as authoritative for compliance, credit approval, audit conclusions, or regulatory interpretation.
   - Emphasize human review, source verification, and internal approval for high-risk banking workflows.

6. Verification
   - After writing files, list the created filenames.
   - Confirm every created file has `.md` extension.
   - Confirm no created filename starts with a numeric prefix.
   - Confirm each article is at least 500 Chinese characters.
   - If the user asks to regenerate the site, run the project generator after files are created.

## Suggested Question Angles

Use these only as inspiration; still inspect the folder and avoid overlap:

- AI helping branch managers compare monthly performance changes.
- AI designing Excel checks for abnormal loan overdue changes.
- AI helping reconcile core banking exports with manual tracking sheets.
- AI creating anonymized prompt templates for customer segmentation.
- AI explaining why KPI results differ between finance and business units.
- AI helping design control checks before submitting regulatory reports.
- AI turning credit review notes into structured Excel tracking fields.
- AI assisting with suspicious transaction triage spreadsheets.
- AI helping validate fee, interest, or rate-change impact reports.
- AI documenting recurring banking Excel report workflows for handover.

## Example User Request

```text
先幫我看資料夾下所有的文件，幫我發想十個在銀行業，AI與EXCEL協作常見問題，不在文件提供的類似問題裡面。
再幫我將十個問題，各自回答後轉成MARKDOWN文件存檔，每個回答要500字以上，存檔檔名不得有問題編號。
```

## Expected Output Behavior

When this skill is used, complete the work end to end:

- Inspect existing documents.
- Create ten non-duplicate banking AI+Excel questions.
- Write ten complete Markdown files.
- Save them into the working article folder.
- Report the created filenames and verification results.
