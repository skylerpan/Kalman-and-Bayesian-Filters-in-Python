# 第 07 章 卡爾曼濾波器的數學：完整講解

本文詳細講解 `07-Kalman-Filter-Math.ipynb`。前面幾章用程式與直覺建立了 Kalman filter 的做法，這一章要回答三個問題：

1. 系統方程式中的 $\mathbf F$、$\mathbf Q$ 從物理模型怎麼來？
2. Kalman 增益與後驗協方差的公式怎麼推出來？
3. Kalman filter 和 g-h filter 到底是什麼關係？

另外還有兩個支線：數值積分（用於非線性系統）與貝氏濾波的觀點。

標註「本文補充」的推導與驗算，是書中沒有完整寫出、我另外補上的部分。

---

## 0. 本章的主軸

這一章的所有數學都在做同一件事：**把連續的物理描述，轉成離散時間步的遞迴式，並算出每一步的不確定性**。

```
連續的微分方程  ──(矩陣指數 / 數值方法)──▶  F（狀態轉移）
連續的雜訊模型  ──(積分 / 分段假設)──────▶  Q（過程雜訊）
最小化誤差      ──(對 trace 取導數)────────▶  K（Kalman 增益）
```

作者也一再提醒：**數學只能給出「模型內」的答案，模型本身永遠是近似**。

---

## 1. 開場：為什麼要學這些數學

- Kalman filter 的名聲比它的難度大。底層概念很簡單：在量測與預測之間選一個輸出。
- 作者挑選的問題（例如牛頓運動方程）特別容易建模，所以 $\mathbf F$ 與 $\mathbf Q$ 相對好算。
- 作者的小玩笑：Apollo 任務用的就是這套數學。

**觀念**：前面各章是「先用程式跑起來再理解」，這一章是「把程式背後的公式推回來」。

---

## 2. 為動態系統建模

### 2.1 什麼是動態系統

動態系統是狀態（位置、溫度等）隨時間演變的物理系統。因為狀態會變，所以用**微分方程**描述。

### 2.2 這一章的範圍

- 建立系統方程式需要好幾門大學課程（常微分方程、偏微分方程、控制理論）。
- 作者的目標比較務實：讓讀者能**讀懂論文並實作演算法**。
- 這是全書最長的純數學段落，而 **EKF（擴展卡爾曼濾波器）** 需要這裡的內容。

**觀念**：濾波器的品質取決於模型，而模型是從微分方程來的。

---

## 3. 狀態空間表示法（State-Space）

### 3.1 從連續到離散

從連續模型出發：

$$\dot{\mathbf x} = \mathbf{Ax} + \mathbf{Bu} + \mathbf w$$

濾波器需要的是**遞迴形式**，也就是由 $\mathbf x_{k-1}$ 算出 $\mathbf x_k$：

$$\mathbf x_k = \mathbf F\,\mathbf x_{k-1} + \mathbf B_k\mathbf u_k$$

- $\mathbf F$ 是 **state transition matrix（狀態轉移矩陣）**，描述一個時間步內狀態如何向前推進。
- $\mathbf A$ 是**系統動態矩陣**，描述連續時間中狀態的變化率。
- 兩者相近，但不是同一個東西。$\mathbf F$ 由 $\mathbf A$ 經過指數運算得到（見第 4 節）。

**觀念**：要把「變化率」的描述，轉成「一個時間步之後的值」的描述。

### 3.2 高階方程式化成一階

許多物理系統是二階或更高階的。例如：

$$\ddot x - 6\dot x + 9x = u$$

做法是為每一階導數定義新變數：

$$x_1 = x,\qquad x_2 = \dot x$$

則 $\dot x_1 = x_2$，而 $\dot x_2 = \ddot x = 6x_2 - 9x_1 + u$。寫成矩陣：

$$\begin{bmatrix}\dot x_1\\ \dot x_2\end{bmatrix} = \begin{bmatrix}0&1\\-9&6\end{bmatrix}\begin{bmatrix}x_1\\x_2\end{bmatrix} + \begin{bmatrix}0\\1\end{bmatrix}u$$

