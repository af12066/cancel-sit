# -*- coding: utf-8 -*-
# Copyright (c) T. H.

import urllib.request
import re
import urllib.parse
from bs4 import BeautifulSoup

uri = 'http://attend.sic.shibaura-it.ac.jp/cancelCalendar/t04/calendar201512-01.html'

html = urllib.request.urlopen(uri)
soup = BeautifulSoup(html, 'lxml')

link = soup.find_all('a', href=re.compile("/cancel/")) #href属性に'/cancel/'を含むa要素を取得し，相対パスを絶対パスに変換

for a in link:
    path = urllib.parse.urljoin(uri, a['href']) #href属性のみを取得
    print(path)

    html2 = urllib.request.urlopen(path) #リストの要素のURLをオープン
    soup2 = BeautifulSoup(html2, 'lxml')
    dat = soup2.find_all(text=True) #テキストをすべて取得
    print([x for x in dat if x != '\n']) #改行文字のみのリスト項目を削除
