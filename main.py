import os
import zipfile
import time
import threading
import requests
import schedule
from datetime import datetime

import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

# ====== 參數 ======

SOURCE_FOLDER = r"C:\Users\GayBottle\AppData\Roaming\RenPy\Monika After Story" # 換成你的路徑 我直接寫死了 懶得取相對路徑
ZIP_PATH = "monika_backup.zip"

GOFILE_UPLOAD_URL = "https://upload-ap-sgp.gofile.io/uploadfile" # 根據你的所在地區選擇離你最近的節點 可以上gofile.io api查看

DISCORD_WEBHOOK_URL = "your discord webhook"

BACKUP_INTERVAL_MINUTES = 5 # 每隔5分鐘備份一次

# ====================

running = True


# ---------- 功能 ----------

def create_zip(source_folder, zip_path):
    if os.path.exists(zip_path):
        os.remove(zip_path)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, source_folder)
                z.write(full_path, rel_path)


def upload_to_gofile(zip_path):
    with open(zip_path, 'rb') as f:
        files = {"file": f}
        try:
            r = requests.post(GOFILE_UPLOAD_URL, files=files, timeout=300)
            data = r.json()
            if data.get("status") == "ok":
                return True, data["data"]["downloadPage"]
            else:
                return False, str(data)
        except Exception as e:
            return False, str(e)


def send_discord_message(success, message):
    if success:
        content = (
            "✅ **Monika 存檔備份完成！**\n"
            f"📦 下載頁面：{message}\n"
            f"🕒 時間：{datetime.now()}"
        )
    else:
        content = (
            "❌ **備份失敗！**\n"
            f"⚠ 錯誤：{message}\n"
            f"🕒 時間：{datetime.now()}"
        )

    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": content}, timeout=10)
    except:
        pass


def backup_job():
    print("開始備份")

    try:
        create_zip(SOURCE_FOLDER, ZIP_PATH)
        success, result = upload_to_gofile(ZIP_PATH)

        if success:
            send_discord_message(True, result)
            try:
                os.remove(ZIP_PATH)   # 上傳成功才刪zip
            except:
                pass
        else:
            send_discord_message(False, result)

    except Exception as e:
        send_discord_message(False, str(e))


# ---------- 排程執行緒 ----------

def scheduler_loop():
    schedule.every(BACKUP_INTERVAL_MINUTES).minutes.do(backup_job)

    backup_job()  # 啟動先跑一次

    while running:
        schedule.run_pending()
        time.sleep(1)


# ---------- 圖示 ----------

def create_image():
    img = Image.new('RGB', (64, 64), (40, 40, 40))
    d = ImageDraw.Draw(img)
    d.ellipse((16, 16, 48, 48), fill=(0, 200, 255))
    return img


def on_backup_now(icon, item):
    threading.Thread(target=backup_job, daemon=True).start()


def on_exit(icon, item):
    global running
    running = False
    icon.stop()


# ---------- 主程式 ----------

def main():
    # 啟動排程執行緒
    t = threading.Thread(target=scheduler_loop, daemon=True)
    t.start()

    # 圖示右鍵選單
    menu = (
        item("立即備份", on_backup_now),
        item("結束程式", on_exit),
    )

    icon = pystray.Icon("MonikaBackup", create_image(), "Monika Backup Running", menu)
    icon.run()

if __name__ == "__main__":
    main()
