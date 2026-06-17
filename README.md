# 🧰 My Used Skills

這裡整理的是「我平常會使用的 AI SKILLS」。  
你可以把它想成一個技能工具箱：不同 AI / 平台有不同專長，每個資料夾裡都有一份 `SKILL.md`，說明這個 skill 什麼時候該用、怎麼用、要注意什麼。

## 🗂️ 專案目錄

```text
MyUsedSkills/
├─ README.md                         # 這份總覽說明
├─ Codex/                            # OpenAI Codex 使用的 skills
│  ├─ bank-ai-excel-article-generator/
│  │  └─ SKILL.md                    # 產生銀行業 AI + Excel FAQ 文章
│  ├─ deploy-to-vercel/
│  │  ├─ SKILL.md                    # 部署網站到 Vercel
│  │  └─ agents/openai.yaml
│  ├─ git-commit-push/
│  │  ├─ SKILL.md                    # Git commit + push 流程
│  │  ├─ scripts/git_commit_push.py
│  │  └─ agents/openai.yaml
│  ├─ git-ignore-warning-fix/
│  │  ├─ SKILL.md                    # 修正 Codex Git ignore 權限警告
│  │  └─ agents/openai.yaml
│  └─ restore-git-version/
│     ├─ SKILL.md                    # 還原 Git 專案到遠端最新版
│     └─ agents/openai.yaml
└─ M365 Copilot/                     # Microsoft 365 Copilot 使用的 skills
   ├─ bot-brand-styling/
   │  └─ SKILL.md                    # 套用臺銀品牌配色到文件內容
   ├─ bot-brand-theme/
   │  └─ SKILL.md                    # 產生臺銀 Office 佈景主題檔
   ├─ bot-credit-risk-report/
   │  └─ SKILL.md                    # 產生授信戶重大變故風險評估報告
   ├─ bot-fund-dca-planner/
   │  └─ SKILL.md                    # 臺銀月報轉定期定額基金規劃 Excel
   ├─ bot-news-briefing/
   │  └─ SKILL.md                    # 整理臺銀相關新聞一頁式簡報
   ├─ bot-sql-summary-report/
   │  └─ SKILL.md                    # SQL 查詢彙總轉 HTML 報表與儀表板
   ├─ bot-training-manual/
   │  └─ SKILL.md                    # 簡報或文件轉教育訓練手冊
   └─ credit-risk-briefing/
      └─ SKILL.md                    # 信用風險新聞一頁式摘要
```

## 📌 分類總覽

| AI / 平台 | Skills 數量 | 這類 skill 主要幫我做什麼 |
|---|---:|---|
| 🤖 Codex | 5 | 寫程式、部署網站、處理 Git、產生文章 |
| 💼 M365 Copilot | 8 | 整理 Word / Excel / 新聞 / 風險報告，並套用臺銀品牌樣式 |

## 🤖 Codex Skills

Codex 類的 skills 偏向「工程師工作流程」：例如 Git、部署、自動產生 Markdown 文章。

| Skill | 一般人版說明 | 檔案 |
|---|---|---|
| 🏦 bank-ai-excel-article-generator | 幫我產生「銀行業 AI 與 Excel 協作」的 FAQ 文章，會避免跟既有文章重複。 | [SKILL.md](./Codex/bank-ai-excel-article-generator/SKILL.md) |
| 🚀 deploy-to-vercel | 幫我把網站或前端專案部署到 Vercel，並確認上線後檔案能正常開啟。 | [SKILL.md](./Codex/deploy-to-vercel/SKILL.md) |
| ✅ git-commit-push | 幫我把目前修改整理成 Git commit，然後 push 到遠端分支。 | [SKILL.md](./Codex/git-commit-push/SKILL.md) |
| 🛠️ git-ignore-warning-fix | 修正 Codex 執行 Git 時常見的 ignore 權限警告，避免每次 `git status` 都跳提示。 | [SKILL.md](./Codex/git-ignore-warning-fix/SKILL.md) |
| ↩️ restore-git-version | 當專案想回到 GitHub / origin 上的最新版時，幫我安全還原本機資料夾。 | [SKILL.md](./Codex/restore-git-version/SKILL.md) |

## 💼 M365 Copilot Skills

M365 Copilot 類的 skills 偏向「辦公室文件與分析工作」：新聞摘要、風險報告、教育訓練手冊、Excel 報表與臺銀品牌樣式。

| Skill | 一般人版說明 | 檔案 |
|---|---|---|
| 🎨 bot-brand-styling | 幫 Word、PowerPoint、Excel 內容直接套用臺灣銀行品牌配色與字型。 | [SKILL.md](./M365%20Copilot/bot-brand-styling/SKILL.md) |
| 🧩 bot-brand-theme | 產生可重複套用的臺銀 Office 佈景主題檔 `.thmx`。 | [SKILL.md](./M365%20Copilot/bot-brand-theme/SKILL.md) |
| 📄 bot-credit-risk-report | 將授信戶重大變故、授信往來資料、研究報告與新聞整理成 Word 風險評估報告。 | [SKILL.md](./M365%20Copilot/bot-credit-risk-report/SKILL.md) |
| 📈 bot-fund-dca-planner | 將臺銀投資組合建議月報 PDF 轉成定期定額基金規劃 Excel，包含候選基金、三組投資組合與比較圖表。 | [SKILL.md](./M365%20Copilot/bot-fund-dca-planner/SKILL.md) |
| 📰 bot-news-briefing | 從新聞彙整裡挑出臺銀相關新聞，整理成高層可快速閱讀的一頁式摘要。 | [SKILL.md](./M365%20Copilot/bot-news-briefing/SKILL.md) |
| 📊 bot-sql-summary-report | 將 SQL 查詢彙總 Excel 轉成 HTML 報表、儀表板與 ZIP 交付檔。 | [SKILL.md](./M365%20Copilot/bot-sql-summary-report/SKILL.md) |
| 📚 bot-training-manual | 把簡報或文件改寫成臺銀配色的教育訓練手冊，包含流程圖與落地使用章節。 | [SKILL.md](./M365%20Copilot/bot-training-manual/SKILL.md) |
| ⚠️ credit-risk-briefing | 從每日新聞中篩選信用風險相關內容，整理成一頁式信用風險摘要。 | [SKILL.md](./M365%20Copilot/credit-risk-briefing/SKILL.md) |

## 🧭 怎麼看這個專案？

- 想知道有哪些 skills：先看本 README。
- 想知道某個 skill 的完整規則：點進該 skill 的 `SKILL.md`。
- 想新增 skill：放進對應 AI / 平台資料夾。
- 想新增另一種 AI：建立新的資料夾，並在本 README 補上分類。

## 🧹 維護規則

- 📁 每個 skill 都放在自己的資料夾。
- 📝 每個 skill 都要有 `SKILL.md`。
- 🧠 `SKILL.md` 內容應該說清楚「什麼時候用、怎麼做、不能做什麼」。
- 🔗 新增或刪除 skill 後，要同步更新本 README 的目錄與表格。
- 🧪 如果 skill 內有腳本，建議放在該 skill 自己的 `scripts/` 資料夾。