這種形式稱為 **companion form（伴隨形式）**。一般的 $n$ 階方程式可以寫成：最後一列放係數 $-a_0/a_n,\ \dots,\ -a_{n-1}/a_n$，上方是單位移位。

**觀念**：一階形式是統一的語言，任何高階系統都能化成它。

### 3.3 例子：質量－彈簧－阻尼器

$$m\ddot x + c\dot x + kx = u$$

取 $x_1 = x$、$x_2 = \dot x$，解出 $\dot x_2$：

$$\dot x_2 = -\frac{c}{m}x_2 - \frac{k}{m}x_1 + \frac{1}{m}u$$

所以

$$\begin{bmatrix}\dot x_1\\ \dot x_2\end{bmatrix} = \begin{bmatrix}0&1\\-\frac{k}{m}&-\frac{c}{m}\end{bmatrix}\begin{bmatrix}x_1\\x_2\end{bmatrix} + \begin{bmatrix}0\\ \frac1m\end{bmatrix}u$$

汽車懸吊、感測器的機械結構，都能用這種方式建模。

---

## 4. 求 $\mathbf F$：從 $\mathbf A$ 到轉移矩陣

目標是找到 $\mathbf F$，使得 $\mathbf x(t_k) = \mathbf F(\Delta t)\,\mathbf x(t_{k-1})$。書中提出三種做法。

### 4.1 矩陣指數（最常用）

**先看純量的情況。** 解 $\dfrac{dx}{dt} = kx$：

$$\frac{dx}{x} = k\,dt \;\Rightarrow\; \ln x = kt + c \;\Rightarrow\; x = c_0e^{kt}$$

代入初值 $x(0)=x_0$，得 $c_0 = x_0$，所以 $x(t) = x_0e^{kt}$。

**推廣到矩陣。** 對 $\dot{\mathbf x} = \mathbf{Ax}$，$\mathbf x(0)=\mathbf x_0$，解為

$$\mathbf x(t) = e^{\mathbf At}\mathbf x_0$$

因此轉移矩陣為

$$\boxed{\mathbf F = e^{\mathbf A\Delta t}}$$

矩陣指數定義為 $e^{\mathbf M} = \mathbf I + \mathbf M + \dfrac{\mathbf M^2}{2!} + \dfrac{\mathbf M^3}{3!}+\cdots$。

**例子驗證（本文補充）**：對 $\mathbf A = \begin{bmatrix}0&1\\0&0\end{bmatrix}$（等速運動），$\mathbf A^2 = \mathbf 0$，所以級數在第二項截斷：

$$\mathbf F = \mathbf I + \mathbf A\Delta t = \begin{bmatrix}1&\Delta t\\0&1\end{bmatrix}$$

這正是第 04、06 章使用的等速模型。**觀念**：等速模型的 $\mathbf F$ 只是矩陣指數的前兩項。

### 4.2 時間不變性（Time Invariance）

- **非時變系統**：系統行為不隨時間改變。同樣的輸入，在任何時間都得到相同的輸出（只是時間平移）。
- 反例：$f(x) = t\,x$，係數 $t$ 隨時間改變，所以是**時變**的。
- 飛機也是時變的：燃油燒掉、重量減輕，同樣的控制輸入會得到不同結果。
- 只有非時變的線性系統，$\mathbf F = e^{\mathbf A\Delta t}$ 才能直接用，因為 $\mathbf A$ 不隨時間變。

**觀念**：Kalman filter 的標準形式假設線性非時變。遇到時變系統，就要重新計算或使用其他方法。

### 4.3 LTI 理論（拉普拉斯轉換）

可以用
$$\Phi(t) = \mathcal L^{-1}\big[(s\mathbf I - \mathbf A)^{-1}\big]$$
求轉移矩陣。本書不用拉普拉斯轉換，但有些文獻會這樣設計 Kalman 矩陣，所以作者提一下。

