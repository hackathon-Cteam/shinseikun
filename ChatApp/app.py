from Entity.ChannelEntity import ChannelEntity
from Entity.ChatMessageEntity import ChatMessageEntity
from Entity.UserEntity import UserEntity
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
    # チャンネル情報
    channel = ChannelEntity('ch-123456789', '会議室', 'よもやまセンター 4F', '少人数用の会議室で数名〜15数名程度を収容できるクローズドな空間です。\n顧客との商談や部署の報告会議、あるいはグループワークや簡易的なブレインストーミングの場として適しています。')
    # メッセージ情報のリスト
    messages = [
        ChatMessageEntity('ユーザー名', 'user', '申請内容(自動メッセージ)', '2023/07/01T10:00'),
        ChatMessageEntity('管理者', 'admin', '申請承認(自動メッセージ)', '2023/07/01T11:30'),
        ChatMessageEntity('管理者', 'admin', 'ご利用ありがとうございました！', '2023/07/07T15:00'),
        ChatMessageEntity('ユーザー名', 'user', 'とても良かったです！', '2023/07/07T18:00'),
        ChatMessageEntity('ユーザー名', 'user', 'クァw瀬drftgyふじこlp；＠', '2023/07/07T22:00'),
    ]

    return render_template('page/chat.html', channel= channel, messages= messages)

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
    # ログイン中のユーザーの情報　
    user = UserEntity('usr-123456789', '申請花子', 'shinsei@gmail.com', 'User12345', '09012345678', 'グループA')
    # チャンネル情報
    channels = [
        ChannelEntity('ch-123456789', '会議室A', 'よもやまセンター 4F', '少人数用の会議室で数名〜15数名程度を収容できるクローズドな空間です。\n顧客との商談や部署の報告会議、あるいはグループワークや簡易的なブレインストーミングの場として適しています。'),
        ChannelEntity('ch-123456789', '会議室B', 'よもやまセンター 4F', '少人数用の会議室で数名〜15数名程度を収容できるクローズドな空間です。\n顧客との商談や部署の報告会議、あるいはグループワークや簡易的なブレインストーミングの場として適しています。'),
        ChannelEntity('ch-123456789', '会議室C', 'よもやまセンター 4F', '少人数用の会議室で数名〜15数名程度を収容できるクローズドな空間です。\n顧客との商談や部署の報告会議、あるいはグループワークや簡易的なブレインストーミングの場として適しています。'),
        ChannelEntity('ch-123456789', '会議室D', 'よもやまセンター 4F', '少人数用の会議室で数名〜15数名程度を収容できるクローズドな空間です。\n顧客との商談や部署の報告会議、あるいはグループワークや簡易的なブレインストーミングの場として適しています。'),
        ChannelEntity('ch-123456789', '多目的ホール', 'よもやまセンター 4F', '少人数用の会議室で数名〜15数名程度を収容できるクローズドな空間です。\n顧客との商談や部署の報告会議、あるいはグループワークや簡易的なブレインストーミングの場として適しています。'),
        ChannelEntity('ch-123456789', '体育館', 'よもやまセンター 4F', '少人数用の会議室で数名〜15数名程度を収容できるクローズドな空間です。\n顧客との商談や部署の報告会議、あるいはグループワークや簡易的なブレインストーミングの場として適しています。')
    ]
    return render_template('page/application-form.html', channels=channels, user=user)

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