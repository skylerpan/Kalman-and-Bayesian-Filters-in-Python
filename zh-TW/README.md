# [Kalman and Bayesian Filters in Python](https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python) 台灣繁體中文翻譯版

## 關於本翻譯版

本資料夾（`zh-TW/`）是 Roger R. Labbe 所著《Kalman and Bayesian Filters in Python》（原書：https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python ）的台灣繁體中文翻譯版。

**授權**：原書的文字採 CC BY 4.0（Creative Commons Attribution 4.0 International）授權，程式碼採 MIT 授權。本翻譯版沿用相同的授權條款：翻譯後的文字同樣以 CC BY 4.0 釋出，程式碼同樣以 MIT 釋出，並在此標註出處為 Roger R. Labbe 的原書。完整的授權條文請見本文件下方的「License（授權）」一節。

**翻譯原則**：

* 技術術語以英文為主。每一章（每一本 notebook）中術語**第一次**出現時，在旁邊以全形括號補上中文，例如 `Kalman filter（卡爾曼濾波器）`、`covariance（共變異數）`；同一章之後再出現時只寫英文。完整的英中術語對照請見 [GLOSSARY.md](./GLOSSARY.md)。
* 所有 code cell 與原書**完全相同**，沒有任何修改，可以直接執行。只有 markdown cell 的文字被翻譯。
* 數學式（LaTeX）、URL、圖片路徑、變數名、函式名、套件名、人名與書名一律保留原文。
* 書名《Kalman and Bayesian Filters in Python》與作者名 Roger R. Labbe 保留英文。

## 如何執行

本翻譯版可以直接用系統的 Python 執行，不需要 docker，也不需要 venv 或 conda 環境：

```
pip3 install --user -r requirements.txt
cd zh-TW
jupyter notebook        # 或 jupyter lab
```

需求：

* Python 3.6 以上。
* 套件：filterpy、numpy、scipy、matplotlib、sympy、jupyter（都列在 `requirements.txt` 裡；本資料夾內也有一份相同的 `requirements.txt`）。

注意事項：

* notebook **必須在 `zh-TW/` 目錄內開啟**（也就是要先 `cd zh-TW` 再啟動 Jupyter），因為每一章開頭都會以相對路徑載入 `book_format.py` 與 `kf_book/` 裡的輔助程式；在其他目錄開啟會找不到這些檔案。
* `Supporting_Notebooks/` 與 `animations/` 內的 notebook 會用 `sys.path` 往上一層找 `kf_book/`，所以一樣可以直接開啟執行。

以下是原書 README 的完整繁體中文翻譯。

---

# [Kalman and Bayesian Filters in Python](https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python)


這是一本 Kalman filter（卡爾曼濾波器）與 Bayesian filter（貝氏濾波器）的入門書。所有程式碼都以 Python 撰寫，而這本書本身是用 Jupyter Notebook 寫成的，所以你可以直接在瀏覽器裡執行、修改程式碼。還有比這更好的學習方式嗎？


**「Kalman and Bayesian Filters in Python」看起來棒極了！……你的書正是我需要的** - Allen Downey，教授暨 O'Reilly 作者。

**感謝你出版這本 Kalman filtering 的入門書，以及 Python 的 Kalman filtering 函式庫，付出了這麼多心力。我們一直在內部用它來教大家一些關鍵的 state estimation（狀態估計）概念，幫助非常大。** - Sam Rodkey，SpaceX

點選下方的 binder 或 Azure 徽章，現在就開始線上閱讀（英文原版）：


