import firebase_admin
from firebase_admin import credentials, firestore
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

# Firebaseの初期化
cred = credentials.Certificate('manga.json')  # サービスアカウントキーのパスを指定
firebase_admin.initialize_app(cred)
db = firestore.client()

def convert_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%Y年%m月%d日発売')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        return None

# SeleniumでChromeを使用
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # ヘッドレスモードで実行（ブラウザを表示しない）
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# スクレイピングするURL
url = "https://www.shueisha.co.jp/books/newcomics/index.html?genre=inherit"
driver.get(url)
driver.implicitly_wait(3)  # 3秒待機

# 必要な情報を抽出
sections = driver.find_elements(By.CLASS_NAME, 'single-item')
print(f"Found {len(sections)} sections.")

for section in sections:
    title_element = section.find_element(By.CLASS_NAME, 'bktitle').find_element(By.TAG_NAME, 'a')
    title = title_element.text.strip() if title_element else 'N/A'
    
    author_element = section.find_element(By.TAG_NAME, 'p').find_element(By.TAG_NAME, 'a')
    author = author_element.text.strip() if author_element else 'N/A'
    
    release_date_element = section.find_elements(By.TAG_NAME, 'p')[-1]
    release_date_raw = release_date_element.text.strip() if release_date_element else 'N/A'
    release_date = convert_date(release_date_raw)
    
    img_element = section.find_element(By.TAG_NAME, 'img')
    img_url = img_element.get_attribute('src') if img_element else 'N/A'

    # Firestoreにデータを保存
    doc_ref = db.collection('comics').add({
        'title': title,
        'author': author,
        'release_date': release_date,
        'image_url': img_url
    })

# ブラウザを閉じる
driver.quit()
