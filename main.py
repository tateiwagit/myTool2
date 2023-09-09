# 目標　nijieのルカリオを自動で新着監視、通知する
import requests
from bs4 import BeautifulSoup
import time
from time import sleep

# セッションを作成
session = requests.Session()

# 与えられたURLからHTMLコンテンツを取得する関数
def get_html(url):
    response = session.get(url)
    return response.text

# HTMLから指定のテキストを含むリンクを探索する関数
def find_links_with_text(html, unique_text):
    links = []
    soup = BeautifulSoup(html, 'lxml')
    
    # <a> タグを探し、href属性とテキストコンテンツを取得
    for a_tag in soup.find_all('a'):
        href = a_tag.get('href')
        text = a_tag.get_text()
        
        # テキストに指定のテキストが含まれているか確認
        if unique_text in text:
            links.append(href)
    
    return links

# メインの実行部分
if __name__ == '__main__':
    # 与えられたURLを指定
    url_searching = 'https://nijie.info/age_ver.php?'
    unique_text = '私は18歳以上'

    # URLからHTMLを取得
    html = get_html(url_searching)
    sleep(3)

    # 指定のテキストを含むリンクを探索
    links = find_links_with_text(html, unique_text)
    print(f'Links URL: {links}\n')

    # 各リンクからページを取得
    for link in links:
        if link.startswith('http://') or link.startswith('https://'):
            # 絶対URLの場合
            link_url = link
        else:
            # 相対URLの場合、元のURLと結合して絶対URLを作成
            link_url = session.get(url_searching).url + link

        # ページを取得
        linked_page_html = get_html(link_url)
        sleep(3)
        # ここで必要な処理を実行
        # 例: ページの内容を解析したり、保存したり

        # ページの内容を表示（テスト用）
        print(f'Linked Page URL: {link_url}')
        print(linked_page_html)

        
    session.close()
