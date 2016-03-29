# -*- coding: utf-8 -*-
# Copyright (c) T. H.

import urllib.request
import re
import urllib.parse
import codecs
import filecmp
import os.path
import os
from bs4 import BeautifulSoup
from slacker import Slacker
from datetime import datetime

class Slack(object):
    __slacker = None

    def __init__(self, token):
        self.__slacker = Slacker(token)

    def get_channnel_list(self):
        """
        Slackチーム内のチャンネルID、チャンネル名一覧を取得する。
        """

        # bodyで取得することで、[{チャンネル1},{チャンネル2},...,]の形式で取得できる。
        raw_data = self.__slacker.channels.list().body

        result = []
        for data in raw_data["channels"]:
            result.append(dict(channel_id=data["id"], channel_name=data["name"]))

        return result

    def post_message_to_channel(self, channel, message):
        """
        Slackチームの任意のチャンネルにメッセージを投稿する。
        """

        channel_name = "#" + channel
        self.__slacker.chat.post_message(channel_name, message)

def writeFile(fileName, content):
    print(fileName)
    f = codecs.open(fileName, 'w', 'utf-8')
    f.write(content)

    f.close()


if __name__ == '__main__':
    slack = Slack('...')

    print(slack.get_channnel_list())

    #今月と翌月のデータを取得
    uri = 'http://attend.sic.shibaura-it.ac.jp/cancelCalendar/t04/calendar{0:d}{1:02d}-{2:02d}.html'.format(datetime.today().year, datetime.today().month, (lambda x: x if x != 12 else x - 11)(datetime.today().month + 1))

    html = urllib.request.urlopen(uri)
    soup = BeautifulSoup(html, 'lxml')

    link = soup.find_all('a', href=re.compile("/cancel/")) #href属性に'/cancel/'を含むa要素を取得し，相対パスを絶対パスに変換

    for a in link:
        path = urllib.parse.urljoin(uri, a['href']) #href属性のみを取得
        print(path)

        fileName = path.split('/')[-1]
        fileName = fileName.replace("html", "txt")

        html2 = urllib.request.urlopen(path) #リストの要素のURLをオープン
        soup2 = BeautifulSoup(html2, 'lxml')
        dat = soup2.find_all(text=True) #テキストをすべて取得
        settext = "\n".join([x for x in dat if x != '\n']) #改行文字のみのリスト項目を削除．リストを結合し，文字列を整形

        # スクレイピングしたテキストを書き出す．
        # もしその日付のファイルが存在しなければ新規に作成し，
        # 既にファイルが存在していれば拡張子に'.tmp'を付加して一時ファイルを作成する．
        # もとのtxtファイルとtmpファイルの差分を比較し，更新があればtxtファイルを更新し，Slackにポストする．
        if os.path.isfile(fileName):
            tmpfileName = fileName + '.tmp'
            writeFile(tmpfileName, settext)

            if filecmp.cmp(fileName, tmpfileName):
                print("no diff")
            else:
                writeFile(fileName, settext)
                slack.post_message_to_channel("class", settext) #Slackにポスト (チャンネル, テキスト)
            os.remove(tmpfileName)

        else:
            #print('write a new file')
            slack.post_message_to_channel("class", settext) #Slackにポスト (チャンネル, テキスト)
            writeFile(fileName, settext)
