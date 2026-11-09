# 讀書筆記索引（zh-TW）

本資料夾收錄對《Kalman and Bayesian Filters in Python》繁體中文版各章的講解與補充推導。內容是對章節 notebook 的延伸說明，不取代原書。

## 目錄結構

```
docs/notes/
├── README.md                              本索引
├── chapters/                              依章節整理的講解
│   ├── notes-ch02-discrete-bayes.md
│   ├── notes-ch03-gaussians.md
│   ├── notes-ch04-one-dimensional-kalman-filters.md
│   ├── notes-ch05-multivariate-gaussians.md
│   ├── notes-ch06-kalman-gain-and-tuning.md
│   ├── notes-ch07-kalman-filter-math.md
│   └── notes-ch08-designing-kalman-filters.md
└── topics/                                跨章節的專題
    └── notes-kalman-gain-and-QR.md
```

## 章節講解

| 檔案 | 對應 notebook | 主要內容 |
|---|---|---|
| `chapters/notes-ch02-discrete-bayes.md` | `02-Discrete-Bayes.ipynb` | 走廊追蹤狗的情境、先驗與後驗、感測器雜訊與正規化、移動的 convolution、預測與更新的循環、壞量測的影響、倉庫列車的控制與模擬 |
| `chapters/notes-ch03-gaussians.md` | `03-Gaussians.ipynb` | 平均值、變異數與標準差、高斯分布的兩個參數、高斯的加法與乘法、貝氏定理與全機率定理、高斯建模的限制 |
| `chapters/notes-ch04-one-dimensional-kalman-filters.md` | `04-One-Dimensional-Kalman-Filters.ipynb` | 用高斯取代直方圖、predict 與 update 的實作、第一個一維 Kalman filter、Kalman gain 與演算法總覽、參數實驗、固定增益濾波器 |
| `chapters/notes-ch05-multivariate-gaussians.md` | `05-Multivariate-Gaussians.ipynb` | 共變異數矩陣、誤差橢圓、多維高斯相乘（雷達三角定位）、隱藏變數的推理拆解 |
| `chapters/notes-ch06-kalman-gain-and-tuning.md` | `06-Multivariate-Kalman-Filters.ipynb` | 多變量 Kalman 增益的兩種推導（資訊形式、最小均方誤差）、R 與 Q 的調整方法與診斷 |
| `chapters/notes-ch07-kalman-filter-math.md` | `07-Kalman-Filter-Math.ipynb` | 狀態空間與矩陣指數求 $\mathbf F$、連續與分段白雜訊求 $\mathbf Q$、Joseph 形式、Kalman 增益的 trace 推導、數值積分、與 g-h filter 的關係 |
| `chapters/notes-ch08-designing-kalman-filters.md` | `08-Designing-Kalman-Filters.ipynb` | 設計流程（狀態、$\mathbf F$、$\mathbf Q$、$\mathbf B$、$\mathbf H$、$\mathbf R$、初始條件）、濾波器階數、gating 與 Mahalanobis 距離、效能評估、融合、拋球與空氣阻力 |

## 專題

| 檔案 | 主要內容 |
|---|---|
| `topics/notes-kalman-gain-and-QR.md` | 從高斯乘法推出 Kalman 增益（一維），以及 process_var（Q）與 sensor_var（R）的取捨。與第 04 章的內容直接相關。 |

## 閱讀建議

- 初次學習貝氏濾波的人：從 `notes-ch02` 開始，它用最直覺的離散例子建立概念。
- 接著讀 `notes-ch03` → `notes-ch04`，理解高斯如何取代離散格子，再看 `topics/` 中的增益推導。
- 想知道多維濾波器怎麼來：`notes-ch05`（共變異數與隱藏變數）→ `notes-ch06`（多維 Kalman filter）。
- 想補足數學：`notes-ch07` 的推導最完整。
- 想知道如何設計實際濾波器：直接看 `notes-ch08`，並回頭參考 `notes-ch06` 的 R、Q 調整。

## 說明

- 文中標註「本文補充」的推導與數值，是對原書的延伸，不是書中的內容。
- 數值範例若標註「本文計算」，是以簡單程式算出，數字可能與書中的示意圖不同。
- 第 02、03、04 章的筆記是依對話中的講解整理而成，內容與原書一致，但不含本文補充的數值驗算。
