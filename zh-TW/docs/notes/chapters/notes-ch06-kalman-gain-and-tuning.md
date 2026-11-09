# 第 06 章補充：多變量 Kalman 增益的推導，以及 R 與 Q 的調整

本文延伸 `06-Multivariate-Kalman-Filters.ipynb` 的兩個主題：

1. Kalman 增益 $\mathbf K$ 的完整推導（書中只給公式，沒有證明）。
2. 量測雜訊 $\mathbf R$ 與過程雜訊 $\mathbf Q$ 的調整方法。

數值範例中，標註「本文計算」的是我用簡單程式算出來的結果，不是書中的數字。

---

# 一、Kalman 增益的完整推導

## 1.1 問題設定

- 先驗（prior）：狀態的真實值 $\mathbf x$ 滿足 $\mathbf x \sim \mathcal N(\bar{\mathbf x},\,\bar{\mathbf P})$。
- 量測模型：$\mathbf z = \mathbf H\mathbf x + \mathbf v$，其中 $\mathbf v \sim \mathcal N(\mathbf 0,\,\mathbf R)$。
- 目標：找一個後驗估計 $\hat{\mathbf x}$ 與後驗協方差 $\mathbf P$，使它是 $\mathbf x$ 的最佳估計。

Kalman 更新的形式是：

$$\hat{\mathbf x} = \bar{\mathbf x} + \mathbf K(\mathbf z - \mathbf H\bar{\mathbf x})$$

也就是「prior + 增益 × 殘差」。問題在於：**這個 $\mathbf K$ 應該是多少？**

下面用兩種方法推導，結果一致。

## 1.2 推導路線 A：資訊形式（Bayes 的觀點）

這個路線與第 05 章的高斯相乘是同一件事，只是推廣到矩陣。

**步驟 1：寫出後驗的對數機率**

先驗與似然的對數（忽略常數）為：

$$-\tfrac12(\mathbf x-\bar{\mathbf x})^\mathsf T\bar{\mathbf P}^{-1}(\mathbf x-\bar{\mathbf x}) \;-\; \tfrac12(\mathbf z-\mathbf H\mathbf x)^\mathsf T\mathbf R^{-1}(\mathbf z-\mathbf H\mathbf x)$$

兩者相加就是後驗的對數機率。

**步驟 2：配方，讀出後驗的精度矩陣**

對 $\mathbf x$ 的二次項係數給出後驗的精度（協方差的反矩陣）：

$$\mathbf P^{-1} = \bar{\mathbf P}^{-1} + \mathbf H^\mathsf T\mathbf R^{-1}\mathbf H$$

**步驟 3：用矩陣反演引理（Woodbury）化簡**

矩陣反演引理告訴我們：

$$\mathbf P = \bar{\mathbf P} - \bar{\mathbf P}\mathbf H^\mathsf T(\mathbf H\bar{\mathbf P}\mathbf H^\mathsf T + \mathbf R)^{-1}\mathbf H\bar{\mathbf P}$$

令 $\mathbf S = \mathbf H\bar{\mathbf P}\mathbf H^\mathsf T + \mathbf R$，則 $\mathbf P = \bar{\mathbf P} - \bar{\mathbf P}\mathbf H^\mathsf T\mathbf S^{-1}\mathbf H\bar{\mathbf P}$。

**步驟 4：得到增益**

後驗均值的線性形式中，$\mathbf x$ 的係數是 $\mathbf P\mathbf H^\mathsf T\mathbf R^{-1}$，利用步驟 3 的結果可化為：

$$\mathbf K = \mathbf P\mathbf H^\mathsf T\mathbf R^{-1} = \bar{\mathbf P}\mathbf H^\mathsf T\mathbf S^{-1}$$

**與第 05 章的對應**：若 $\mathbf H = \mathbf I$（直接量測全部狀態），則
$$\mathbf P = \bar{\mathbf P}(\bar{\mathbf P}+\mathbf R)^{-1}\mathbf R$$
這正是第 05 章的公式 $\Sigma = \Sigma_1(\Sigma_1+\Sigma_2)^{-1}\Sigma_2$，其中 $\Sigma_1=\bar{\mathbf P}$（先驗）、$\Sigma_2=\mathbf R$（量測）。

## 1.3 推導路線 B：最小化均方誤差（估計理論的觀點）

這個路線不需要假設高斯，只要求估計誤差的均方最小。

**步驟 1：線性形式的假設**

