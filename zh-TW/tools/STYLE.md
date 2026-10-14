# 翻譯風格規範 STYLE

適用於 `zh-TW/` 內所有 notebook 的 markdown cell。目標讀者：會英文技術術語、但偏好用繁體中文閱讀說明文字的工程師／學生。

## 1. 術語：英文為主、中文補充
- 每一本 notebook（= 一章）中，技術術語**第一次出現**時寫成「English（中文）」，使用全形括號，例如：
  `Kalman filter（卡爾曼濾波器）`、`covariance（共變異數）`、`prior（先驗）`。
- 同一本 notebook **之後再出現**同一術語，只寫英文：`Kalman filter`、`covariance`、`prior`。
- 中文譯名以 `GLOSSARY.md` 為準；表裡沒有的術語自行用台灣慣用譯法，並維持同一章內一致。
- 一本 notebook 若被切成多個 part：只有 **part 1** 負責「首次出現附中文」；part 2 以後一律只寫英文術語（可以假設 part 1 已經標注過常見術語）。
- 下列東西永遠保持英文、不翻譯：變數名、函式名、矩陣符號（`x`, `P`, `F`, `H`, `R`, `Q`, `K`）、套件名（NumPy、SciPy、FilterPy、Matplotlib、Jupyter、SymPy）、人名、書名、檔名。
- `notebook`、`cell`、`kernel`、`magic` 這類 Jupyter 用語保留英文。

## 2. 標題
- 標題翻成中文並保留英文術語，格式「English（中文）」或在中文句子裡保留術語：
  - `# The g-h Filter` → `# g-h Filter（g-h 濾波器）`
  - `## Kalman Gain` → `## Kalman Gain（卡爾曼增益）`
  - `## Tracking a Dog` → `## 追蹤一隻狗 Tracking a Dog`
  - `## Summary` → `## 小結`、`## Exercise: ...` → `## 練習：...`、`## Solution` → `## 解答`、`## References` → `## 參考文獻`
- 標題的 `#` 數量與行數必須和原文完全相同。
- `[Table of Contents](./table_of_contents.ipynb)` → `[目錄 Table of Contents](./table_of_contents.ipynb)`（連結不變）。

## 3. 絕對不可更動的內容
- LaTeX：`$...$`、`$$...$$`、`\begin{...}` 區塊內的一切。`$` 的數量必須與原文相同。LaTeX 裡的 `\text{...}`、`\mathbf{...}` 也不要翻。
- 行內程式碼 `` `code` `` 與 ``` 程式碼區塊。
- 所有 URL、圖片路徑（`![...](./figs/x.png)`、`<img src=...>`）、HTML 標籤。
- 數字、單位（lbs、meters、m/s）、公式編號。
- Markdown 結構：段落切分、列表（`*`、`1.`）、粗體 `**`、斜體 `*`、引用 `>`、表格。保持一一對應。
- 不可增加、刪除或合併 cell；輸出 JSON 的 `i` 值與順序必須與輸入相同。

## 4. 文字風格
- 用台灣繁體中文與台灣慣用語（軟體、程式、資料、函式、矩陣、變異數）；不要用簡體或中國大陸用語（软件、程序、数据、方差）。
- 中文與英文／數字之間留一個半形空格：`用 NumPy 計算 3 個 sigma 點`。
- 中文標點用全形（，。：；？！「」），英文術語內的標點照原文。
- 保留作者 Roger Labbe 的第一人稱、口語且親切的語氣（「我」、「我們」、「你」）。作者的幽默與自嘲照翻，不要刪。
- 翻譯要完整：每一句英文都要有對應的中文，不可摘要、不可省略段落。
- 不加入譯者意見。真的需要補充時用「（譯註：…）」，一章最多幾處。
- 連結文字可翻譯，URL 不可動：`[Jupyter Notebooks](http://jupyter.org/)` → `[Jupyter Notebook](http://jupyter.org/)`。
- 書名《Kalman and Bayesian Filters in Python》保留英文。
- 參考文獻（References）列表中的作者、論文名、期刊名保留英文，不翻譯。

## 5. 輸出格式
- 輸出與輸入相同結構的 JSON：`{"notebook", "part", "nparts", "cells": [{"i", "src"}, ...]}`，`src` 為翻譯後的 markdown 全文。
- 必須是合法 JSON（換行用 `\n`、引號要跳脫）。用 Python 的 `json.dump(..., ensure_ascii=False, indent=1)` 寫出最保險。
