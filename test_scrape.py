import os
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# PATH環境変数にChromeDriverのパスを追加
os.environ["PATH"] += os.pathsep + '/home/terms/bin/mongodb/chromedriver-linux64/'

# SeleniumでChromeを起動
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

# 起点となるページへ移動
loginUrl = "https://www.seaart.ai/explore/detail/cka430p4msb8st1im62g"
driver.get(loginUrl)

# 最大で20秒待つ設定
wait = WebDriverWait(driver, 20)

# スクロールを続ける
while True:
    # 1スクロールごとに要素を取得
    try:
        parent_elements = driver.find_elements(By.CLASS_NAME, 'waterfall-item')  # 親要素
        child_elements = driver.find_elements(By.CLASS_NAME, 'cntImg')  # 子要素

        for parent, child in zip(parent_elements, child_elements):
            parent_url = parent.get_attribute("href")
            child_src = child.get_attribute("src")
            
            print(f"親要素のURL: {parent_url}")
            print(f"子要素のsrc: {child_src}")

    except TimeoutException:  # 要素が見つからない場合
        print("要素が見つかりません。")
    
    # スクロール
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # スクロール後に要素が読み込まれるまで少し待つ
    
    # 「これ以上のデータはありません」が出現したら終了
    try:
        tips_elements = driver.find_elements(By.CLASS_NAME, 'tips')
        end_of_data_element = [elem for elem in tips_elements if 'これ以上のデータはありません' in elem.text]
        
        if end_of_data_element:
            print("No more data to load.")
            break
    except NoSuchElementException:
        continue


# ブラウザを閉じる
driver.quit()
