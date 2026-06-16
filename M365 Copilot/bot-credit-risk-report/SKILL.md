---
name: bot-credit-risk-report
description: |
  將臺灣銀行（Bank of Taiwan）授信戶的案件來源文件——「授信戶重大變故維護單／重大變故」、
  「授信往來情形表（含集團彙總）」、研究報告、新聞剪報或重大訊息——彙整成一份臺銀酒紅＋金色
  配色的「授信戶重大變故風險評估報告」Word（.docx）檔，供下載。報告自動帶出本行曝險、集團
  授信彙總、退票／變故事件時序、公司治理與財務流動性分析、分級風險評估與保全建議事項，所有
  金額與動用率均以程式計算、絕不杜撰。
  Use when the user uploads or references 授信案件文件（重大變故維護單 / 授信往來情形表 /
  研究報告 / 新聞 / 重大訊息）and asks to "做一份授信戶重大變故風險評估報告",
  "彙整文件寫風險評估報告", "把這些文件整理成 Word 風險評估報告", "臺銀配色的授信風險報告",
  "credit risk assessment report for this borrower", "授信戶出事幫我做評估報告",
  "幫這個授信戶做風險評估". Each quoted phrase above is a trigger phrase.
  Do NOT use for：一般非授信案件的 Word 製作（用 docx / work-doc）、純品牌主題檔 .thmx
  （用 bot-brand-theme）、新聞剪報彙整成純文字一頁式（用 bot-news-briefing /
  credit-risk-briefing）、SQL 彙總網頁化（用 bot-sql-summary-report）、教育訓練手冊
  （用 bot-training-manual）、或寄送 email／Teams 訊息。
cowork:
  category: analysis
  icon: DocumentTable
---

# 臺銀授信戶重大變故風險評估報告（Word）

把一組授信案件來源文件，彙整成一份**臺灣銀行酒紅＋金色配色**的「授信戶重大變故風險評估
報告」`.docx`，供風險管理部／分行使用並下載。本技能負責**內容彙整與報告結構**，實際檔案由
內建 `docx` 技能建置，配色規範取自 `bot-brand-styling`。

## Quick Start

```
使用者：（上傳 重大變故維護單＋授信往來情形表＋研究報告＋新聞）
        「幫這個授信戶做風險評估報告，臺銀配色，給我 Word」
→ Glob / Read 讀取四份文件 → 擷取事實寫入 working/content-brief.md
→ Bash(python) 計算動用率、集團合計曝險 → 套 bot-brand-styling 酒紅配色
→ docx 技能：寫 create-doc.js 建八章報告 → validate.py + soffice/pdftoppm QA
→ Glob output/**/*.docx 把關 → 交付 output/<授信戶>_授信戶重大變故風險評估報告.docx
```

## When NOT to Use

- 使用者要的是**可重複套用的佈景主題檔（.thmx）** → use **bot-brand-theme** instead。
- 要把新聞剪報整理成**純文字一頁式高層摘要**（非授信案件、不產檔） → use **bot-news-briefing**
  or **credit-risk-briefing** instead。
- 要把「SQL 查詢彙總」Excel **視覺化成網頁／儀表板** → use **bot-sql-summary-report** instead。
- 要把簡報／文件改寫成**教育訓練手冊** → use **bot-training-manual** instead。
- 只是要一份**一般 Word 文件**、與授信案件無關 → use 內建 **docx** or **work-doc** instead。
- 要**寄送**報告（email／Teams） → 本技能只存檔到 `output/`，不寄送。

## 來源文件對照（會收到哪些、各自提供什麼）

| 文件 | 典型格式 | 擷取重點 |
|------|---------|---------|
| 授信戶重大變故維護單／「重大變故」 | .doc / .docx | 授信戶名稱、統編、行業別、起案／承貸單位、變故日期、勾選之變故原因、是否影響本行債權、負責人／保證人、連帶借用人 |
| 授信往來情形表 | .doc / .docx | 各帳號授信項目／用途、訂借額度、現放餘額、動用期間、利率、擔保註記、本行授權有效額度、現放總餘額 |
| 集團授信往來彙總表 | 常併於上表 | 關係／集團企業統編、戶名、關係、額度、餘額、評等／分數、年度、合計曝險 |
| 研究報告 | .docx | 事件來龍去脈、財務徵兆、公司治理動盪、影響分析、類似案例 |
| 新聞／重大訊息 | .pdf / 文字 | 退票／變故事件時序與金額、股東會、董監異動、記者會說法 |

不是每個案件都四種齊全；**以實際提供者為準**，缺漏的章節據實標示「資料不足」，不臆測補白。

## Workflow

1. **找齊並讀取來源文件**：用 `Glob`（`input/**/*`）找出使用者上傳檔；附件清單已列路徑時直接用
   `Read` tool。PDF 用 `Read`；`.docx` 解壓 `word/document.xml` 取段落文字；`.doc` 先以
   `soffice --headless --convert-to docx` 轉檔再讀。逐一擷取上表重點。
