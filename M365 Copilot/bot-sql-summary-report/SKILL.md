---
name: bot-sql-summary-report
description: |
  將臺灣銀行風險管理部的「SQL 查詢彙總」Excel 檔（含會計月計表、備抵呆帳、放款分類、
  企業/房貸放款品質、執行記錄等工作表）一鍵轉成兩份臺銀酒紅配色、單一可離線的網頁，
  並打包成 ZIP：(1) 表格版報表（全資料可排序/搜尋/分頁）與 (2) 十種圖形儀表板。
  Use when the user uploads or references a「SQL 查詢彙總」/「SQL查詢」xlsx 並要求
  "做成 HTML"、"建立網頁報表"、"做成儀表板"、"十種圖形"、"套臺銀/酒紅配色"、
  "打包成 ZIP"、或要把這份彙總視覺化呈現給高層。
  Do NOT use for：一般非此彙總結構的 Excel、要產出 .docx/.pdf/.pptx 檔、
  寄送 email 或 Teams 訊息、或新聞剪報彙整（用 bot-news-briefing / credit-risk-briefing）。
cowork:
  category: analysis
  icon: DataBarVertical
---

# 臺灣銀行 SQL 查詢彙總 — 報表＋儀表板產生器

把風險管理部每期的「SQL 查詢彙總」Excel，產出兩份臺銀官方酒紅配色、單一檔案、
可離線開啟的網頁，再打包成 ZIP 供下載。流程固定、可每期重複使用。

## When NOT to Use

- 來源不是此彙總結構的一般 Excel（沒有備抵呆帳／放款品質等工作表）
- 要產出 Word / PDF / PowerPoint 檔（改用 docx / pdf / pptx）
- 要寄 email 或發 Teams（本技能只產生本機檔案）
- 新聞剪報 / 信用風險新聞彙整（用 bot-news-briefing 或 credit-risk-briefing）

## 輸出格式 Output Format（皆存到 output/）

1. `SQL_查詢彙總報表.html` — 表格版：6 個工作表全資料，數字千分位、年增率百分比、
   風險指標 3 位小數；可排序／搜尋／分頁；含備抵呆帳折線圖。
2. `SQL_查詢彙總儀表板.html` — 十種圖形 + 4 張 KPI 卡：
   折線、區域、直條、群組直條、堆疊長條、橫條(Top15)、圓餅、環圈、散佈、量規。
3. `臺灣銀行_SQL查詢彙總_報表與儀表板_<日期>.zip` — 兩份 HTML 打包。

## 工作流程

使用工具：**Glob**（找檔）、**Read**（必要時看內容）、**Bash**（執行 `build_bot_report.py`、
`validate.py`）、**Skill: html**（表格版報表的 `generate.py`）。

1. **找檔**：先看 `input/`（使用者上傳處）。用 **Glob** `input/**/*.xlsx` 找「SQL 查詢彙總」檔；
   若 `<attached_files>` 已給路徑，直接用。找不到才詢問。
2. **執行產生器**（一次完成讀檔、產兩份 HTML、打包 ZIP）：
   ```bash
   python scripts/build_bot_report.py --input "<xlsx路徑>" --outdir output --workdir working
   ```
   - 腳本以「關鍵字」比對工作表（備抵呆帳／放款進出口押匯／企業放款品質／房貸品質／
     會計月計表／執行記錄），期別自動偵測，缺某張表時自動略過對應圖表，不會中斷。
   - 表格版報表會呼叫內建 html 技能的 `generate.py` 再注入臺銀配色；
     路徑預設 `/opt/workspace-config/.claude/skills/html/scripts/generate.py`，
     可用環境變數 `HTML_GENERATE_PY` 覆寫。
3. **檢核**（兩份 HTML 都要過）：
   ```bash
   python /opt/workspace-config/.claude/skills/html/scripts/validate.py output/SQL_查詢彙總報表.html
   python /opt/workspace-config/.claude/skills/html/scripts/validate.py output/SQL_查詢彙總儀表板.html
   ```
   status 必須為 `success`；若有 errors 依訊息修正後重跑。
4. **確認交付**：`Glob output/**/*` 確認三個檔案都在，再用業務語言回覆使用者
   （勿提腳本名稱或路徑細節）。

## 配色（臺灣銀行官方）

見 [references/brand-palette.md](references/brand-palette.md)。重點：
- 主色 臺銀深酒紅 `#6B1629`（標題、表頭底）、副色 酒紅 `#8C2038`（連結、章標籤）
- 中灰 `#666666`（輔助／頁尾）、淺粉 `#F5E6EA`（標籤底）、極淺粉 `#FAF5F6`（交替列／頁底）
- 圖表以酒紅家族層次區分；散佈圖風險指標 ≥1 以深酒紅標示並畫警戒線；
  量規以「淺粉→酒紅→深酒紅」表示風險升高。

## Guardrails（守則）

- **絕不**杜撰數字：金額、比率**必須**全部來自 Excel；缺資料時**必須**略過該圖並據實說明，**不得**填入示意值。
- 兩份 HTML **必須**通過 `validate.py`（單一檔案、UTF-8 BOM、無外部連線）才算完成。
- **只能**輸出到 `output/`；中間檔**務必**放 `working/`。回覆使用者**必須**用業務語言，**不得**揭露腳本名稱或路徑。
- 數字換算單位**固定**：放款金額(千元)÷1e5→億元、備抵呆帳(元)÷1e8→億元、年增率→%。
- **絕不**寄送 email 或發 Teams；本技能**只**產生本機檔案。

### 失敗處理 Failure handling

- 若 **Glob** 在 `input/` 找不到 xlsx：先放寬為 `**/*.xlsx` 再找；仍找不到才以一個問題詢問使用者，**不得**自行假設檔名。
- 若 `build_bot_report.py` 因工作表缺漏而某組資料為空：腳本會自動略過對應圖表；**必須**在回覆中說明哪些圖因無資料而省略。
- 若 `validate.py` 回報 errors：**必須**依 `kind`／`message` 修正後**重跑一次**；連續失敗才回報使用者並說明卡點，**不得**宣稱完成。
- 若表格版報表的 `generate.py` 路徑不存在：以環境變數 `HTML_GENERATE_PY` 指定正確路徑後重試；仍失敗時，至少交付儀表板版並據實告知。
- 交付前**務必**以 `Glob output/**/*` 確認報表、儀表板、ZIP 三個檔案皆存在，缺檔**不得**回報成功。
