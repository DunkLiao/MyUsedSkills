# recipes — 產生 draw.io 與資料字典 Excel 的程式範本

臺銀配色：酒紅 `5B0E2D`、金 `C8A24B`／`B8860B`、淺紅 `FBE9EF`、淺金 `FFF4D6`／`FFF6E0`、灰 `F2F2F2`。
中文字型 `Microsoft JhengHei`。**Excel 色碼一律 8 碼 ARGB（`FF` 開頭）。**

---

## A. draw.io 流程圖（mxGraphModel XML）

直接用字串組 XML，`escape()` 處理使用者文字，最後以 `minidom` 驗證。

```python
from xml.sax.saxutils import escape
import xml.dom.minidom as minidom

cells = []
def cell(cid, value, x, y, w, h, style):
    cells.append(f'<mxCell id="{cid}" value="{escape(value)}" style="{style}" '
                 f'vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" '
                 f'width="{w}" height="{h}" as="geometry"/></mxCell>')
def edge(eid, src, tgt, value="", style="edgeStyle=orthogonalEdgeStyle;html=1;endArrow=block;"):
    cells.append(f'<mxCell id="{eid}" value="{escape(value)}" style="{style}" '
                 f'edge="1" parent="1" source="{src}" target="{tgt}">'
                 f'<mxGeometry relative="1" as="geometry"/></mxCell>')

# 樣式
START = "rounded=1;whiteSpace=wrap;html=1;fillColor=#5B0E2D;fontColor=#FFFFFF;strokeColor=#5B0E2D;fontStyle=1;"
PROC  = "rounded=0;whiteSpace=wrap;html=1;fillColor=#FBE9EF;strokeColor=#5B0E2D;align=left;spacingLeft=8;"
STAGE = "rounded=0;whiteSpace=wrap;html=1;fillColor=#5B0E2D;strokeColor=#5B0E2D;fontColor=#FFFFFF;fontStyle=1;"
DEC   = "rhombus;whiteSpace=wrap;html=1;fillColor=#FFF4D6;strokeColor=#B8860B;"
DB    = "shape=cylinder3;whiteSpace=wrap;html=1;backgroundOutline=1;fillColor=#FFF4D6;strokeColor=#B8860B;align=center;"
NOTE  = "shape=note;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#999999;align=left;spacingLeft=6;"

# 版面：中央主流程往下排，左側來源表(DB)虛線指入對應步驟，右側 NOTE 放稽核/例外
# 主流程依序：開始 → 各階段標頭(STAGE) → 各步驟(PROC) → 結束
# 來源表 → 用 dashed 邊：edge(..., style="...;dashed=1;strokeColor=#B8860B;")

xml = ('<mxfile host="app.diagrams.net"><diagram name="proc">'
       '<mxGraphModel dx="1200" dy="900" grid="1" gridSize="10" page="1" '
       'pageWidth="1169" pageHeight="1654"><root>'
       '<mxCell id="0"/><mxCell id="1" parent="0"/>'
       + "".join(cells) + '</root></mxGraphModel></diagram></mxfile>')
open("output/PROC_流程圖.drawio","w",encoding="utf-8").write(xml)
minidom.parseString(xml)   # 驗證
```

要點：主流程節點依序用 `edge` 串接；來源 `DB` 節點各放左側、虛線指向它餵入的步驟；INSERT 的轉換管線可拆成數個 `PROC`，篩選用 `DEC` 菱形。

---

## B. 資料字典 Excel（openpyxl）

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

WINE="FF5B0E2D"; GOLD="FFC8A24B"; LWINE="FFFBE9EF"; LGOLD="FFFFF6E0"; GREY="FFF2F2F2"
WHITE="FFFFFFFF"; INK="FF333333"; FONT="Microsoft JhengHei"
thin=Side(style="thin",color="FFD0B070"); border=Border(thin,thin,thin,thin)

def hdr(c):
    c.fill=PatternFill("solid",fgColor=WINE); c.font=Font(name=FONT,bold=True,size=11,color=WHITE)
    c.alignment=Alignment("center","center",wrap_text=True); c.border=border
def body(c, zebra=False, align="left"):
    c.font=Font(name=FONT,size=10,color=INK)
    c.alignment=Alignment(align,"center",wrap_text=True); c.border=border
    if zebra: c.fill=PatternFill("solid",fgColor=GREY)

wb=Workbook()
# 五分頁：說明 / 資料表總覽 / 來源表欄位 / 目標表欄位 / 對照碼與篩選
# 每張表頭列套 hdr()，資料列套 body()（奇偶斑馬），欄寬用 ws.column_dimensions[L].width=
wb.save("working/PROC_資料字典.xlsx")   # 先寫 working/
```

**分頁欄位建議：**
- 說明：兩欄（項目／內容）— 程序名、輸入參數、目標表、處理對象、各階段、稽核機制。
- 資料表總覽：資料表全名｜Schema｜類型(來源/目標/參數/稽核)｜中文說明｜在程序中的角色。
- 來源表欄位：資料表｜欄位｜中文說明｜用途/加工備註。
- 目標表欄位：欄位｜中文說明｜資料來源｜加工/計算邏輯｜寫入階段。
- 對照碼與篩選：分節列出值對照（如 FLAG→代碼）、計算分類規則、納入/排除篩選條件。

---

## C. ★ 讓 Excel 不跳「修復」視窗（關鍵）

openpyxl 直接存的檔，Excel 嚴格解析會因色碼透明位元（6 碼被補成 `00xxxxxx`）或非標準字串結構而判定毀損。
**先寫到 `working/`，再用 LibreOffice 轉檔正規化輸出到 `output/`：**

```bash
soffice --headless --convert-to xlsx --outdir output working/PROC_資料字典.xlsx
```

轉檔後 LibreOffice 會重寫成標準結構（含 `xl/sharedStrings.xml`、標準 styles）。
注意：`output/` 掛載偶有覆寫鎖定，故用 `--outdir output` 由 soffice 直接建立；若目標已存在先 `rm -f` 再轉。

---

## D. 還原 Big5/CP950 中文註解

```python
raw = open(path, "rb").read()
text = raw.decode("big5", "replace")     # 亂碼時改 "cp950" / "gb18030"
open("working/proc_decoded.txt","w",encoding="utf-8").write(text)
```

---

## E. 交付前驗證

```python
import zipfile, re, xml.dom.minidom as m
from openpyxl import load_workbook
p="output/PROC_資料字典.xlsx"; z=zipfile.ZipFile(p)
assert any("sharedStrings" in n for n in z.namelist()), "缺 sharedStrings — 未經 LibreOffice 正規化"
for n in z.namelist():
    if n.endswith((".xml",".rels")): m.parseString(z.read(n))   # XML 合法
assert not re.findall(r'rgb="00[0-9A-Fa-f]{6}"', z.read("xl/styles.xml").decode().split("<colors>")[0])
wb=load_workbook(p); assert len(wb.sheetnames)==5
m.parse("output/PROC_流程圖.drawio")   # drawio 合法
```