假設 $\hat{\mathbf x} = \bar{\mathbf x} + \mathbf K(\mathbf z - \mathbf H\bar{\mathbf x})$，目標是選 $\mathbf K$ 使後驗誤差協方差的跡（trace）最小。

**步驟 2：後驗誤差協方差的一般形式（Joseph 形式）**

對任意的 $\mathbf K$，後驗誤差協方差可以寫成：

$$\mathbf P(\mathbf K) = (\mathbf I-\mathbf K\mathbf H)\bar{\mathbf P}(\mathbf I-\mathbf K\mathbf H)^\mathsf T + \mathbf K\mathbf R\mathbf K^\mathsf T$$

這個式子對任意 $\mathbf K$ 都成立，不只最佳的 $\mathbf K$。它也比 $(\mathbf I-\mathbf K\mathbf H)\bar{\mathbf P}$ 數值上更穩定，因為它保證對稱、半正定。

**步驟 3：展開**

$$\mathbf P(\mathbf K) = \bar{\mathbf P} - \mathbf K\mathbf H\bar{\mathbf P} - \bar{\mathbf P}\mathbf H^\mathsf T\mathbf K^\mathsf T + \mathbf K\mathbf S\mathbf K^\mathsf T$$

其中已用到 $\mathbf S = \mathbf H\bar{\mathbf P}\mathbf H^\mathsf T + \mathbf R$。

**步驟 4：配方（completing the square）**

把含 $\mathbf K$ 的項寫成完全平方：

$$\mathbf P(\mathbf K) = \underbrace{(\mathbf K - \bar{\mathbf P}\mathbf H^\mathsf T\mathbf S^{-1})\,\mathbf S\,(\mathbf K - \bar{\mathbf P}\mathbf H^\mathsf T\mathbf S^{-1})^\mathsf T}_{\text{半正定，最小值為 }0} + \bar{\mathbf P} - \bar{\mathbf P}\mathbf H^\mathsf T\mathbf S^{-1}\mathbf H\bar{\mathbf P}$$

**步驟 5：找出最小值**

第一項是半正定矩陣，在
$$\mathbf K = \bar{\mathbf P}\mathbf H^\mathsf T\mathbf S^{-1}$$
時為零。此時後驗協方差最小：

$$\mathbf P = \bar{\mathbf P} - \bar{\mathbf P}\mathbf H^\mathsf T\mathbf S^{-1}\mathbf H\bar{\mathbf P} = (\mathbf I-\mathbf K\mathbf H)\bar{\mathbf P}$$

這與路線 A 的結果一致。

## 1.4 純量情況檢查

令 $\mathbf H = 1$、$\bar{\mathbf P} = P$、$\mathbf R = R$（都是純量），則：

$$K = \frac{P}{P+R}, \qquad P_{\text{post}} = (1-K)P = \frac{PR}{P+R}$$

與一維 Kalman 濾波器的結果相同。

## 1.5 數值範例（本文計算）

設 prior 協方差為 $\bar{\mathbf P} = \begin{bmatrix}4&2\\2&3\end{bmatrix}$（位置、速度），$\mathbf H = [1\ \ 0]$，$R = 1$。

**(a) 計算 S**

$$\mathbf S = \mathbf H\bar{\mathbf P}\mathbf H^\mathsf T + R = 4 + 1 = 5$$

**(b) 計算 K**

$$\bar{\mathbf P}\mathbf H^\mathsf T = \begin{bmatrix}4\\2\end{bmatrix},\qquad \mathbf K = \frac{1}{5}\begin{bmatrix}4\\2\end{bmatrix} = \begin{bmatrix}0.8\\0.4\end{bmatrix}$$

**(c) 狀態更新**

假設先驗 $\bar{\mathbf x} = [3,\,1]^\mathsf T$，量測 $z = 6$，則殘差 $y = 6 - 3 = 3$：

$$\hat{\mathbf x} = \begin{bmatrix}3\\1\end{bmatrix} + \begin{bmatrix}0.8\\0.4\end{bmatrix}\cdot 3 = \begin{bmatrix}5.4\\2.2\end{bmatrix}$$

位置從 3 移向量測 6，變成 5.4。**速度也被修正了**，從 1 變成 2.2，雖然我們沒有量測速度。

**(d) 協方差更新**

$$\mathbf P = \bar{\mathbf P} - \mathbf K\mathbf S\mathbf K^\mathsf T = \begin{bmatrix}4&2\\2&3\end{bmatrix} - \begin{bmatrix}3.2&1.6\\1.6&0.8\end{bmatrix} = \begin{bmatrix}0.8&0.4\\0.4&2.2\end{bmatrix}$$