### 4.4 數值方法：van Loan

- 系統變大時，解析解會很繁瑣（SymPy 可以幫忙）。
- van Loan 的方法可以**同時數值求出 $\mathbf F$ 與 $\mathbf Q$**。給定連續模型 $\dot{\mathbf x} = \mathbf{Ax} + \mathbf{Gw}$，其中 $w$ 是單位白雜訊。
- FilterPy 提供 `van_loan_discretization(A, G, dt)`。

**觀念**：實務上常用數值方法，而不是手算解析解。

---

## 5. 過程雜訊矩陣 $\mathbf Q$ 的設計

### 5.1 為什麼最困難

- $\mathbf Q$ 的推導需要訊號理論基礎。
- 我們是在為「不太了解的東西的雜訊」建模。作者用**投出的棒球**做例子：旋轉、轉速衰減、縫線的阻力、風與空氣密度，都是模型之外的因素。
- 因為模型本身不完整，$\mathbf Q$ 的結果也不完整：
  - $\mathbf Q$ 太小：濾波器對自己的模型過度自信，會偏離真實解。
  - $\mathbf Q$ 太大：濾波器過度受量測雜訊影響，表現不佳。

**觀念**：$\mathbf Q$ 的數學推導只是起點，最後仍要靠模擬與資料校準。

### 5.2 假設：加速度是白雜訊

後面兩個模型都假設運動學系統（用牛頓方程描述），並且讓**最高階的導數受雜訊影響**：

- 我們的模型可以是「位置＋速度」，也可以是「位置＋速度＋加速度」。
- 理論上可以加到 jerk、jounce 等，但加入超出真實動態的項，通常會讓估計變差。
- 假設加速度不是常數，而是受未建模外力干擾的白雜訊。

### 5.3 連續白雜訊模型

**定義**：連續時間的過程雜訊 $w(t)$，平均為零，且不同時間互不相關。離散化的 $\mathbf Q$ 為

$$\mathbf Q = \int_0^{\Delta t}\mathbf F(\tau)\,\mathbf Q_c\,\mathbf F^\mathsf T(\tau)\,d\tau$$

其中 $\mathbf Q_c$ 是連續雜訊的強度。

**直覺**：$\mathbf F(\tau)\mathbf Q_c\mathbf F^\mathsf T(\tau)$ 表示在時刻 $\tau$ 的雜訊，如何投影到狀態上；把它沿整個時間步積分，就得到這段時間的累積效果。

**推導例子（本文補充）**：狀態為 $[x,\,\dot x]^\mathsf T$，雜訊加在速度的導數上（即 $\dot v = w$）。此時 $\mathbf F(\tau) = \begin{bmatrix}1&\tau\\0&1\end{bmatrix}$，雜訊輸入向量 $\mathbf G = [0,\,1]^\mathsf T$，因此 $\mathbf F(\tau)\mathbf G = [\tau,\,1]^\mathsf T$。於是

$$\mathbf Q = q\int_0^{\Delta t}\begin{bmatrix}\tau^2 & \tau\\ \tau & 1\end{bmatrix}d\tau = q\begin{bmatrix}\dfrac{\Delta t^3}{3} & \dfrac{\Delta t^2}{2}\\[2mm] \dfrac{\Delta t^2}{2} & \Delta t\end{bmatrix}$$

（已用數值積分驗證，見第 12 節。）

**觀念**：連續雜訊必須在時間區間上積分，才能變成離散的 $\mathbf Q$。

### 5.4 分段白雜訊模型（Piecewise White Noise）

**假設**：加速度在每個時間步內是常數，但不同時間步的值互相獨立。也就是說，加速度在每一步都有「跳動」。

**一階系統**（位置＋速度，雜訊為加速度）：

$$\mathbf F = \begin{bmatrix}1&\Delta t\\0&1\end{bmatrix},\qquad \boldsymbol\Gamma = \begin{bmatrix}\tfrac12\Delta t^2\\ \Delta t\end{bmatrix}$$

