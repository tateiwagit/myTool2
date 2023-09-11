# 目標　nijieのルカリオを自動で新着監視、通知する
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

# WebDriverを設定 (Firefoxを使用する場合)
driver = webdriver.Chrome()

# 指定したURLを開く
age_url = 'https://nijie.info/age_ver.php/'  # age_urlを実際のURLに置き換えてください
driver.get(age_url)

try:
    # 「私は１８歳以上」というテキストを持つ要素の下にあるボタンを探す
    age_verification_text = "はい、私は18歳以上です" # 後で正規表現で書き換える
    button = driver.find_element(By.LINK_TEXT, age_verification_text)

    # ボタンをクリック
    button.click()
    sleep(3)

    # ボタンをクリックした後のURLを取得
    next_page_url = driver.current_url
    print(f'次のページのURL: {next_page_url}')

    # 入力フォームにメールアドレスとパスワードを入力
    my_email = input("メールアドレスを入力してください: ")  # ご自身のメールアドレスを指定してください
    my_pass = input("パスワードを入力してください: ") # ご自身のパスワードを指定してください

    # メールアドレス入力フォームを探す
    email_input = driver.find_element(By.NAME, "email")
    email_input.send_keys(my_email)
    sleep(3)

    # パスワード入力フォームを探す
    pass_input = driver.find_element(By.NAME, "password")
    pass_input.send_keys(my_pass)
    sleep(3)

    # ログインボタンをクリック
    login_button = driver.find_element(By.CLASS_NAME, "login_button")
    login_button.click()
    sleep(3)

    # ログイン後のページのURLを取得
    logged_in_url = driver.current_url
    print(f'ログイン後のページのURL: {logged_in_url}')
    
except Exception as e:
    print(f'ボタンが見つからないか、クリックできないエラーが発生しました: {str(e)}')

# WebDriverを終了
driver.quit()
