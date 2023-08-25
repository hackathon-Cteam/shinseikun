# 申請くん
RareTECHハッカソン2023年夏の陣 初級者コース CチームのChatAppです。

申請・申込をテーマとし、ユーザーと申請受付担当者がつながるチャットアプリです。


**起動方法**
```
docker compose up
```

### ディレクトリ構成
```
.
├── ChatApp
│   ├── app.py
│   ├── common
│   │   └── util
│   ├── entity # テンプレート返却用クラス
│   ├── model
│   │   └── external # DB操作クラス
│   └── view
│       ├── static
│       │   ├── css
│       │   ├── img
│       │   └── js
│       │       └── common
│       └── templates
│           ├── error
│           └── page 
└── Docker
    ├── Flask
    └── MySQL
```