可以用 $(\mathbf I-\mathbf K\mathbf H)\bar{\mathbf P}$ 驗證，結果相同。

**重點解讀**

- 速度的修正量 $K_2 = 0.4$ 不為零，原因是先驗的交叉項 $\bar P_{12} = 2$ 不為零。
- 速度的變異數從 3 降到 2.2，減少量為 $K_2\cdot\bar P_{12} = 0.4\times 2 = 0.8$。
- **如果 $\bar P_{12} = 0$**，則 $K_2 = 0$，速度完全不會被修正。這正是第 05 章說的「相關性就是資訊」。

## 1.6 增益的直覺

$$\mathbf K = \bar{\mathbf P}\mathbf H^\mathsf T\,\mathbf S^{-1}$$

- $\bar{\mathbf P}\mathbf H^\mathsf T$：先驗的不確定性「投影」到量測空間，也就是「預測的量測」有多不確定。
- $\mathbf S^{-1}$：總不確定性（先驗投影 + 量測雜訊）的倒數。
- 所以 $\mathbf K$ 可以讀成：**預測的不確定性 ÷ 總不確定性**。預測越不確定，就越依賴量測。

**單位檢查**：若狀態單位是 m、量測單位是 m，則 $\bar{\mathbf P}\mathbf H^\mathsf T$ 單位是 m²、$\mathbf S$ 單位是 m²，所以 $\mathbf K$ 無單位。若量測單位不同（例如電壓），$\mathbf K$ 的單位會是「狀態單位 / 量測單位」，使 $\mathbf K\mathbf y$ 的單位回到狀態單位。

## 1.7 實作上的注意事項

- $\mathbf S$ 必須可逆。只要 $\mathbf R$ 是正定的，$\mathbf S$ 就是正定的，這點不用擔心。
- 實務上不直接算 $\mathbf S^{-1}$，而是解線性方程組（例如 `np.linalg.solve`），數值上較穩定。
- 更新協方差時，建議用 Joseph 形式，避免數值誤差讓 $\mathbf P$ 失去對稱性或變成負定。
- FilterPy 的 `update()` 內部已處理這些細節。

---

# 二、R 與 Q 的調整

## 2.1 兩者各自代表什麼

| 符號 | 名稱 | 意義 | 來源 |
|---|---|---|---|
| $\mathbf R$ | 量測雜訊協方差 | 感測器有多不準 | 規格書、靜態量測、校正實驗 |
| $\mathbf Q$ | 過程雜訊協方差 | 模型有多不準，狀態在兩步之間有多少未被模型解釋的變化 | 系統的物理特性、模型誤差分析 |

- $\mathbf R$ 只出現在更新步驟，描述「我有多不信量測」。
- $\mathbf Q$ 只出現在預測步驟，描述「我有多不信模型」。

## 2.2 它們如何影響增益

由 $\bar{\mathbf P} = \mathbf F\mathbf P\mathbf F^\mathsf T + \mathbf Q$ 與 $\mathbf K = \bar{\mathbf P}\mathbf H^\mathsf T\mathbf S^{-1}$ 可以看出：

- **$\mathbf Q$ 變大** → $\bar{\mathbf P}$ 變大 → $\mathbf K$ 變大 → 更相信量測。
- **$\mathbf R$ 變大** → $\mathbf S$ 變大 → $\mathbf K$ 變小 → 更相信預測。

一個重要的性質：**若把 $\mathbf Q$、$\mathbf R$、初始 $\mathbf P$ 全部乘上同一個常數 $c$，則 $\mathbf K$ 不變，$\mathbf P$ 會乘上 $c$**。所以真正影響 $\mathbf K$ 的是 $\mathbf Q$ 與 $\mathbf R$ 的相對大小，而不是絕對值。但 $\mathbf P$ 的絕對大小仍然有意義，會影響對誤差的解讀（例如誤差橢圓的大小）。

## 2.3 書中的實驗回顧

書中（第 06 章「調整 Filter」一節）用的設定：

- 把 $\mathbf R$ 設為 225 m²。這是刻意放大的值，用來讓 Q 的效果更明顯，不是真實感測器的值。
- **Q = 20 m²（大）**：濾波器緊跟量測，雜訊很大，因為它不信任預測。
- **Q = 0.02 m²（小）**：輸出很平滑，但 $\mathbf P$ 一直沒有收斂，而且初始位置猜錯 50 m 時無法鎖定軌跡。
- 作者的經驗法則：$\mathbf Q$ 的量級約在 $\tfrac12\Delta a$ 到 $\Delta a$ 之間，其中 $\Delta a$ 是加速度在相鄰取樣之間可能變化的最大量。這是書中在「加速度為常數、各時間區段互不相關」假設下的建議。