$\boldsymbol\Gamma$ 的來源：在一個時間步內，加速度 $w$ 讓速度改變 $w\Delta t$，讓位置改變 $\tfrac12 w\Delta t^2$。

$$\mathbf Q = \boldsymbol\Gamma\,\sigma^2\,\boldsymbol\Gamma^\mathsf T = \sigma^2\begin{bmatrix}\dfrac{\Delta t^4}{4} & \dfrac{\Delta t^3}{2}\\[2mm] \dfrac{\Delta t^3}{2} & \Delta t^2\end{bmatrix}$$

**二階系統**（位置＋速度＋加速度，雜訊為 jerk，即加速度的離散白雜訊，稱為離散 Wiener process）：

$$\mathbf F = \begin{bmatrix}1&\Delta t&\tfrac12\Delta t^2\\0&1&\Delta t\\0&0&1\end{bmatrix},\qquad \boldsymbol\Gamma = \begin{bmatrix}\tfrac12\Delta t^2\\ \Delta t\\ 1\end{bmatrix}$$

$$\mathbf Q = \boldsymbol\Gamma\,\sigma^2\,\boldsymbol\Gamma^\mathsf T$$

### 5.5 兩種模型的比較

| 面向 | 連續白雜訊 | 分段白雜訊 |
|---|---|---|
| 雜訊的假設 | 連續時間的白雜訊 | 每段常數，段間獨立 |
| 參數 | 需要指定 spectral density $q$（較不直覺） | 直接用 $\sigma^2$（較直覺） |
| 不固定的取樣時間 | 處理較容易（積分自然對應） | 較麻煩 |
| 正確性 | 兩者都是近似，沒有哪個「更正確」 | 同左 |

作者強調：**只有經驗與實驗能告訴你哪個模型適合**。實務上兩者常常都能給出合理結果，但通常其中一個表現更好。

### 5.6 經驗法則

設 $\sigma$ 在 $\tfrac12\Delta a$ 到 $\Delta a$ 之間，其中 $\Delta a$ 是相鄰取樣區間內加速度的最大變化量。實務上挑一個數字，用資料跑模擬，然後選效果好的值。

### 5.7 FilterPy 工具

- `Q_continuous_white_noise(dim, dt, spectral_density)`：連續模型。
- `Q_discrete_white_noise(dim, dt, var)`：分段模型。

### 5.8 Q 的簡化

許多文獻只在 $\mathbf Q$ 的右下角放一個 $\sigma^2$，其餘為零：

$$\mathbf Q = \begin{bmatrix}0&0&0\\0&0&0\\0&0&\sigma^2\end{bmatrix}$$

**理由**：當 $\Delta t$ 很小時，$\mathbf Q$ 的大部分元素很小，對 $\mathbf P = \mathbf{FPF}^\mathsf T + \mathbf Q$ 的貢獻有限。

**注意**：
- 這是不正確的近似，用在重要應用前必須大量驗證。
- 「右下角」指的是變化最快的那個狀態。若狀態是 $[x,\dot x,\ddot x,y,\dot y,\ddot y]^\mathsf T$，則 $\ddot x$ 與 $\ddot y$ 對應的元素都必須非零。

**觀念**：簡化是常見做法，但要知道它忽略了什麼。

---

## 6. 穩定地計算後驗協方差

### 6.1 兩種公式

理論上正確的公式是

$$\mathbf P = (\mathbf I - \mathbf{KH})\bar{\mathbf P}$$

FilterPy 實際使用的是 **Joseph 形式**：

$$\mathbf P = (\mathbf I-\mathbf{KH})\bar{\mathbf P}(\mathbf I-\mathbf{KH})^\mathsf T + \mathbf{KRK}^\mathsf T$$

兩者在數學上相等（當 $\mathbf K$ 是最佳增益時），但數值行為不同。

### 6.2 為什麼 Joseph 形式較穩定

