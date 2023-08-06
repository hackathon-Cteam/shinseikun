from flask import Flask, request, redirect, render_template, session, flash, abort
from datetime import timedelta
import uuid

# アプリの設定
app = Flask(__name__, static_folder='view/static', template_folder='view/templates')
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)

# 画面表示の呼び出し

# ログイン画面のルート
@app.route('/login')
def login():
    return ""

# チャンネル一覧ページのルート
@app.route('/')
def index():
    # チャンネル名の一覧を取得
    # チャンネルID
    # 画像データの情報（データ名とか）
    # チャンネル名とIDが紐づいた形式のデータ
    return "画面の指定とテンプレート変数にデータを渡す記述"

# チャット画面ルート
@app.route('/talk') ## /talk/channel-id
def talk():
    # メッセージ情報のリスト
    return "画面の指定とテンプレート変数にデータを渡す記述" 

# 管理者画面のルート
@app.route('/admin')
def admin():
    # タスク一覧のデータ取得(チャンネル名, 申請者名, 申請日時, 申請内容, 利用目的, ステータス)
    # チャンネル一覧のデータ（チャンネル名）
    return ""

# 管理者アカウント編集画面
@app.route('/admin-edit')
def adminEdit():
    # 管理者情報
    return ""

# ユーザー画面
@app.route('/mypage')
def mypage():
    # ユーザー情報
    # 申請中の一覧
    # 過去の利用歴
    # 通知情報の一覧
    return ""

# 申請フォーム画面
@app.route('/form')
def form():
    # ログイン中のユーザーの情報　※ユーザーDBより「氏名」「メールアドレス」「電話番号」を抽出
    user_name = "申請花子"
    user_email = "shinsei.hanako@gmail.com"
    user_phone_number = "09011111111"
    # チャンネル情報（貸出対象となっている施設や備品の一覧）※チャンネルDBより「チャンネル名」を抽出
    channel_names = ["会議室A","会議室B","会議室C","会議室D","会議室E","体育館","多目的ホール"]
    return render_template('page/application-form.html', channel_names=channel_names, user_name=user_name, user_email=user_email, user_phone_number=user_phone_number)

# POST(処理の呼び出し)
# ログイン処理のルート

# 申請フォームのルート
@app.post('/apply')
def apply():
    # ユーザー情報
    # チャンネル情報
    return ""

# メッセージ投稿のアクション

# チャンネル削除のアクション

# チャンネル追加のアクション

# 管理者アカウント変更アクション

# 申請キャンセルのアクション


@app.errorhandler(404)
def showError404(error):
    """404エラーページの表示"""
    return render_template('error/404.html'),404


@app.errorhandler(500)
def showError500(error):
    """500エラーページの表示"""
    return render_template('error/500.html'),500

# アプリの起動
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)