## 仮想環境作成
```
python3 -m venv .venv
```

## 仮想環境に入る
### Mac
```
source .venv/bin/activate
```
### Win
```
.venv\Scripts\activate.bat
```

## ライブラリ読み込み
```
python -m pip install -r requirements.txt
```

## kabu_list.xlsx作成

| code | getPrice |
| ---- | ---- |
| 銘柄コード | 取得単価 |

## .envファイル作成

### Line Notify登録
https://notify-bot.line.me/ja/

### アクセストークン発行
.envファイルにLINE_TOKEN変数で登録

## Pythonプロジェクト起動
```
python app.py
```
