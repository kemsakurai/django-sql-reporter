# django-sql-reporter

業務データ監視のための、SQL実行、結果通知を行うDjango plugin。
以下の記事に触発されてツールは作成しています。       
[SQLを使った監視でデータ基盤の品質を向上させる - MonotaRO Tech Blog](https://tech-blog.monotaro.com/entry/2021/08/24/100000)      

yamlの定義ファイル元にSQLを実行し、SQLの実行結果をメールで通知します。
メール送付先は、Gmailでメール受信後は、Google Apps Scriptでメール本文のJSONデータを取得し、     
Google スプレッドシートやBig Query にデータを登録して分析するというユースケースをイメージしています。

もしかすると、通知方法を変更できると便利かもしれませんが、まずメール関連の機能追加を優先しています。

---

## ライセンス      

MIT