- 減法 $(\mathbf I - \mathbf{KH})$ 會因浮點數誤差，讓結果變得不對稱。
- 協方差必須是對稱的。一旦不對稱，常導致濾波器發散，甚至觸發 NumPy 的檢查而拋出例外。
- Joseph 形式的兩項都是 $\mathbf M\mathbf N\mathbf M^\mathsf T$ 的形式，**結構上保證對稱、半正定**。

作者說明：有人寄信或開 issue 說這是 bug，但它是刻意的設計。

### 6.3 另一個保持對稱的做法

$$\mathbf P \leftarrow \tfrac12(\mathbf P + \mathbf P^\mathsf T)$$

這樣做是安全的，因為它只是把誤差平均掉，不改變數學意義。

**觀念**：數學上等價的公式，數值上不一定等價。

---

## 7. 推導 Kalman 增益

### 7.1 重要的說明

- 這個推導**沒有用貝氏公式**。作者說他看過至少四種推導方法，這是文獻中常見的一種，來源是 Brown & Hwang。
- 承接第 6 節的 Joseph 形式，推導的目標是找出讓後驗協方差「最小」的 $\mathbf K$。

### 7.2 設定

估計的更新式為

$$\hat{\mathbf x} = \bar{\mathbf x} + \mathbf K(\mathbf z - \mathbf H\bar{\mathbf x})$$

真實量測為 $\mathbf z = \mathbf H\mathbf x + \mathbf v$，其中 $\mathbf v$ 是零均值、協方差為 $\mathbf R$ 的雜訊，且與 $\mathbf x$、$\bar{\mathbf x}$ 獨立。

### 7.3 把估計誤差寫成 $\mathbf K$ 的函數

定義誤差 $\mathbf e = \mathbf x - \hat{\mathbf x}$。逐步代入：

$$\begin{aligned}
\mathbf e &= \mathbf x - \big(\bar{\mathbf x} + \mathbf K(\mathbf H\mathbf x + \mathbf v - \mathbf H\bar{\mathbf x})\big)\\
&= (\mathbf x - \bar{\mathbf x}) - \mathbf K\mathbf H(\mathbf x - \bar{\mathbf x}) - \mathbf K\mathbf v\\
&= (\mathbf I - \mathbf{KH})(\mathbf x - \bar{\mathbf x}) - \mathbf K\mathbf v
\end{aligned}$$

### 7.4 計算誤差的協方差

$\mathbf x - \bar{\mathbf x}$ 的協方差是 $\bar{\mathbf P}$，$\mathbf v$ 的協方差是 $\mathbf R$，兩者獨立且零均值，所以交叉項為零：

$$\mathbf P(\mathbf K) = \mathbb E[\mathbf e\mathbf e^\mathsf T] = (\mathbf I-\mathbf{KH})\bar{\mathbf P}(\mathbf I-\mathbf{KH})^\mathsf T + \mathbf K\mathbf R\mathbf K^\mathsf T$$

這正是第 6 節的 Joseph 形式。**它對任意的 $\mathbf K$ 都成立**，所以可以用來比較不同增益的好壞。

### 7.5 展開

令 $\mathbf S = \mathbf H\bar{\mathbf P}\mathbf H^\mathsf T + \mathbf R$，展開可得

$$\mathbf P(\mathbf K) = \bar{\mathbf P} - \mathbf K\mathbf H\bar{\mathbf P} - \bar{\mathbf P}\mathbf H^\mathsf T\mathbf K^\mathsf T + \mathbf K\mathbf S\mathbf K^\mathsf T$$

（驗算：$\mathbf K\mathbf H\bar{\mathbf P}\mathbf H^\mathsf T\mathbf K^\mathsf T + \mathbf K\mathbf R\mathbf K^\mathsf T = \mathbf K\mathbf S\mathbf K^\mathsf T$。）

### 7.6 最小化：對 trace 取導數

誤差的大小用協方差的對角線衡量（每個狀態的變異數），所以目標是最小化 $\operatorname{tr}\mathbf P(\mathbf K)$。