## 2.4 本文計算：穩態增益隨 Q、R 變化

**模型設定**（本文假設，與書中的參數化不同）：

- 狀態 $\mathbf x = [x,\,v]^\mathsf T$，$\mathbf F = \begin{bmatrix}1&\Delta t\\0&1\end{bmatrix}$，$\Delta t = 0.1$，$\mathbf H = [1\ \ 0]$。
- 過程雜訊採用常見的離散白雜訊加速度模型：$\mathbf Q = q\begin{bmatrix}\Delta t^4/4 & \Delta t^3/2\\ \Delta t^3/2 & \Delta t^2\end{bmatrix}$，$q$ 是加速度雜訊的強度。
- 初始 $\mathbf P = \mathrm{diag}(500, 49)$，迭代 2000 次至穩態。

**表 1：改變 $q$（$R = 225$）**

| $q$ | $K_\text{pos}$ | $K_\text{vel}$ | 後驗 σ 位置 | 後驗 σ 速度 |
|---|---|---|---|---|
| 0.02 | 0.0136 | 0.0009 | 1.75 | 0.17 |
| 0.5 | 0.0302 | 0.0046 | 2.61 | 0.57 |
| 20 | 0.0743 | 0.0287 | 4.09 | 2.25 |

觀察：$q$ 越大，增益越大，濾波器越依賴量測。但後驗 σ 也越大，代表濾波器對自己的估計越沒有把握。

**表 2：改變 $R$（$q = 0.5$）**

| $R$ | $K_\text{pos}$ | $K_\text{vel}$ | 後驗 σ 位置 | 後驗 σ 速度 |
|---|---|---|---|---|
| 0.5 | 0.1319 | 0.0932 | 0.26 | 0.26 |
| 5 | 0.0764 | 0.0304 | 0.62 | 0.35 |
| 225 | 0.0302 | 0.0046 | 2.61 | 0.57 |

觀察：$R$ 越小，增益越大，後驗越準確。$R$ 大時，濾波器幾乎只靠模型，估計誤差變大。

**注意**：這些是穩態值（迭代後的收斂結果），且模型參數是本文自行選定的。實際系統應該用自己的模型與資料重算。

## 2.5 常見的失敗模式

| 症狀 | 可能原因 | 修正方向 |
|---|---|---|
| 估計太平滑，跟不上真實運動（落後） | $\mathbf Q$ 太小，過度相信模型 | 增大 $\mathbf Q$ |
| 估計跳動劇烈，跟著雜訊走 | $\mathbf Q$ 太大，或 $\mathbf R$ 太小 | 減小 $\mathbf Q$，或增大 $\mathbf R$ |
| 協方差持續變大或震盪，不收斂 | $\mathbf Q$ 太小以致模型不足以解釋實際運動；或模型結構錯誤 | 檢查模型與 $\mathbf Q$ |
| 初始值稍錯就無法鎖定 | $\mathbf P_0$ 太小（過度自信） | 增大初始 $\mathbf P$ |
| 殘差有明顯偏移（bias） | 感測器有系統性誤差，但模型沒有考慮 | 在模型中加入偏差狀態，或校正感測器 |
| 殘差與前一步相關（非白噪） | 模型結構錯誤，或 $\mathbf Q$ 缺少相關項 | 修正模型，考慮 $\mathbf Q$ 的非對角線 |

## 2.6 如何選 R

1. **靜態量測**：讓感測器靜止，錄製一段資料，計算樣本變異數。這是最直接的方法。
2. **多感測器**：$\mathbf R$ 的非對角線元素代表感測器之間的誤差相關性。若兩個感測器共用同一個干擾來源，就要估計它們的共變異數，否則會高估資訊量。
3. **注意規格書**：確認數值是最大值、1σ，還是 3σ。書中（第 05 章）提醒過，若誤用，$R$ 會相差好幾倍。
4. **注意非高斯誤差**：若感測器的誤差有偏差或厚尾，$\mathbf R$ 只能描述二階的部分，仍然需要其他處理。

## 2.7 如何選 Q

