# 用 venv 執行本翻譯版

本文件說明如何用 Python 內建的 `venv` 建立獨立環境來執行 `zh-TW/` 內的 notebook，避免套件裝進系統 Python 而與其他專案互相干擾。
README 的「如何執行」是直接裝到系統 Python 的做法，兩者擇一即可。

## 需求

* Python 3.9 以上（macOS 的 Xcode Command Line Tools 自帶 `/usr/bin/python3` 3.9.6 即可）。
* 不需要 docker、conda 或其他工具。

## 建立環境

venv 建在 repo **根目錄**（`Kalman-and-Bayesian-Filters-in-Python/.venv`），英文原版與 zh-TW 版可共用同一個環境。

```bash
cd Kalman-and-Bayesian-Filters-in-Python
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
```

接著安裝套件，二選一：

**A. 鎖定版本（建議，多台機器可裝出一致的環境）**

```bash
pip install -r zh-TW/requirements.lock
```

**B. 最新相容版本**

```bash
pip install -r zh-TW/requirements.txt
```

`requirements.lock` 是在 macOS、Python 3.9.6 上由 `pip freeze` 產生；主要套件版本如下：

| 套件 | 版本 |
|---|---|
| filterpy | 1.4.5 |
| numpy | 2.0.2 |
| scipy | 1.13.1 |
| matplotlib | 3.9.4 |
| sympy | 1.14.0 |
| notebook | 7.5.8 |

`.venv/` 與 `_executed/` 已列在根目錄的 `.gitignore`，不會被 commit。

## 啟動 Jupyter

notebook **必須在 `zh-TW/` 目錄內開啟**，因為每一章開頭會用相對路徑載入 `book_format.py` 與 `kf_book/`。

```bash
source .venv/bin/activate
cd zh-TW
jupyter notebook        # 或 jupyter lab
```

用 venv 內的 `jupyter` 啟動時，預設 kernel 就是這個 venv，不需另外註冊 kernel。
若你習慣從別的 Jupyter（例如 VS Code）開啟，可把 venv 註冊成 kernel：

```bash
python -m ipykernel install --user --name kf_bf --display-name "Python (kf_bf)"
```

## 驗證環境

1. 匯入檢查。在 `zh-TW/` 內執行，會觸發 `book_format.test_installation()`；正常時只印出版本，不會有「Please install ...」或最低版本警告：

   ```bash
   cd zh-TW
   python -c "import book_format, filterpy, numpy; print(filterpy.__version__, numpy.__version__)"
   ```

2. 實際執行一章。`tools/run_all.sh` 會用 nbconvert 跑指定的 notebook，結果寫到 `zh-TW/_executed/`，不會動到原 notebook：

   ```bash
   cd zh-TW
   bash tools/run_all.sh 01-g-h-filter.ipynb     # 單章
   bash tools/run_all.sh                         # 全部
   ```

   預期輸出 `OK    01-g-h-filter.ipynb (...s)`。

## 更新鎖定檔

升級套件後，重新產生 `requirements.lock`：

```bash
source .venv/bin/activate
pip freeze > zh-TW/requirements.lock
```

## 注意事項

* `book_format.py` 使用 `distutils.version.LooseVersion`，而 Python 3.12 起已移除 `distutils`。若改用 3.12 以上的 Python，venv 內必須裝有 `setuptools`（它會提供 `distutils` 相容層），上面的 `pip install --upgrade setuptools` 已涵蓋。
* Python 3.9 已於 2025 年 10 月停止維護。若換成較新的 Python，請重新產生 `requirements.lock`，因為舊鎖定檔裡的 numpy/scipy 版本可能沒有對應新版 Python 的 wheel。
* `tools/run_all.sh` 的註解寫「no venv」，但它只是呼叫 `PATH` 上的 `jupyter`，啟用 venv 後可直接使用。
