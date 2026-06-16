---
name: bot-training-manual
description: |
  將簡報（.pptx）或文件（.docx/.pdf/文字）內容改寫成「臺灣銀行（Bank of Taiwan）配色的
  Word 教育訓練手冊」，自動重組成章節化手冊，內含以 Word 原生物件繪製的流程圖（方塊＋▼箭頭
  ＋決策分支）、「如何落地使用（導入與實踐）」專章、用語小辭典與可列印檢核表，並**必定**一併輸出一張
  Mermaid 全書總覽流程圖。主要輸出為 output/ 下的 .docx 檔，並附帶一份 Mermaid 總覽（必要交付）。
  Use when the user asks to "把這份簡報做成教育訓練手冊", "改寫成訓練手冊", "做一本臺銀配色的手冊",
  "加上流程圖跟如何落地使用", "turn this deck into a training manual", "make a BOT-branded training
  manual", "rewrite this pptx into a 教育訓練手冊", "手冊的總覽流程圖 mermaid", or uploads a
  pptx/docx and asks to convert it into a training manual.
  Do NOT use for: 一般 PPT/Word 製作而非「教育訓練手冊」(用 pptx/docx/work-doc)、
  純品牌主題檔 .thmx (用 bot-brand-theme)、把既有報表視覺化成網頁 (用 bot-sql-summary-report)、
  新聞剪報彙整 (用 bot-news-briefing / credit-risk-briefing)、或寄送 email / Teams 訊息。
cowork:
  category: writing
  icon: BookGlobe
---

# 臺灣銀行教育訓練手冊產生器

把一份來源材料（簡報、文件或文字）改寫成**結構完整、臺銀配色、含流程圖與落地指引**的
Word 教育訓練手冊。本技能負責「規劃手冊結構＋撰寫 docx 生成腳本＋套臺銀配色」；實際建檔、
驗證與 QA 交由內建 **docx** 技能執行。

## Examples

```
User: 「把這份簡報做成臺銀配色的教育訓練手冊，要有流程圖跟如何落地使用」(附 deck.pptx)
→ Glob input/** → 用 python-pptx 萃取 → 規劃章節(補落地專章) → 複製 manual_template.js 為
  create-doc.js 改寫 children → Skill(docx) 在單一 Task 內 node create-doc.js + validate.py + QA
  → Glob output/**/*.docx → 產出必要的 Mermaid 全書總覽圖(程式碼區塊 + output/<書名>-總覽.md) → 回報

User: 「幫我把整本手冊濃縮成一張 mermaid 總覽流程圖」
→ 依 references/mermaid_overview.md 產出單一 flowchart TD（程式碼區塊回覆）
```

## When NOT to Use

- 使用者只要一般簡報或文件、不是「教育訓練手冊」→ 用 **pptx** / **docx** / **work-doc**。
- 使用者要可重複套用的佈景主題檔（`.thmx`）→ 用 **bot-brand-theme**。
- 使用者要把既有 Excel 彙總做成網頁儀表板 → 用 **bot-sql-summary-report**。
- 使用者要新聞/信用風險剪報彙整 → 用 **bot-news-briefing** / **credit-risk-briefing**。
- 使用者只要 Mermaid 圖、完全不要 Word 檔 → 直接輸出 Mermaid 文字即可，無須建檔。
  （注意：只要有產出手冊，Mermaid 全書總覽流程圖就是**必要**附帶交付，不可省略。）

## 臺灣銀行配色（固定值，勿自行更動）

| 角色 | 名稱 | HEX |
|------|------|-----|
| 主色（主標題、表頭底、流程圖起終點實心塊） | 臺銀深酒紅 | `#6B1629` |
| 副色（英文副標、次標、決策框外框） | 臺銀酒紅 | `#8C2038` |
| 內文 | 黑 | `#000000` |
| 輔助文字（頁尾、圖說、頁首） | 中灰 | `#666666` |
| 欄標籤底、流程方塊底 | 淺粉紅 | `#F5E6EA` |
| 表格交替列底、決策框底 | 極淺粉 | `#FAF5F6` |
| 表頭文字、實心塊文字 | 白 | `#FFFFFF` |

字型：標題與內文皆用 **微軟正黑體 Microsoft JhengHei**（CJK 可靠顯示）。

## 手冊標準結構（依來源內容調整，但保留此骨架）

1. **封面** — 臺銀字標＋中英書名＋版次/日期/編製單位。
2. **前言與使用說明** — 編製目的、適用對象、如何使用本手冊、重要提醒框。
3. **目錄**（TableOfContents，依 Heading1/2）。
4. **主體章節**（依來源材料重組，通常 4–6 章）：觀念 → 應用情境 → 實作範例 → 風險須知。
5. **「如何落地使用（導入與實踐）」專章（必備）** — 即使來源沒有，也要自行補上：
   標準作業流程（SOP 流程圖）、Prompt/指令撰寫原則、任務適配評估、人工驗證檢核清單、
   部門推動步驟（試點→擴散）、決策流程圖。
6. **總結**（對照表）＋ **附錄**（用語小辭典、可列印檢核表）。

> 交付清單（每次都要）：① 上述章節組成的 .docx 手冊　② 一張 Mermaid 全書總覽流程圖（必要附帶）。

## 流程圖做法（重要：用 Word 原生物件，不要點陣圖）

容器環境**無中文字型**，故流程圖**絕不可用 matplotlib/PIL 產生圖片**（中文會變成方框且烙印在圖上）。
一律以 docx 原生物件繪製，文字才是真實 Unicode、在使用者 Word 上正常顯示：