1. **從物理推估**：先找出系統狀態在一個取樣週期內可能的最大變化。例如加速度變化的上限 $\Delta a$，用書中的經驗法則把 $\mathbf Q$ 的量級設在 $\tfrac12\Delta a$ 到 $\Delta a$ 之間。
2. **用模型推導**：若假設加速度是白雜訊、強度為 $\sigma_a^2$，則
   $$\mathbf Q = \sigma_a^2\begin{bmatrix}\Delta t^4/4 & \Delta t^3/2\\ \Delta t^3/2 & \Delta t^2\end{bmatrix}$$
   這是實務上很常見的做法，本文的表 1 就是用這個形式（$q$ 即 $\sigma_a^2$）。
3. **用模擬校準**：用已知真值的模擬資料，掃描 $\mathbf Q$ 與 $\mathbf R$ 的網格，比較均方根誤差（RMSE），找出最佳組合。
4. **用真實資料驗證**：模擬調好後，在真實資料上檢查殘差與誤差比例（見 2.8）。

## 2.8 如何判斷 R 與 Q 設得好不好

- **殘差檢查**：殘差 $\mathbf y$ 應該以 0 為中心，沒有趨勢，且彼此不相關。這是書中（第 06 章批次處理一節）建議的目視檢查。
- **誤差比例**：約 68% 的誤差應落在 1σ 之內，約 99.7% 落在 3σ 之內（若誤差是高斯的）。若比例差距很大，表示 $\mathbf P$ 太大或太小。
- **協方差的收斂**：$\mathbf P$ 的對角線應該收斂。若持續變大，表示 $\mathbf Q$ 不足或模型不符。
- **靈敏度測試**（補充）：把 $\mathbf Q$、$\mathbf R$ 分別乘以 0.5 與 2，觀察結果的變化。若結果對參數極度敏感，表示模型可能有問題。
- **一致性檢查**（補充，超出本章範圍）：常用的指標是歸一化新息平方（NIS）
  $$\varepsilon_k = \mathbf y_k^\mathsf T\mathbf S_k^{-1}\mathbf y_k$$
  若模型一致，$\varepsilon_k$ 的平均值應約等於量測的維度 $\dim(\mathbf z)$。若明顯偏大，表示 $\mathbf R$ 或 $\mathbf Q$ 低估了真實誤差；明顯偏小，則表示高估了。

## 2.9 書中的範例：為什麼 R 與 Q 的效果要靠理解

作者強調：**不要魔法式地亂調 R 與 Q，直到輸出看起來順眼**。原因有兩點：

1. 過度平滑的結果看起來很漂亮，但可能是濾波器過度相信模型，誤差其實很大。
2. 同樣看起來平滑的輸出，可以由不同的 R 與 Q 組合得到，但它們對應的物理意義完全不同。

書中的例子正說明這一點：Q = 0.02 的輸出看起來很好，但 $\mathbf P$ 沒有收斂，而且對初始值很敏感。這代表它只是在「看起來正確」，實際上並不可靠。

---

# 三、總結

- **Kalman 增益**可以從兩個角度推導：Bayes 的資訊形式，或均方誤差最小化。兩者結果相同：$\mathbf K = \bar{\mathbf P}\mathbf H^\mathsf T\mathbf S^{-1}$。
- 增益的直覺是「預測的不確定性 ÷ 總不確定性」。預測越不確定，越依賴量測；量測越不確定，越依賴預測。
- **$\mathbf Q$ 與 $\mathbf R$ 決定增益的大小**，而兩者的相對比例最重要。
- 調整時應該從物理意義出發，用模擬與真實資料驗證，不要只看輸出的外觀。

---

## 附錄：本文數值的重現方法

2.4 節的數值可以用以下的純 Python 迴圈重現（不需要 NumPy）：

```python
import math

def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]

def T(A):
    return [list(r) for r in zip(*A)]

def add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def steady(dt, R, q, iters=2000):
    F = [[1, dt], [0, 1]]
    Q = [[q*dt**4/4, q*dt**3/2], [q*dt**3/2, q*dt**2]]
    P = [[500., 0.], [0., 49.]]
    for _ in range(iters):
        Pb = add(mm(mm(F, P), T(F)), Q)          # predict
        S = Pb[0][0] + R
        K = [Pb[0][0]/S, Pb[1][0]/S]              # gain
        IKH = [[1-K[0], 0], [-K[1], 1]]
        P = mm(IKH, Pb)                           # update
    return K, Pb, P

K, Pb, P = steady(0.1, 225., 0.5)
print(K, math.sqrt(P[0][0]), math.sqrt(P[1][1]))
```
