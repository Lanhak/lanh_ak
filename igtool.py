import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

ACCOUNTS_FILE = "accounts.json"


# ===========================
# Load danh sách tài khoản
# ===========================
def load_accounts():
    if not os.path.exists(ACCOUNTS_FILE):
        return []
    try:
        with open(ACCOUNTS_FILE, "r") as f:
            return json.load(f)
    except:
        return []


# ===========================
# Lưu danh sách tài khoản
# ===========================
def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent=4)


# ===========================
# Setup selenium browser
# ===========================
def setup_driver():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    return driver


# ===========================
# Lấy cookie 1 tài khoản
# ===========================
def get_cookie(username):
    print(f"\n🔄 Mở Instagram để login tài khoản: {username}")
    driver = setup_driver()

    driver.get("https://www.instagram.com/accounts/login/")

    print("➡ Sau khi bạn đăng nhập xong → trở về Termux bấm Enter để tiếp tục.")
    input("Nhấn Enter khi đăng nhập hoàn tất...")

    cookies = driver.get_cookies()
    file = f"{username}_cookies.json"

    with open(file, "w") as f:
        json.dump(cookies, f, indent=4)

    print(f"✅ Đã lưu cookie vào file: {file}\n")
    driver.quit()


# ===========================
# MENU CHÍNH
# ===========================
def menu():
    accounts = load_accounts()

    while True:
        print("""
=== IG COOKIE TOOL ===
1) Login tài khoản đầu tiên & lưu cookie
2) Thêm tài khoản (login + lưu cookie)
3) Lấy cookie TẤT CẢ tài khoản
4) Lấy cookie TỪNG tài khoản (menu con)
0) Thoát
""")
        choice = input("Chọn: ").strip()

        # 1) login tài khoản đầu tiên
        if choice == "1":
            username = input("Nhập username IG: ").strip()
            if username not in accounts:
                accounts.append(username)
                save_accounts(accounts)
            get_cookie(username)

        # 2) Thêm tài khoản + login + lưu cookie
        elif choice == "2":
            username = input("Nhập username IG cần thêm: ").strip()

            if username in accounts:
                print("⚠ Tài khoản đã tồn tại, nhưng vẫn login để lấy cookie mới.")
            else:
                accounts.append(username)
                save_accounts(accounts)
                print(f"✅ Đã thêm tài khoản mới: {username}")

            get_cookie(username)

        # 3) Lấy cookie tất cả
        elif choice == "3":
            if not accounts:
                print("⚠ Chưa có tài khoản nào!")
                continue

            print("\n🔄 Lấy cookie tất cả tài khoản...")
            for acc in accounts:
                print(f"--- {acc} ---")
                get_cookie(acc)
            print("🎉 Hoàn tất!")

        # 4
        elif choice == "4":
            if not accounts:
                print("⚠ Danh sách trống!")
                continue

            print("\n=== Danh sách tài khoản ===")
            for i, acc in enumerate(accounts):
                print(f"{i+1}) {acc}")

            sel = input("Chọn số: ").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(accounts):
                username = accounts[int(sel)-1]
                get_cookie(username)
            else:
                print("❌ Lỗi lựa chọn!")

        elif choice == "0":
            break

        else:
            print("❌ Sai lựa chọn!")


if __name__ == "__main__":
    menu()