$$\operatorname{tr}\mathbf P(\mathbf K) = \operatorname{tr}\bar{\mathbf P} - 2\operatorname{tr}(\mathbf K\mathbf H\bar{\mathbf P}) + \operatorname{tr}(\mathbf K\mathbf S\mathbf K^\mathsf T)$$

（用到 $\operatorname{tr}\mathbf A = \operatorname{tr}\mathbf A^\mathsf T$，把兩個交叉項合併。）

要用的導數公式（Brown 提供）：

$$\frac{\partial\operatorname{tr}(\mathbf{AB})}{\partial\mathbf A} = \mathbf B^\mathsf T,\qquad \frac{\partial\operatorname{tr}(\mathbf{ACA}^\mathsf T)}{\partial\mathbf A} = 2\mathbf{AC}\quad(\mathbf C\text{ 對稱})$$

套用：
- 第二項：$\dfrac{\partial}{\partial\mathbf K}\operatorname{tr}(\mathbf K\mathbf H\bar{\mathbf P}) = (\mathbf H\bar{\mathbf P})^\mathsf T = \bar{\mathbf P}\mathbf H^\mathsf T$
- 第三項：$\dfrac{\partial}{\partial\mathbf K}\operatorname{tr}(\mathbf K\mathbf S\mathbf K^\mathsf T) = 2\mathbf K\mathbf S$（$\mathbf S$ 對稱）

所以

$$\frac{\partial\operatorname{tr}\mathbf P}{\partial\mathbf K} = -2\bar{\mathbf P}\mathbf H^\mathsf T + 2\mathbf K\mathbf S$$

令其為零：

$$\boxed{\mathbf K = \bar{\mathbf P}\mathbf H^\mathsf T\mathbf S^{-1}}$$

這就是第 06 章的 Kalman 增益。

### 7.7 代回去得到後驗協方差

$$\mathbf P = \bar{\mathbf P} - \bar{\mathbf P}\mathbf H^\mathsf T\mathbf S^{-1}\mathbf H\bar{\mathbf P} = (\mathbf I-\mathbf{KH})\bar{\mathbf P}$$

### 7.8 因為 $\mathbf S$ 是對稱正定的，極值是最小值

由 7.5 的形式，$\mathbf P(\mathbf K)$ 的二次項是 $\mathbf K\mathbf S\mathbf K^\mathsf T$，而 $\mathbf S$ 正定，所以這是一個凸函數，唯一的駐點就是最小值。

**觀念**：Kalman 增益是「讓估計的平均誤差平方最小」的線性估計量。這就是為什麼它被稱為最佳（optimal）濾波器（在線性高斯假設下）。

---

## 8. 微分方程的數值積分

### 8.1 為什麼需要

- 前面的方法（矩陣指數、LTI、van Loan）只適用於**線性**常微分方程。
- 例子：急轉彎的汽車。前輪轉動使車子繞後軸旋轉，路徑不斷變化，線性外推必然出錯。
- 若系統在 $\Delta t$ 內變化不大，線性近似通常還夠用；但非線性濾波器（例如 EKF）的情況常常不是這樣。

### 8.2 Euler 方法

**問題**：$y' = y$，$y(0) = 1$。精確解是 $y = e^t$，但實務上通常不知道精確解。

**做法**：用起點的斜率外推一步：
$$y_{n+1} = y_n + h\,f(t_n, y_n)$$

**例子（書中的數字）**：
- 步長 $h=1$：$y(1) \approx 1 + 1\cdot 1 = 2$；再用 $t=1$ 的斜率 $2$，得 $y(2) \approx 2 + 2 = 4$。精確值 $e^2 \approx 7.39$，誤差很大。
- 步長變小，結果更準，但需要非常多次迭代才能達到三位有效數字。

**推導**：Taylor 展開

$$y(t_0+h) = y(t_0) + hy'(t_0) + \tfrac{1}{2}h^2y''(t_0) + \cdots$$

Euler 方法只取前兩項。作者指出 Euler 方法就是最簡單形式的 Runge-Kutta。

