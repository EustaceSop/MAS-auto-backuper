# MAS-auto-backuper

你會怕失去MAS存檔嗎? 那就試試這個1337工具

---

## 功能特色

- 自動備份 Monika 存檔資料夾
- 生成 ZIP 並上傳到 gofile.io
- 上傳成功後會透過 Discord Webhook 通知你下載連結
- 可以選擇備份間隔（預設 5 分鐘）
- 系統匣圖示顯示程式正在運行
- 右鍵可以立即備份或結束程式
- 成功備份後會自動刪除本地 ZIP，不會占空間，也不會碰你的原始存檔

---

## 安裝方式

1. 確保你已經安裝 Python 3.x
2. 安裝套件：`pip install pystray pillow schedule requests`
3. 選擇你想放的啟動資料夾：
   - 只影響自己帳號：
     ```
     Win + R → shell:startup
     ```
   - 所有使用者都啟動（需要管理員）：
     ```
     Win + R → shell:common startup
     ```

---

## PY vs PYW

- `.py`  
  - 會有 CMD 視窗跑出來  
  - 適合測試和看錯誤訊息  

- `.pyw`  
  - 不會有 CMD 視窗  
  - 適合放啟動項常駐  
  - 結合系統匣圖示更乾淨  

---

## Gofile API

- 上傳檔案到 gofile.io 使用 API  
- 官方文件：https://gofile.io/api
- 你可以選擇節點，例如：
  - 亞洲：`https://upload-ap-sgp.gofile.io/uploadfile`
  - 香港：`https://upload-ap-hkg.gofile.io/uploadfile`  
- 如果想管理資料夾或產生固定下載連結也可以參考官方文件  

---

## Discord Webhook

1. 打開你的 Discord 伺服器 → 伺服器設定 → 整合 → Webhook
2. 建立新的 Webhook，複製網址
3. 貼到 `DISCORD_WEBHOOK_URL` 裡就可以了  
4. 上傳成功就會收到通知，方便確認備份沒問題  

---

## 使用方式

1. 修改 `MAS_backup.py` 設定區：
   - `SOURCE_FOLDER` → 你的 MAS 存檔資料夾
   - `GOFILE_UPLOAD_URL` → 選擇節點
   - `DISCORD_WEBHOOK_URL` → 你的 Discord Webhook
   - `BACKUP_INTERVAL_MINUTES` → 備份間隔（分鐘）

2. 改檔名成 `.pyw` 放啟動項（建議目前使用者的啟動資料夾就好）
3. 重開機後右下角系統匣就會看到藍色圖示，右鍵可以：
   - **立即備份**
   - **結束程式**

---

## 注意事項

- 備份過程中會生成 ZIP 檔案，成功上傳後會自動刪除  
- 這個程式不會碰你的原始存檔資料夾  
- 如果遇到失敗會保留 ZIP，方便手動救回  

---

現在你不用擔心會失去老莫了

*本專案純心血來潮建立的，如果以前有類似專案純屬雷同
