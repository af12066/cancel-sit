# cancel-sit

芝浦工業大学の休講情報をスクレイピングしてSlackにポストしてくれます。

## 使用方法

1. `slack = Slack('...')` の`...`にSlackのトークンを入力する．
2. cronかなにかで定期的にスクリプトを実行します．
3. 休講情報が更新されるとSlackにポストされます．

## モジュール

以下のモジュールが必要になります．

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Slacker](https://github.com/os/slacker)