**觀念**：數值方法的核心是用局部斜率來近似曲線。

### 8.3 Runge-Kutta（RK4）

RK4 在速度、精確度與穩定性之間取得良好平衡。作者的建議是：除非有特別理由，否則它是數值積分的首選。

對 $\dot y = f(y,t)$，一步的更新為

$$y(t+\Delta t) = y(t) + \tfrac16(k_1 + 2k_2 + 2k_3 + k_4)$$

其中

$$\begin{aligned}
k_1 &= f(y,\,t)\,\Delta t\\
k_2 &= f\big(y + \tfrac12k_1,\ t + \tfrac12\Delta t\big)\,\Delta t\\
k_3 &= f\big(y + \tfrac12k_2,\ t + \tfrac12\Delta t\big)\,\Delta t\\
k_4 &= f\big(y + k_3,\ t + \Delta t\big)\,\Delta t
\end{aligned}$$

直觀理解：$k_1$ 是起點斜率，$k_2$、$k_3$ 是中點的斜率估計（用不同的中間值），$k_4$ 是終點斜率；最後用 $1:2:2:1$ 加權平均。

書中的例子是 $\dot y = t\sqrt{y}$，$y(0)=1$。

**觀念**：用多個斜率的加權平均，來提高精確度。

---

## 9. 貝氏濾波（Bayesian Filtering）

### 9.1 狀態與量測

- 狀態 $\mathbf x_t$ 是物體在時間 $t$ 的位置、速度等，例如 $\mathbf x_t = [x_t,\ \dot x_t]^\mathsf T$。
- 量測是狀態的函數，而且帶有雜訊。狀態改變會改變量測，但量測的改變不會改變狀態。

### 9.2 統計反演（Statistical Inversion）

- **正向問題**：已知狀態序列 $\mathbf x_{0:t}$，算出量測 $\mathbf z_{0:t}$，很簡單。
- **反向問題**：濾波要做的是，已知量測 $\mathbf z_{0:t}$，反推狀態 $\mathbf x_{0:t}$。
- 反演通常沒有唯一解：不同的狀態序列，可能產生相似的量測。

因此濾波是一個**不適定的反問題（ill-posed inverse problem）**，需要機率框架來處理不確定性。

**觀念**：貝氏濾波把「從量測推斷狀態」當作條件機率問題來處理，Kalman filter 是這個框架在線性高斯情況下的閉式解。

---

## 10. 把 Kalman filter 轉換成 g-h filter

### 10.1 出發點

一維高斯相乘的均值公式：

$$\mu_x = \frac{\sigma_1^2\,\mu_2 + \sigma_2^2\,\mu_1}{\sigma_1^2 + \sigma_2^2}$$

在 Kalman 的情境中，$\mu_1$ 是先驗（預測）、$\mu_2$ 是量測。因為量測的權重應該是先驗變異數的比例，所以應把先驗的變異數放在量測的係數上。設先驗變異數為 $P$，量測變異數為 $R$，則

$$\mu = \frac{R\,\bar x + P\,z}{P+R}$$

### 10.2 代數化簡成 g-h 形式

記 $g = \dfrac{P}{P+R}$：

$$\begin{aligned}
\mu &= \frac{R\bar x + Pz}{P+R}\\
&= \bar x + \frac{R\bar x + Pz - (P+R)\bar x}{P+R}\\
&= \bar x + \frac{P(z - \bar x)}{P+R}\\
&= \bar x + g\,(z - \bar x)
\end{aligned}$$

所以 Kalman 的均值更新就是 g-h filter 的形式：**新估計 = 預測 + g × 殘差**。

### 10.3 變異數也能化成同一形式

$$\sigma^2 = \frac{PR}{P+R} = \Big(1-\frac{P}{P+R}\Big)P = (1-g)\,P$$

### 10.4 結論

