---
name: bot-sql-proc-doc
description: |
  將 Oracle PL/SQL 預存程序（stored procedure，如 ETL／風險計算批次程序）的原始碼，
  解析成兩份可下載交付物：(1) draw.io 流程圖（.drawio 檔），呈現各階段
  DELETE／INSERT／UPDATE 處理流程、來源表與目標表資料流；(2) 資料字典 Excel（.xlsx），
  整理所有來源表／目標表的欄位、用途、加工邏輯、對照碼與篩選條件。會自動還原 Big5／CP950
  亂碼中文註解，所有檔案套臺銀酒紅＋金配色，並以 LibreOffice 正規化確保 Excel 不跳修復視窗。
  Use when the user uploads or references a .sql / .txt / .pks / .pkb / .prc Oracle 預存程序（procedure／package／PL-SQL）
  and asks to "畫成流程圖", "畫 draw.io 流程圖", "做這支程序的流程圖", "建立資料字典",
  "整理來源表目標表欄位", "幫這支 SQL／預存程序做文件", "把這個 stored procedure 文件化",
  "turn this stored procedure into a flowchart and data dictionary",
  "document this Oracle procedure". 每一句引號片語皆為觸發語。
  Do NOT use for：執行或除錯 SQL（本 skill 只做靜態文件化，不連資料庫、不跑查詢）、
  一般非 SQL 程式碼的流程圖、把既有 Excel 彙總視覺化成網頁（用 bot-sql-summary-report）、
  純品牌主題檔 .thmx（用 bot-brand-theme）、或寄送 email／Teams 訊息。
cowork:
  category: analysis
  icon: FlowchartCircle
---

# bot-sql-proc-doc — Oracle 預存程序文件化（流程圖 + 資料字典）

把一支 Oracle PL/SQL 預存程序的原始碼，產出**流程圖（draw.io）**與**資料字典（Excel）**兩份交付物，
供風險管理／資料治理留存與審閱。本 skill **只做靜態解析與文件化**，不連線資料庫、不執行任何 SQL。

## When NOT to Use

- 要實際執行、測試或除錯 SQL／預存程序 → 本 skill 不連資料庫，僅做靜態文件化。
- 程式不是 Oracle PL/SQL 預存程序（例如一般 Python／Java 流程圖）→ 用通用作法。
- 已經是彙總好的 Excel，要做成網頁儀表板 → 用 `bot-sql-summary-report`。
- 只要品牌主題檔（.thmx）→ 用 `bot-brand-theme`；只要把文件套色不解析 SQL → 用 `bot-brand-styling`。

## 輸入

- 一個或多個 `.sql` / `.txt` / `.pks` / `.pkb` / `.prc` 檔（`input/` 或對話附件），內容為 `CREATE OR REPLACE PROCEDURE/PACKAGE … BEGIN … END;`。
- 先用 `Glob input/**/*` 找檔；附件路徑直接 `Read`。

## 使用工具（Tools）

每個步驟對應的 tool 如下：`Glob`（找 `input/` 內的程序檔）、`Read`（讀原始碼／附件）、`Bash`（執行 Python 解析、`openpyxl` 產 Excel、`soffice` 正規化）、`Write`（寫中繼檔）。本 skill 不需要、也不應呼叫任何 email／Teams／資料庫工具。

## 處理流程（Workflow）

### 1. 讀檔並還原中文編碼
原始檔的中文註解常是 **Big5／CP950**，用 `Read` 直接看會是亂碼。務必用程式重新解碼：

```python
raw = open(path, 'rb').read()
text = raw.decode('big5', 'replace')   # 多數臺銀 DB 匯出為 Big5；亂碼時改試 'cp950' / 'gb18030'
```

解碼後存到 `working/proc_decoded.txt` 再判讀。**註解中的中文業務語意（欄位意義、對照碼、篩選原因）是資料字典的關鍵來源，不可略過。**

### 2. 靜態解析程序結構
逐段（每個 `begin … exception … end;` 區塊）拆解，記錄：

- **階段別**：DELETE（清空）／INSERT（寫入）／UPDATE（逐欄更新）／MERGE。
- **目標表**：被 INSERT／UPDATE／DELETE 的資料表（通常 1 張，貫穿全程）。
- **來源表**：FROM／JOIN／子查詢／純量子查詢（`set col = (select … from X)`）引用的每一張表，連同 schema。
- **參數**：輸入參數（如 `p_vr_seq`）如何貫穿各來源表的 `WHERE`（常見 `SS_SEQ = p_vr_seq`）。
- **衍生／計算欄位**：`CASE WHEN`、運算式（如 `EAD = Σ(DEAL_AMT+AR_INT)×FX`）、`||` 字串組合。
- **對照碼**：`CASE WHEN col='中文' THEN '代碼'` 之類的值對應（整理成對照表）。
- **篩選條件**：`WHERE`／`NOT IN`／`substr(...) in (...)` 等納入／排除規則（連同其業務理由＝原始碼註解）。
- **稽核**：對 `USP_ST_AUDIT_LOG` 或同類 logging 程序的呼叫、`EXCEPTION WHEN OTHERS`、`COMMIT` 點。

### 3. 產出 draw.io 流程圖
用 Python 直接組 `mxGraphModel` XML（見 `references/recipes.md` 的 drawio 範本），輸出
`output/<程序名>_流程圖.drawio`。版面要點：