- **流程方塊** = 置中的單格表格（`F5E6EA` 底 + `#6B1629` 外框 + 深酒紅粗體字）。
- **起點／終點** = 主色 `#6B1629` 實心塊 + 白字。
- **箭頭** = 置中段落內的「▼」（深酒紅、加粗）；可在箭頭上方加灰色小字註記流向。
- **決策／分支** = 兩欄表格，左格「✔ 是」(淺粉底)、右格「✘ 否」(極淺粉底)，外框用副色 `#8C2038`。

`references/manual_template.js` 已內含 `flowBox / flowBoxSolid / arrow / branch / table / calloutBox`
等 helper 與配色常數，**直接複製為 create-doc.js 後改寫 children 內容**即可，不要從零重寫。

## Mermaid 全書總覽流程圖（必要・每次產出）

**只要產出手冊，就一定要附上這張總覽圖，不可省略。** 輸出單一 `flowchart TD`：
縱向主軸＝學習路徑（觀念→情境→實作→風險→**落地（核心）**→總結→附錄），每章一個 `subgraph`
含 2–5 個重點節點，並以 `classDef` 套臺銀配色（`fill:#6B1629,color:#FFFFFF` 為起終點、
`fill:#F5E6EA,stroke:#6B1629` 為章節節點、核心章 `stroke:#8C2038,stroke-width:3px`）。
範本見 `references/mermaid_overview.md`。**交付方式（兩者皆做）**：(1) 在回覆中以程式碼區塊呈現，
(2) 同時存成 `output/<書名>-總覽.md`，使章節異動時總覽圖同步更新。

## Workflow

1. **取得來源**：在 `input/`（及 `grounding/`）找使用者上傳的 pptx/docx/pdf；以 python-pptx /
   pandoc / markitdown 萃取文字與各頁標題，整理成內容大綱（可暫存 `working/content-brief.md`，<5KB）。
2. **規劃結構**：依「手冊標準結構」把來源重組成章節；**務必補上「如何落地使用」專章**與附錄。
   找出 2–4 個適合畫成流程圖的環節（實作步驟、決策、安全把關、落地 SOP）。
3. **撰寫腳本**：複製 `references/manual_template.js` 為工作區 `create-doc.js`，保留配色常數與
   helper，改寫 `children` 內容；數字一律用程式計算，缺資料留 `[待補：…]` 佔位，**勿杜撰**。
4. **建檔＋驗證＋QA**：透過 **Skill 工具呼叫 docx 技能**，在單一 Task 內 `node create-doc.js`
   →`validate.py`→ 轉 PDF/JPG 檢查版面。注意：QA 預覽因無中文字型會顯示方框，**僅用來檢查版面
   溢出/對齊，勿據以判斷文字內容**；交付的 .docx 文字本身正確。
5. **落地交付閘**：`Glob output/**/*.docx` 確認檔案存在後才回報。
6. **產出必要的 Mermaid 全書總覽圖**：依 `references/mermaid_overview.md` 產生單一 `flowchart TD`，
   在回覆中以程式碼區塊呈現，並同時寫入 `output/<書名>-總覽.md`。此為**每次必做**，不因使用者未提及而省略。
7. **回報**：用 docx 技能完成後，以平實中文說明：手冊名稱、章節、流程圖數量、已套臺銀主色
   `#6B1629`，並附上 Mermaid 全書總覽圖（程式碼區塊）。

## Output Format

- 主要交付：`output/<書名>.docx`（臺銀配色教育訓練手冊，含原生流程圖、落地專章、附錄）。
- **必要交付（每次）**：一張 Mermaid 全書總覽 `flowchart TD` — 同時以程式碼區塊回覆並存成
  `output/<書名>-總覽.md`。此項不可省略。
- 回報以使用者語言、不顯示 XML / 程式碼 / 工具名稱；不貼配色表除非被問。

## Failure Handling（失敗處理）

- **找不到來源檔**：若 Glob 在 `input/`、`grounding/` 都找不到對應檔案，先請使用者確認檔名，
  never 臆測或杜撰來源內容；do not 逕自開始建檔。
- **萃取失敗**：若 pptx/pdf 解析失敗，改用 pandoc / markitdown 重試一次；仍失敗則如實告知該檔
  無法讀取、請其重新提供，never 以範例資料替代真實內容。
- **建檔/驗證失敗**：若 `node create-doc.js` 或 `validate.py` 失敗，讀 docx 技能 SKILL.md 修正後
  retry；always 在回報前以 `Glob output/**/*.docx` 確認檔案存在（落地交付閘）。
- **版面溢出**：QA 發現流程方塊或兩欄分支超出 9360 DXA 內容寬時，縮小該方塊寬度後重建。
- **漏做總覽圖**：回報前 always 自我檢查是否已附上必要的 Mermaid 全書總覽圖；缺漏則補上後再回報。

## Guardrails

- **Never fabricate facts**（絕不杜撰人名、數字、引文、日期）；缺漏一律以 `[待補：…]` 清楚標示，
  do not 以想像內容填補。
- **配色固定**：always 只用上表 HEX，never 自行發明顏色；主色 `#6B1629` 為主導色，副色與淺底點綴。
- **流程圖一律原生物件**，never 使用會把中文烙印成方框的點陣圖（matplotlib/PIL）。
- **委派建檔**：本技能負責結構與配色，建/驗/QA always 交給 docx 技能，do not 在此重造建檔流程。
- **Mermaid 全書總覽圖為必要交付**：always 產出（程式碼區塊＋`output/<書名>-總覽.md`），never 省略。
- **只存 output/**，never 寄送或張貼到任何外部位置。
- 引用之 AI 回應範例屬示意，always 於手冊內加註「不代表各 AI 平台回應之一致性」。