2. **建立事實清單（content brief）**：將授信戶基本資料、本行各帳號曝險、集團彙總、變故／退票
   事件時序、治理動盪、財務流動性要點，整理成 `working/content-brief.md`（純文字、簡明）。
   **只記錄文件中確有的數字與事實**。
3. **以程式計算所有衍生數字**：用 `Bash`（python）計算動用率（餘額／額度）、集團合計曝險、
   折算金額（千元→億元）等。**不得心算**；計算結果寫回 brief。
4. **套用臺銀配色規範**：採用 `bot-brand-styling` 色票——主色酒紅 `#9A0036`、淺紅 `#D93657`、
   金棕 `#9C7625`、金黃 `#F7C84D`、深灰 `#4A4D53`、暖紅白斑馬列 `#F6E8E8`；標題／表頭紅底
   白字；字型標題與內文皆用「微軟正黑體 Microsoft JhengHei」(CJK)／Arial(Latin)。
5. **撰寫並產出 Word**：以內建 `docx` 技能流程，寫一支 `create-doc.js`（docx-js）建置報告，
   套用第 4 點配色，輸出至 `output/<授信戶>_授信戶重大變故風險評估報告.docx`。報告章節：
   1. 報告抬頭（臺灣銀行 風險管理部）＋授信戶／統編／單位／資料日期／報告日期／整體風險評等
      之 meta `table`
   2. **一、報告摘要**：3 格關鍵指標卡（本行曝險、集團合計曝險、負責人退票累計），加一段結論句
   3. **二、授信戶基本資料**（`table`）
   4. **三、本行授信往來情形**：本行授信明細 `table` ＋集團授信彙總 `table`（含合計列與動用率）
   5. **四、重大變故事件說明**：勾選之變故原因、是否影響債權，加退票／變故**事件時序 `table`**
   6. **五、公司治理與經營權風險**（`bullet` 條列）
   7. **六、財務與流動性分析**（`bullet` 條列）
   8. **七、對本行債權之風險評估**：信用／流動性／治理／擔保／聲譽五面向**分級 `table`**（高／中高／中）
   9. **八、結論與建議事項**：停止動撥、擔保品總體檢、強化保證追償、債權分類提存、持續監控重訊、
      集團連動檢視等保全措施（編號清單）
   頁首：酒紅細線＋「臺灣銀行　風險管理部／報告名稱」；頁尾：「機密文件　限行內使用」＋頁碼。
6. **驗證與 QA**（包在單一 Task 內）：`node create-doc.js` →
   `python scripts/office/validate.py` → 轉 PDF＋`pdftoppm` 出圖檢查表格是否爆版、欄寬加總、
   中文呈現、配色；發現問題改 `create-doc.js` 重跑，直到乾淨。
7. **交付前把關（BLOCKING）**：`Glob output/**/*.docx` 確認檔案存在後才回報。
8. **回報**：以白話說明產出內容、採臺銀配色（主色 `#9A0036`）與檔名；提醒數據基準日與後續滾動
   更新，不貼原始程式碼或工具名稱。

## Output Format

Output: a Bank-of-Taiwan-styled Word (.docx) report — 8 numbered sections, each built with
`table` layouts (meta table, exposure table, group table, event-timeline table, risk-grade
table) plus `bullet` lists; saved to `output/`. Tools used: `Glob`, `Read`, `Bash`(python),
the `docx` skill (create-doc.js + validate.py) and `soffice`/`pdftoppm` for QA.

交付物：`output/<授信戶名稱>_授信戶重大變故風險評估報告.docx`（臺銀酒紅＋金色配色）。
回覆使用者時用白話：產出了什麼、含哪些章節與關鍵數字、採臺銀品牌配色與字型、檔名為何，並提醒
數據以資料日期為準、建議依最新重訊滾動更新。不貼色票表、XML 或工具名稱，除非使用者要求。

## Guardrails

- **絕不杜撰事實（never fabricate）**：人名、統編、金額、日期、評等、引述一律以來源文件為準；
  if a fact is missing or a source is not found，以清楚標註的占位字（例如 `[待補：擔保品鑑價]`）
  呈現，不得自行編造。缺整類資料時據實寫「資料不足」並說明缺口。
- **數字一律程式計算（always compute with code）**：總額、動用率、百分比、折算金額等，先用
  `Bash`(python) 算好再嵌入；禁止心算。
- **配色只用 bot-brand-styling 色票**：never 自創顏色；以酒紅為主色、配色節制（紅底白字、斑馬列
  暖紅白、強調用金棕／金黃），不要整份花俏。
- **委派建檔**：本技能負責彙整與結構，實際 `.docx` 由內建 `docx` 技能建置；don't 重寫文件產生
  邏輯，也不產 `.thmx`（那是 bot-brand-theme 的工作）。
- **個資審慎（privacy / redact）**：報告含負責人／保證人身分證號等敏感資訊時，比照行內慣例
  redact／遮罩中間碼；save to `output/` only，never auto-send、不上傳任何外部服務。
- **沙箱限制與失敗處理**：never `pip install`／`npm install`（會逾時）；以容器既有工具完成。
  if a source file cannot be read or 轉檔 fails，據實告知並 ask 使用者重新提供，不以範例資料
  替代真實內容。