- 中央為**主流程**（上而下）：開始 →（各階段標頭 + 各步驟方塊）→ 結束；INSERT 的轉換管線、決策用菱形。
- 左側放**來源資料表**（cylinder/datastore），以**虛線箭頭**指向它所餵入的步驟。
- 右側放**跨階段註記**（例外處理、稽核 log、COMMIT）。
- 套臺銀配色：主節點酒紅 `#5B0E2D` 白字、流程方塊淺紅 `#FBE9EF`、來源/決策金色系 `#FFF4D6`／`#B8860B`。
- 完成後用 `xml.dom.minidom.parse` 驗證 XML 合法。

### 4. 產出資料字典 Excel
用 `openpyxl` 建立活頁簿（見 `references/recipes.md` 的 xlsx 範本），固定五個分頁：

1. **說明**：程序名、輸入參數、目標表、處理對象、各階段摘要、稽核機制。
2. **資料表總覽**：每張表的全名／Schema／類型（來源／目標／參數／稽核）／中文說明／在程序中的角色。
3. **來源表欄位**：每張來源表的每個被引用欄位 → 中文說明、用途／加工備註。
4. **目標表欄位**：目標表每個欄位 → 中文說明、資料來源、加工／計算邏輯、寫入階段。
5. **對照碼與篩選**：所有值對照表（如 FLAG→代碼）、計算分類規則、納入／排除篩選條件。

字型 `Microsoft JhengHei`，表頭酒紅底白字，斑馬列灰底。**目標表的任何加總／百分比若要直接寫數字，須以程式或公式計算，不可手算杜撰**（本 skill 多為文字字典，通常無計算）。

### 5. ★ 確保 Excel 不跳「修復」視窗（必做）
openpyxl 直接產生的檔，Excel 嚴格解析時常因**色碼透明位元異常**或非標準字串結構而跳出「我們發現…部分內容有問題」修復視窗。務必兩步：

1. **色碼用 8 碼 ARGB（FF 開頭）**：例如 `FF5B0E2D`、`FFFFFFFF`，**不要**用 6 碼（openpyxl 會補成透明的 `00xxxxxx`）。
2. **以 LibreOffice 正規化**：產生後務必轉檔一次，輸出標準（含 sharedStrings）的 Excel 檔：
   ```bash
   soffice --headless --convert-to xlsx --outdir output working/<程序名>_資料字典.xlsx
   ```
   先把 openpyxl 檔寫到 `working/`，再 `--outdir output` 轉出，避免覆寫鎖定。

### 6. 交付前檢查（Delivery Gate）
- `Glob output/**/*` 確認兩個檔都在 `output/`。
- Excel：用 `zipfile` 確認含 `xl/sharedStrings.xml`、所有 XML 以 `minidom` 可解析、`styles.xml` 無 `rgb="00xxxxxx"` 的自訂色；用 `openpyxl.load_workbook` 確認 5 分頁與列數無誤。
- draw.io：`minidom.parse` 通過。

## 輸出格式（Output format）

固定產出兩個檔（路徑與命名如下）；交付後另以 markdown 條列（bullet）回報摘要，資料字典固定含五個 sections（分頁）：

| 交付物 | 路徑 |
|---|---|
| 流程圖 | `output/<程序名>_流程圖.drawio` |
| 資料字典 | `output/<程序名>_資料字典.xlsx`（五分頁：說明／資料表總覽／來源表欄位／目標表欄位／對照碼與篩選） |

完成後用簡短文字回報：程序用途一句話、各階段摘要、兩個檔名與如何開啟（draw.io 用 diagrams.net 或 VS Code 外掛）。檔案同步到 OneDrive `Documents/Cowork 1`。

## 失敗處理（Failure handling）

- **解碼後仍是亂碼** → 依序改試 `cp950`、`gb18030`、`utf-8`；若全部失敗，明白告知無法判讀中文註解，請使用者確認原始編碼，不要拿亂碼當欄位名硬產。
- **Excel 仍跳「修復」視窗** → 確認步驟 5 的 LibreOffice 正規化有實際執行（`xl/sharedStrings.xml` 必須存在）；若 `output/` 覆寫出現 I/O error，先 `rm -f` 目標檔，再以 `soffice --outdir output` 由 working 轉出。
- **`output/` 寫入鎖定（OneDrive 同步）** → 重試一次；仍失敗則改存帶版本後綴的新檔名（如 `_v2`）並告知使用者，切勿回報「已完成」卻無檔。
- **解析不到來源表／目標表** → 回報實際找到的內容與缺口，請使用者確認檔案是否完整，不要編造資料表。
- **一次多支程序** → 每支各產一組流程圖＋字典；若要彙整成單一活頁簿多分頁，先向使用者確認再做。
- 交付前一律跑 `Glob output/**/*` 與步驟 6 的驗證；驗證未過不得宣稱完成。

## Guardrails

- **Never connect to a database or execute SQL** — 本 skill 只做靜態文件化，絕不連線、不跑查詢、不臆測資料內容或筆數。
- **Never fabricate（絕不杜撰）** — 資料表／欄位的中文意義一律以原始碼與其註解為憑（grounding）；無註解可考者依欄位名與用法保守描述並標註為「推斷」，嚴禁編造業務定義、筆數或數值。
- **Always 還原編碼** — 一律以 `big5`／`cp950` 重新解碼還原中文，不要拿亂碼當欄位名。
- **Always 驗證再交付** — Excel 必經 LibreOffice 正規化並通過 XML／sharedStrings 檢查；drawio 必經 `minidom` 驗證。
- **Always 存 `output/`** — 交付物一律存 `output/`，中繼檔放 `working/`。
- **Do NOT 寄送或改動來源** — 不在本 skill 內寄送 email／Teams，也不修改或刪除任何使用者來源檔。
