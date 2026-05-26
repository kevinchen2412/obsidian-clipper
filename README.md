# Obsidian Clipper PWA — 部署指南

## 📁 檔案清單

```
obsidian-clipper/
├── index.html      ← 主程式（UI + 邏輯）
├── manifest.json   ← PWA 設定（含 Share Target）
├── sw.js           ← Service Worker（離線支援）
├── icon-192.png    ← App 圖示
└── icon-512.png    ← App 圖示（大）
```

---

## 🚀 部署到 GitHub Pages（免費 HTTPS，推薦）

### 步驟一：建立 GitHub Repo

1. 登入 [github.com](https://github.com)
2. 右上角 **New repository**
3. Repository name：`obsidian-clipper`（或任意名稱）
4. 設為 **Public**（Pages 免費方案需 Public）
5. 點 **Create repository**

### 步驟二：上傳檔案

方法 A（網頁介面）：
1. 在 repo 頁面點 **Add file → Upload files**
2. 把 `index.html`、`manifest.json`、`sw.js`、兩個 `.png` 全部拖進去
3. 點 **Commit changes**

方法 B（git 指令）：
```bash
git clone https://github.com/你的帳號/obsidian-clipper.git
cp /path/to/files/* obsidian-clipper/
cd obsidian-clipper
git add .
git commit -m "init"
git push
```

### 步驟三：開啟 GitHub Pages

1. repo 頁面 → **Settings → Pages**
2. Source 選 **Deploy from a branch**
3. Branch 選 **main**，資料夾選 **/ (root)**
4. **Save**
5. 等約 1 分鐘，取得網址：`https://你的帳號.github.io/obsidian-clipper/`

---

## 📱 手機安裝 PWA

1. 手機用 **Chrome** 開啟上述網址
2. 點右上角 **⋮ → 新增到主畫面**
3. 名稱保持 "Obsidian Clipper"，點**新增**
4. 桌面會出現 App 圖示

---

## 🔗 使用流程

```
瀏覽網頁
  → 點分享按鈕
    → 選「Obsidian Clipper」
      → 確認標題／備註／標籤
        → 點「存入 Obsidian」
          → 自動跳 Obsidian App
            → 筆記建立於 Clippings/ 資料夾
```

---

## ⚙️ 客製化

### 修改預設 Vault 名稱
- 在 App 畫面最下方「Vault 資料夾名稱」欄位直接修改
- 會自動儲存到本機（localStorage）

### 修改預設標籤
在 `index.html` 找到這行，改成你想要的預設標籤：
```javascript
let tags = ['clipping'];
```

### 修改目標資料夾（Clippings 以外）
在 `index.html` 找到：
```javascript
`&file=${encodeURIComponent('Clippings/' + filename)}`
```
改成你想要的路徑，例如 `'06-Inbox/' + filename`

---

## 🔒 隱私說明

- **所有處理在手機本地完成**，無任何資料上傳至伺服器
- GitHub Pages 只提供靜態檔案，不記錄你剪藏的內容
- Obsidian URI 呼叫直接在手機系統層完成

---

## ❓ 常見問題

**Q：分享選單沒出現 Obsidian Clipper？**
A：需先安裝為 PWA（新增到主畫面），且必須用 Chrome 安裝。

**Q：點「存入 Obsidian」後沒反應？**
A：確認 Vault 名稱是否正確。Vault 名稱 = 手機上 Obsidian 資料夾的名稱（預設為 `obsidian`）。

**Q：筆記出現在哪裡？**
A：`內部儲存空間/obsidian/Clippings/筆記標題.md`

**Q：可以加密 Vault 嗎？**
A：可搭配 Obsidian 的 Meld Encrypt 外掛對特定筆記加密，但 Clippings 資料夾本身建議保持明文（方便搜尋）。