[![Binder](http://mybinder.org/badge.svg)](https://beta.mybinder.org/v2/gh/rlabbe/Kalman-and-Bayesian-Filters-in-Python/master)


![alt tag](https://raw.githubusercontent.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python/master/animations/05_dog_track.gif)

什麼是 Kalman Filter 與 Bayesian Filter？
-----

sensor（感測器）是有雜訊的。世界上充滿了我們想要量測與追蹤的資料和事件，但我們無法指望感測器給我們完美的資訊。我車上的 GPS 會回報高度。每次我經過路上的同一個點，它回報的高度都略有不同。我廚房的磅秤，同一個東西秤兩次會給我不同的讀數。

在簡單的情況下，解法很明顯。如果磅秤的讀數略有差異，我可以多秤幾次然後取平均。或者我可以換一台更精準的磅秤。但如果感測器的雜訊非常大，或者環境讓資料蒐集變得困難，我們該怎麼辦？我們可能想追蹤一架低空飛行的飛機的動向。我們可能想為無人機做一套自動駕駛，或是確保農場的曳引機把整片田都播了種。我從事 computer vision（電腦視覺）的工作，需要追蹤影像中的移動物體，而電腦視覺演算法產生的結果雜訊很大、很不可靠。

這本書教你如何解決這類 filtering（濾波）問題。我用了許多不同的演算法，但它們全都建立在 Bayesian probability（貝氏機率）之上。簡單來說，貝氏機率是根據過去的資訊來判斷什麼比較可能為真。

如果我現在問你我的車的車頭朝向，你完全不會知道。你會隨便挑一個 1° 到 360° 之間的數字，答對的機會是 360 分之 1。現在假設我告訴你，2 秒前它的朝向是 243°。在 2 秒內我的車轉不了多少，所以你可以做出準確得多的 prediction（預測）。你正在利用過去的資訊，更準確地推斷現在或未來的資訊。

世界本身也是有雜訊的。那個預測能幫你做出更好的 estimate（估計值），但它同樣受雜訊影響。我可能剛為了閃一隻狗而煞車，或是為了避開坑洞而偏了一下。強風和路面結冰都是影響我車子路徑的外部因素。在控制領域的文獻裡，我們把這稱為 noise（雜訊），雖然你可能不會這樣想。

貝氏機率還有更多內容，但你已經掌握主要的概念了。知識是不確定的，而我們會根據 evidence（證據）的強度來修正自己的 belief（信念）。Kalman filter 與 Bayesian filter 把我們對系統行為那些有雜訊、有限的知識，和有雜訊、有限的感測器讀數融合起來，產生對系統 state（狀態）的最佳估計。我們的原則是：絕不丟棄資訊。

假設我們在追蹤一個物體，而感測器回報它突然改變了方向。它真的轉向了，還是資料有雜訊？視情況而定。如果這是一架噴射戰鬥機，我們會很傾向相信這個突然機動的回報。如果它是一列行駛在筆直軌道上的貨運火車，我們就會不予採信。我們還會根據感測器有多準確，進一步修正我們的信念。我們的信念取決於過去、取決於我們對所追蹤系統的了解，也取決於感測器的特性。

Kalman filter 是由 Rudolf Emil Kálmán 發明的，用來以數學上最佳的方式解決這類問題。它的第一次應用是在阿波羅登月任務，從那之後，它被應用在極為廣泛的領域裡。飛機上、潛艇上、巡弋飛彈上都有 Kalman filter。華爾街用它們來追蹤市場。它們被用在機器人、IoT（物聯網）感測器和實驗室儀器裡。化工廠用它們來控制與監測反應。它們被用來做醫學影像，以及去除心臟訊號裡的雜訊。只要牽涉到感測器和／或時間序列資料，通常就會有 Kalman filter 或它的近親在其中。

動機
-----

寫這本書的動機，來自我自己想要一本溫和的 Kalman filtering 入門書。我是一名軟體工程師，在航空電子領域待了將近二十年，所以我一直和 Kalman filter「擦肩而過」，卻從來沒有親手實作過一個。當我轉向用電腦視覺解決 tracking（追蹤）問題時，這個需求變得很迫切。這個領域有一些經典教科書，例如 Grewal 與 Andrews 優秀的 *Kalman Filtering*。但如果你沒有必要的背景知識，坐下來試著讀這些書會是很慘的經驗。通常頭幾章就飛快地掃過好幾年的大學部數學，若無其事地叫你去翻 Itō calculus（伊藤微積分）之類主題的教科書，然後用短短幾段文字塞進整整一學期份量的統計學。它們對高年級大學部課程來說是好教材，對研究人員和專業人員來說也是無價的參考書，但對比較隨性的讀者而言，讀起來真的很吃力。符號被引入時沒有解釋，不同的書用不同的名詞和變數來指同一個概念，而且這些書幾乎沒有範例或解題過程。我常常發現自己讀得懂字句、看得懂一個定義的數學，卻完全不知道它們描述的是什麼真實世界的現象。「可是這到底*是什麼意思？*」是我反覆冒出來的念頭。

然而，當我終於開始理解 Kalman filter 之後，我發現它背後的概念其實相當直截了當。幾條簡單的機率規則、一點關於我們在日常生活中如何整合各種不同的知識來解釋事件的 intuition（直覺），Kalman filter 的核心概念就變得平易近人了。Kalman filter 向來以難懂聞名，但一旦剝去大量正式術語，這門學問和它背後數學的美就在我眼前清楚地展現出來，我愛上了這個主題。

隨著我開始理解數學和理論，更多困難浮現出來。書或論文的作者陳述某個事實，然後附上一張圖當作證明。不幸的是，我不清楚那個陳述為什麼成立，也看不出那張圖是怎麼畫出來的。或者我會想：「如果 R=0，這還成立嗎？」又或者作者給的 pseudocode（虛擬碼）層次太高，實作方式並不明顯。有些書附了 Matlab 程式碼，但我沒有那個昂貴套件的授權。最後，許多書在每章末尾都附上大量有用的練習題。這些練習題是你想親手實作 Kalman filter 就必須弄懂的，卻沒有附答案。如果你是在課堂上用這本書，也許這樣沒關係，但對自學的讀者來說實在糟透了。我很厭惡作者對我隱瞞資訊，大概是為了防止課堂上的學生「作弊」。

從我的角度來看，這些都沒有必要。當然，如果你是在為飛機或飛彈設計 Kalman filter，你必須徹底精通典型 Kalman filter 教科書裡的所有數學與主題。但我只是想在螢幕上追蹤一張影像，或是為 Arduino 專案寫點程式。我想知道書裡的圖是怎麼畫的，並且選用和作者不一樣的參數。我想跑 simulation（模擬）。我想在訊號裡注入更多雜訊，看看濾波器表現如何。日常程式碼裡有成千上萬個可以使用 Kalman filter 的機會，然而這個其實相當直截了當的主題卻一直是火箭科學家和學者的專屬領域。

我寫這本書就是為了滿足這些需求。如果你是在為 Boeing 寫導航電腦程式，或為 Raytheon 設計雷達，那這本書不適合你。去 Georgia Tech、UW 之類的學校拿個高等學位吧，因為你會需要的。這本書是為業餘愛好者、好奇的人，以及需要對資料做濾波或 smoothing（平滑）的工程師寫的。

這本書是互動式的。雖然你可以把它當作靜態內容在線上閱讀，但我強烈建議你按照它的設計方式來使用。它是用 Jupyter Notebook 寫成的，讓我可以把文字、數學、Python 和 Python 的輸出放在同一個地方。書裡每一張圖、每一筆資料，都是由 notebook 裡你隨手可得的 Python 程式產生的。想把某個參數的值加倍？點一下 Python cell，改掉參數的值，再按「Run」。新的圖或輸出就會出現在書裡。

這本書有練習題，但也附有答案。我信任你。如果你只需要答案，儘管直接去看答案。如果你想把這些知識內化，就試著在看答案之前先自己實作練習題。

這本書附有一些輔助函式庫，用來計算統計量、繪製各種與濾波器相關的圖，以及實作我們會談到的各種濾波器。這裡必須強烈提醒一點：大部分的程式碼都是為了教學目的而寫的。我很少選擇最有效率的解法（那通常會讓程式碼的意圖變得模糊），而且在本書的前幾部分，我並不在意數值穩定性。理解這一點很重要——飛機上的 Kalman filter 是經過精心設計與實作以確保數值穩定的；而最單純的實作在許多情況下並不穩定。如果你是認真要鑽研 Kalman filter，這本書不會是你需要的最後一本書。我的目的是帶你認識這些概念與數學，把你帶到能夠讀懂那些教科書的程度。

最後，這本書是免費的。學習 Kalman filtering 所需的那些書，價格就連像我這樣的矽谷工程師都覺得有點難以負擔；我不相信經濟蕭條地區的人，或是經濟拮据的學生負擔得起。我從 Python 這類自由軟體，以及 Allen B. Downey 的免費書籍（[這裡](http://www.greenteapress.com/)）得到了太多。該是回報的時候了。所以，這本書是免費的，它放在免費的伺服器上，並且只使用 IPython 和 MathJax 這類自由且開放的軟體來製作。


## 線上閱讀

這本書是以一系列 Jupyter Notebook 寫成的，那是一套互動式、以瀏覽器為基礎的系統，讓你能把文字、Python 和數學結合在瀏覽器裡。線上閱讀的方式有好幾種，列在下面。

### binder

binder 在線上提供互動式 notebook，所以你不必下載這本書、也不必安裝 Jupyter，就能在瀏覽器裡執行與修改程式碼。（英文原版）

[![Binder](http://mybinder.org/badge.svg)](https://beta.mybinder.org/v2/gh/rlabbe/Kalman-and-Bayesian-Filters-in-Python/master)


### nbviewer

http://nbviewer.org 這個網站提供了一個 Jupyter Notebook 伺服器，能把存放在 github（或其他地方）的 notebook 渲染出來。渲染是在你載入這本書時即時進行的。你可以用[*這個 nbviewer 連結*](http://nbviewer.ipython.org/github/rlabbe/Kalman-and-Bayesian-Filters-in-Python/blob/master/table_of_contents.ipynb)（英文原版）透過 nbviewer 閱讀我的書。如果你今天讀了我的書，而我明天做了修改，那你明天再回去看時就會看到那個修改。notebook 是以靜態方式渲染的——你可以閱讀，但不能修改或執行程式碼。

nbviewer 似乎會比簽入的版本落後幾天，所以你讀到的可能不是最新的內容。


### GitHub

GitHub 可以直接渲染 notebook。瀏覽 notebook 最快的方式就是直接點選上方的檔案。不過它渲染數學式的方式有誤，如果你不只是想稍微翻翻這本書，我無法推薦這種方式。


PDF 版本
-----

本書的 PDF 版本可以在[這裡]https://drive.google.com/file/d/0By_SW19c1BfhSVFzNHc0SjduNzg/view?usp=sharing&resourcekey=0-41olC9ht9xE3wQe2zHZ45A)取得（英文原版）


PDF 通常會落後於 github 上的內容，因為我不會為每一次小修改都更新它。


## 下載並執行這本書

不過，這本書的設計是互動式的，我建議以那種形式來使用它。設定起來要多花一點功夫，但很值得。如果你在電腦上安裝 IPython 和一些輔助函式庫，然後 clone 這本書，你就能自己執行書裡所有的程式碼。你可以做實驗、看看濾波器對不同的資料有什麼反應、看看不同的濾波器對同一份資料有什麼反應，等等。我覺得這種即時回饋既關鍵又令人振奮。你不必再猜「如果……會怎樣」。試試看就知道了！

這本書和輔助軟體可以在命令列執行以下指令，從 GitHub 下載：

    git clone --depth=1 https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python.git
    pip install filterpy

IPython 生態系的安裝說明可以在「Installation（安裝）」附錄中找到，連結在[這裡](http://nbviewer.ipython.org/github/rlabbe/Kalman-and-Bayesian-Filters-in-Python/blob/master/Appendix-A-Installation.ipynb)（英文原版）。

軟體安裝好之後，你可以切換到安裝目錄，用以下命令列指令執行 Jupyter notebook

    jupyter notebook

這會開啟一個瀏覽器視窗，顯示基底目錄的內容。這本書是以章為單位組織的，每一章放在一本 IPython Notebook 裡（這些 notebook 檔案的副檔名是 .ipynb）。舉例來說，要閱讀第 2 章，就點選 *02-Discrete-Bayes.ipynb* 這個檔案。有時候會有一些輔助 notebook，用來做像是產生章節中所顯示的動畫這類的事。這些並不是要給一般讀者閱讀的，不過如果你好奇動畫是怎麼做出來的，當然可以去看看。你可以在名為 *Supporting_Notebooks* 的資料夾裡找到這些 notebook。

（譯註：若要執行本繁體中文翻譯版，請參考本文件最上方的「如何執行」段落；翻譯版直接用系統 Python 即可，不需要 docker 或 venv。）

我承認，以一本書來說這是個有點笨重的介面；我是跟隨其他幾個專案的腳步，把 Jupyter Notebook 稍微挪作他用來產生整本書。我覺得這些小小的不便換來了巨大的回報——你不必在試著讀書的同時，另外下載一份程式碼然後在 IDE 裡執行，所有的程式碼和文字都在同一個地方。如果你想修改程式碼，儘管改，而且馬上就能看到修改的效果。如果你發現了 bug，可以修好它，然後推回我的 repository，讓全世界的人都受惠。當然，你也永遠不會碰到我在傳統書籍上經常遇到的問題——書和程式碼彼此不同步，而你只能搔著頭不知道該相信哪一邊。


配套軟體
-----

[![Latest Version](http://img.shields.io/pypi/v/filterpy.svg)](http://pypi.python.org/pypi/filterpy)

我寫了一個開源的 Bayesian filtering Python 函式庫，叫做 **FilterPy**。我已經把這個專案放上 PyPi（Python Package Index）。要從 PyPi 安裝，在命令列下這個指令

    pip install filterpy

如果你沒有 pip，可以依照這裡的說明：https://pip.pypa.io/en/latest/installing.html 。

本書用到的所有濾波器，以及其他書裡沒提到的濾波器，都實作在我的 Python 函式庫 FilterPy 裡，可以在[這裡](https://github.com/rlabbe/filterpy)取得。閱讀這本書並不需要下載或安裝它，但你很可能會想用這個函式庫來寫自己的濾波器。它包含 Kalman filter、Fading Memory filter（衰減記憶濾波器）、H infinity filter（H∞ 濾波器）、Extended 與 Unscented filter（擴展與無損濾波器）、least square filter（最小平方濾波器）等等許多種。它也包含一些輔助函式，可以簡化某些濾波器所用矩陣的設計，以及其他程式碼，例如以 Kalman 為基礎的 smoother（平滑器）。


FilterPy 放在 github 上（https://github.com/rlabbe/filterpy ）。如果你想要最前沿的版本，就從 github 抓一份下來，然後依照你的 Python 安裝方式的說明，把它加進 Python 的搜尋路徑。這可能會讓你碰到一些不穩定的情況，因為你拿到的可能不是測試過的釋出版本，但好處是你也會拿到所有用來測試這個函式庫的測試腳本。你可以研究這些腳本，看到許多在 Jupyter Notebook 環境之外撰寫與執行濾波器的範例。

另一種方式：在 Conda 環境中執行這本書
----
如果你安裝了 conda 或 miniconda，可以用以下指令建立環境

    conda env update -f environment.yml

然後用

    conda activate kf_bf

與

    conda deactivate kf_bf

來啟用與停用這個環境。


問題或疑問
------

如果你有意見，可以在 GitHub 上開一個 issue，這樣大家都能連同我的回覆一起讀到。請不要把它只當作回報 bug 的管道。另外，我也建立了一個 gitter 聊天室供比較非正式的討論。 [![Join the chat at https://gitter.im/rlabbe/Kalman-and-Bayesian-Filters-in-Python](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/rlabbe/Kalman-and-Bayesian-Filters-in-Python?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


License（授權）
-----
（以下為原書的授權聲明，法律條文保留英文原文。本翻譯版沿用相同授權：文字為 CC BY 4.0，程式碼為 MIT。）

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">Kalman and Bayesian Filters in Python</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python" property="cc:attributionName" rel="cc:attributionURL">Roger R. Labbe</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.

本書中的所有軟體、支援本書的軟體（例如 code 目錄中的）或用於產生本書的軟體（在 pdf 目錄中），只要包含在這個 repository 裡，皆以下列 MIT 授權釋出：

The MIT License (MIT)

Copyright (c) 2015 Roger R. Labbe Jr

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.TION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

聯絡方式
-----

rlabbejr at gmail.com

## 已知問題（原書既有，非翻譯造成）

以下 notebook 在原版英文 repo 中執行時也會出現相同錯誤。本翻譯版的 code cell 與原書逐字相同，因此保留原狀：

| Notebook | 錯誤 | 原因 |
|---|---|---|
| `table_of_contents.ipynb` | `ImportError: cannot import name 'load_style'` | 原書 `book_format.py` 已沒有 `load_style`；目錄頁本身只有連結，不影響閱讀 |
| `Appendix-I-Analytic-Evaluation-of-Performance.ipynb` | 同上 | 同上，此附錄原文尚未完成 |
| `animations/Gaussians_Animations.ipynb` | `ModuleNotFoundError: No module named 'stats'` | 引用了原書早期版本的模組 |
| `animations/Kalman_Filters_Animations.ipynb` | `NameError: name 'voltage' is not defined` | 原書程式碼遺漏定義 |

animations 資料夾只是用來產生書中 GIF 的輔助檔，GIF 已附在資料夾中。

## 翻譯工具

`tools/` 內是產生本翻譯版的腳本：`extract.py` 抽出 markdown cell、`inject.py` 寫回翻譯、`check.py` 比對結構（LaTeX、連結、標題、code cell 是否與原書一致）、`run_all.sh` 用系統 Jupyter 執行全部 notebook，`STYLE.md` 是翻譯風格規範。