- **Kalman filter 就是 g-h filter，只是 g 不是固定的常數，而是由 $P$ 與 $R$ 算出來的**。
- 第 06 章提到的 $h$（速度修正）也是同一邏輯：在多維情況下，$\mathbf K$ 的每個分量扮演一個 g 或 h 的角色。

**觀念**：g-h filter 和 Kalman filter 的差別，只在 g 與 h 的來源（固定 vs 由不確定性計算）。

---

## 11. 參考文獻

- **[1]** Moler & Van Loan, "Nineteen Dubious Ways to Compute the Exponential of a Matrix, Twenty-Five Years Later", *SIAM Review*, 2003。矩陣指數的各種計算方法與比較。
- **[2]** van Loan, "Computing Integrals Involving the Matrix Exponential", *IEEE Transactions on Automatic Control*, 1978。同時求 $\mathbf F$ 與 $\mathbf Q$ 的方法。
- **[3]** Calvetti & Somersalo, *Introduction to Bayesian Scientific Computing*, Springer, 2007。貝氏科學計算。
- **[4]** Brown & Hwang, *Introduction to Random Signals and Applied Kalman Filtering*, 4th ed., Wiley, 2012。本章 Kalman 增益推導的主要來源。

---

## 12. 附錄：本文的數值驗證

以下是我對本文公式的數值檢查（用純 Python 的數值積分與代數比對）：

1. **連續白雜訊的 $\mathbf Q$**：取 $\Delta t = 0.1$、$q = 1$，用中點法數值積分 $\int_0^{\Delta t}\begin{bmatrix}\tau^2&\tau\\\tau&1\end{bmatrix}d\tau$：

   $$\begin{bmatrix}3.3333\times10^{-4} & 5.0\times10^{-3}\\ 5.0\times10^{-3} & 0.1\end{bmatrix}$$

   與解析式 $q\begin{bmatrix}\Delta t^3/3 & \Delta t^2/2\\ \Delta t^2/2 & \Delta t\end{bmatrix}$ 完全相同。

2. **分段白雜訊的 $\mathbf Q$**：同樣參數下，$\boldsymbol\Gamma\boldsymbol\Gamma^\mathsf T = \begin{bmatrix}2.5\times10^{-5}&5\times10^{-4}\\5\times10^{-4}&10^{-2}\end{bmatrix}$。注意它的量級比連續模型小，因為兩者的雜訊定義不同（$\sigma^2$ 與 $q$ 不是同一個量）。

3. **g-h 的等價性**：隨機取 $P, R, \bar x, z$，檢查 $\mu = \bar x + g(z-\bar x)$ 與 $\sigma^2 = (1-g)P$ 與高斯相乘的結果一致，誤差為 $0$。

---

## 13. 總結

本章的數學可以分成四條主線：

| 主線 | 問題 | 工具 | 結果 |
|---|---|---|---|
| 狀態轉移 | 連續動態如何變成離散 | 矩陣指數、van Loan | $\mathbf F = e^{\mathbf A\Delta t}$ |
| 過程雜訊 | 雜訊在一步內的累積 | 積分、分段模型 | $\mathbf Q = \int \mathbf F\mathbf Q_c\mathbf F^\mathsf T$ 或 $\boldsymbol\Gamma\sigma^2\boldsymbol\Gamma^\mathsf T$ |
| 最佳增益 | 怎樣的 $\mathbf K$ 使誤差最小 | Joseph 形式、trace 導數 | $\mathbf K = \bar{\mathbf P}\mathbf H^\mathsf T\mathbf S^{-1}$ |
| 非線性 | 非線性系統怎麼積分 | Euler、RK4 | 為 EKF 等後續章節鋪路 |

此外，Kalman filter 可以化成 g-h filter 的形式，而貝氏觀點說明了濾波本質上是在解一個反問題。

**一句話總結**：這一章把前面「看起來像魔法」的方程式逐一推回來——$\mathbf F$ 來自矩陣指數，$\mathbf Q$ 來自對連續雜訊的積分，$\mathbf K$ 來自最小化誤差，而 Joseph 形式則保證數值穩定。
