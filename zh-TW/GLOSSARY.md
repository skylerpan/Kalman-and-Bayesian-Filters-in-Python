# 術語表 Glossary

本翻譯版的術語以英文為主，中文放在旁邊作為輔助。每一本 notebook（每一章）中，術語**第一次**出現時寫成「English（中文）」，之後同一章只寫英文。本表是翻譯時統一用語的依據，也方便讀者查閱。

## 濾波器與估計 Filters and estimation

| English | 中文 |
|---|---|
| filter | 濾波器 |
| g-h filter / alpha-beta filter | g-h 濾波器（保留原名） |
| Kalman filter | 卡爾曼濾波器 |
| extended Kalman filter (EKF) | 擴展卡爾曼濾波器 |
| unscented Kalman filter (UKF) | 無損卡爾曼濾波器 |
| ensemble Kalman filter (EnKF) | 系集卡爾曼濾波器 |
| particle filter | 粒子濾波器 |
| H-infinity filter | H∞ 濾波器（保留原名） |
| least squares filter | 最小平方濾波器 |
| discrete Bayes filter | 離散貝氏濾波器 |
| multivariate Kalman filter | 多變量卡爾曼濾波器 |
| univariate / one-dimensional | 單變量 / 一維 |
| estimate | 估計值 |
| estimation | 估計 |
| prediction / predict step | 預測 / 預測步驟 |
| update step | 更新步驟 |
| predict/update cycle | 預測／更新循環 |
| tracking | 追蹤 |
| smoothing / smoother | 平滑 / 平滑器 |
| RTS smoother (Rauch-Tung-Striebel) | RTS 平滑器 |
| fixed-lag smoother | 固定延遲平滑器 |
| adaptive filtering | 適應性濾波 |
| sensor fusion | 感測器融合 |
| Kalman gain | 卡爾曼增益 |
| residual | 殘差 |
| innovation | 新息 |
| gating | 閘控 |
| fading memory filter | 衰減記憶濾波器 |
| multiple model estimation (MMAE / IMM) | 多模型估計 / 互動多模型 |
| divergence | 發散 |
| convergence | 收斂 |
| steady state | 穩態 |
| observability | 可觀測性 |

## 狀態與模型 State and models

| English | 中文 |
|---|---|
| state | 狀態 |
| state variable | 狀態變數 |
| state vector | 狀態向量 |
| state transition function / matrix | 狀態轉移函數 / 矩陣 |
| process model | 過程模型 |
| measurement model / function | 量測模型 / 函數 |
| measurement | 量測（值） |
| sensor | 感測器 |
| control input | 控制輸入 |
| control function / matrix | 控制函數 / 矩陣 |
| process noise | 過程雜訊 |
| measurement noise | 量測雜訊 |
| white noise | 白雜訊 |
| noise | 雜訊 |
| system model | 系統模型 |
| observed / hidden variable | 可觀測 / 隱藏變數 |
| dynamic system | 動態系統 |
| time step | 時間步 |
| epoch | 時刻 |
| linear / nonlinear | 線性 / 非線性 |
| linearization | 線性化 |
| Jacobian | 雅可比矩陣 |
| Taylor series | 泰勒級數 |
| sigma points | sigma 點 |
| unscented transform | 無損轉換 |
| resampling | 重採樣 |
| importance sampling | 重要性採樣 |
| Monte Carlo | 蒙地卡羅（法） |
| particle | 粒子 |
| degeneracy | 退化 |
| discretization | 離散化 |
| Newtonian equations / kinematics | 牛頓運動方程 / 運動學 |
| constant velocity / acceleration model | 等速 / 等加速模型 |

## 機率與統計 Probability and statistics

| English | 中文 |
|---|---|
| probability | 機率 |
| probability distribution | 機率分布 |
| probability density function (pdf) | 機率密度函數 |
| random variable | 隨機變數 |
| Gaussian / normal distribution | 高斯分布 / 常態分布 |
| multivariate Gaussian | 多變量高斯分布 |
| mean | 平均值 |
| expected value | 期望值 |
| median | 中位數 |
| mode | 眾數 |
| variance | 變異數 |
| standard deviation | 標準差 |
| covariance | 共變異數 |
| covariance matrix | 共變異數矩陣 |
| correlation | 相關性 |
| prior | 先驗 |
| posterior | 後驗 |
| likelihood | 似然 |
| evidence | 證據 |
| Bayes' theorem | 貝氏定理 |
| Bayesian | 貝氏 |
| conditional probability | 條件機率 |
| joint probability | 聯合機率 |
| marginal | 邊際 |
| normalization | 正規化 |
| convolution | 捲積 |
| histogram | 直方圖 |
| belief | 信念 |
| uncertainty | 不確定性 |
| confidence interval | 信賴區間 |
| standard error | 標準誤差 |
| total probability theorem | 全機率定理 |
| central limit theorem | 中央極限定理 |
| independent and identically distributed (iid) | 獨立同分布 |
| sampling | 取樣 |
| weight (of a sample) | 權重 |
| outlier | 離群值 |
| bias | 偏差 |
| unbiased | 無偏 |
| error ellipse / covariance ellipse | 誤差橢圓 / 共變異數橢圓 |
| Mahalanobis distance | 馬氏距離 |
| chi-squared | 卡方 |
| Markov chain | 馬可夫鏈 |
| Markov property | 馬可夫性質 |
| hidden Markov model | 隱馬可夫模型 |

## 數學與程式 Math and code

| English | 中文 |
|---|---|
| matrix | 矩陣 |
| vector | 向量 |
| transpose | 轉置 |
| inverse | 反矩陣 |
| identity matrix | 單位矩陣 |
| determinant | 行列式 |
| eigenvalue / eigenvector | 特徵值 / 特徵向量 |
| dot product | 內積 |
| element-wise | 逐元素 |
| derivative | 導數 |
| integral | 積分 |
| differential equation | 微分方程 |
| closed form | 閉合形式 |
| numerical integration | 數值積分 |
| Runge-Kutta | 龍格－庫塔（法） |
| interpolation | 內插 |
| extrapolation | 外插 |
| simulation | 模擬 |
| ground truth | 真實值 |
| tuning (a filter) | 調校 |
| design (a filter) | 設計 |
| performance | 效能 |
| bandwidth | 頻寬 |
| frequency response | 頻率響應 |
| lag | 延遲 |
| overshoot | 過衝 |
| ringing | 振盪 |
| gain | 增益 |
| scaling factor | 比例因子 |
| hypothesis | 假說 |
| iterative | 迭代 |
| recursive | 遞迴 |
| batch processing | 批次處理 |

## 常見句型用語 Common wording

| English | 中文 |
|---|---|
| intuition | 直覺 |
| exercise | 練習 |
| solution | 解答 |
| summary | 小結 |
| references | 參考文獻 |
| Table of Contents | 目錄 |
| chapter | 章 |
| appendix | 附錄 |
| notebook | notebook（保留） |
| cell | cell（保留） |
| plot / chart | 圖 |
| dog tracking example | 狗追蹤範例 |
| pound (lb) | 磅 |
