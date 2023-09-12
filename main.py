# 目標　nijieのルカリオを自動で新着監視、通知する
import subprocess
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

from datetime import datetime

# 文字列から年月日と時間を取得する関数
def extract_datetime_from_string(date_string):
    try:
        # "投稿時間："の部分を削除してから、指定された形式の文字列を解析してdatetimeオブジェクトを作成
        date_format = '%Y-%m-%d %H:%M:%S'
        parsed_date = datetime.strptime(date_string, date_format)
        return parsed_date
    except ValueError:
        print("無効な日時形式です。")

# 日時の比較を行う関数
def compare_dates(date1, date2):
    if date1 > date2:
        return "date1が後の日時です。"
    elif date2 > date1:
        return "date2が後の日時です。"
    else:
        return "両方の日時は同じです。"

# 設定ファイルからemailとpasswordを読み込む関数
def read_user_info_from_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    if 'user_info' in config:
        email = config['user_info'].get('email')
        password = config['user_info'].get('password')
        return email, password
    else:
        return None, None

# 設定ファイルからLucarioのチェック日時を取得する関数
def read_check_date_from_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    if 'check_date' in config:
        lucario_date = config['check_date'].get('Lucario')
        return lucario_date
    else:
        return None

# メッセージをUbuntu通知として表示する関数
def send_notification(message):
    subprocess.run(['notify-send', message])

# 設定ファイルのパス
config_file = 'config/config.ini'
    
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

    # 設定ファイルからemailとpasswordを読み込む
    my_email, my_pass = read_user_info_from_config(config_file)
    print(f"read info: {my_email}, {my_pass}")

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

    search_word = "ルカリオ"
    input_id = "form2"
    search_input = driver.find_element(By.ID, input_id)
    search_input.send_keys(search_word)
    sleep(3)

    search_btn_xpath = "//*[@id='btn']"
    search_button = driver.find_element(By.XPATH, search_btn_xpath)
    search_button.click()
    sleep(3)

    item_for_search = "/html/body/div[3]/div[2]/div[2]/div[5]/div[1]/p[1]/a"
    page_button = driver.find_element(By.XPATH, item_for_search)
    page_button.click()
    sleep(3)

    item_for_search = "/html/body/div[2]/div[2]/div[4]/div[3]/div[2]/p/span"
    element = driver.find_element(By.XPATH, item_for_search)
    time = element.text
    print(f"post time: {time}")

    # テスト用の文字列
    date_string1 = time
    date_string1 = date_string1.replace("投稿時間：", "")
    date_string2 = read_check_date_from_config(config_file)  # config.iniからLucarioのチェック日時を取得

    # 文字列から年月日と時間を取得
    date1 = extract_datetime_from_string(date_string1)
    date2 = extract_datetime_from_string(date_string2)

    if date1 and date2:
        # 日時の比較を行う
        result = compare_dates(date1, date2)
        print(f"judge new Post: {result}")

        # もしdate1が後の日時である場合、config.iniの値をdate1に書き換える
        if result == "date1が後の日時です。":
            config = configparser.ConfigParser()
            config.read(config_file)
            config.set('check_date', 'Lucario', date_string1)
            with open(config_file, 'w') as configfile:
                config.write(configfile)

            message = f'nijieの"{search_word}"カテゴリーに新着投稿があります。'
            send_notification(message)

except Exception as e:
    print(f'ボタンが見つからないか、クリックできないエラーが発生しました: {str(e)}')

# WebDriverを終了
driver.quit()
