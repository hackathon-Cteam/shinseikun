from Entity.ChannelEntity import ChannelEntity
from Entity.ChatMessageEntity import ChatMessageEntity
from Entity.UserEntity import UserEntity
from Entity.ReserveInfoEntity import ReserveInfoEntity
from Entity. PastUsageEntity import PastUsageEntity
from Entity. InformationEntity import InformationEntity
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
    return render_template('/page/login.html')

# チャンネル一覧ページのルート
@app.route('/')
@app.route('/channel_list')
def channel_list():
    # チャンネル名の一覧を取得
    # チャンネルID
    # 画像データの情報（データ名とか）
    # チャンネル名とIDが紐づいた形式のデータ
    channels = [
        ChannelEntity('ch-123', '会議室1', 'よもやまセンター 4F', 'kaigi.jpg'),
        ChannelEntity('ch-456', '会議室2', '新ビル 2F', 'kaigi.jpg'),
        ChannelEntity('ch-789', '体育館', 'グラウンド西', 'gym.jpg'),
        ChannelEntity('ch-246', 'テニス', 'グラウンド東', 'tennis.jpg'),
    ]
    
    return render_template('/page/channel_list.html',channels=channels)


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
    return render_template('page/chat.html', userType= 'admin', channel= channel, messages= messages)

# 管理者画面のルート
@app.route('/admin')
def admin():
    # ユーザー情報
    user = UserEntity('345', 'NRK', 'rrr@gmail', '', '000-1111-2222', '運動部')
    applyID = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] #申請ID「チャンネルID*ユーザーID*申請日時」
    #channelss = ["会議室5", "noyamaさん", "2023/08/11/10:30", "予約", "利用目的〇〇〇", "未受領"]
    channelID = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    channelnames = ["第１会議室", "第２会議室", "第５講義室", "体育館", "テニスコート"]
    channels = [
        ChannelEntity('ch-123456789', '会議室A', 'よもやまセンター 4F', '少人数用の会議室で数名〜15数名程度を収容できるクローズドな空間です。\n顧客との商談や部署の報告会議、あるいはグループワークや簡易的なブレインストーミングの場として適しています。'),
        ChannelEntity('ch-123456789', '会議室B', 'よもやまセンター 4F', '少人数用の会議室で数名〜15数名程度を収容できるクローズドな空間です。\n顧客との商談や部署の報告会議、あるいはグループワークや簡易的なブレインストーミングの場として適しています。'),
        ChannelEntity('ch-123456789', '会議室C', 'よもやまセンター 4F', '少人数用の会議室で数名〜15数名程度を収容できるクローズドな空間です。\n顧客との商談や部署の報告会議、あるいはグループワークや簡易的なブレインストーミングの場として適しています。'),
        ChannelEntity('ch-123456789', '会議室D', 'よもやまセンター 4F', '少人数用の会議室で数名〜15数名程度を収容できるクローズドな空間です。\n顧客との商談や部署の報告会議、あるいはグループワークや簡易的なブレインストーミングの場として適しています。'),
        ChannelEntity('ch-123456789', '多目的ホール', 'よもやまセンター 4F', '少人数用の会議室で数名〜15数名程度を収容できるクローズドな空間です。\n顧客との商談や部署の報告会議、あるいはグループワークや簡易的なブレインストーミングの場として適しています。'),
        ChannelEntity('ch-123456789', '体育館', 'よもやまセンター 4F', '少人数用の会議室で数名〜15数名程度を収容できるクローズドな空間です。\n顧客との商談や部署の報告会議、あるいはグループワークや簡易的なブレインストーミングの場として適しています。')
    ]
    return render_template('page/kanrisyagamen.html', channels=channels, user=user, applyID=applyID, channelID=channelID, channelnames=channelnames)

    

    # タスク一覧のデータ取得(チャンネル名, 申請者名, 申請日時, 申請内容, 利用目的, ステータス)
    # チャンネル一覧のデータ（チャンネル名）
            

# 管理者アカウント編集画面
@app.route('/admin-edit')
def adminEdit():
    # 管理者情報
    return render_template('page/kanrisya-edit.html')

# ユーザー画面
@app.route('/mypage')
def mypage(): 
    # ユーザー情報
    user = UserEntity('345', 'NRk', 'rrr@gmail', '', '000-1111-2222', '運動部')

    # 申請中の一覧
    print(user.name)
    test= '  '
    reserinfo = ReservationEntity('333', '2023/08/11', '利用予約完了')
    reserinfo2 = ReservationEntity('444', '2023/08/10', '予約キャンセル')
    
    reserinfo_list = [reserinfo,reserinfo2]

    # 過去の利用歴
    past = PastUsageEntity('777','2022/6/2','キャンセル済')
    past2 = PastUsageEntity('888','2022/4/2','ご利用済')
    past3 = PastUsageEntity('999','2022/3/2','キャンセル済')
    past4 = PastUsageEntity('123','2022/2/2','ご利用済')

    past_list = [past,past2,past3,past4]

    # 通知情報の一覧

    information = InformationEntity('111','2023/8/24','第一体育館修理のため休館のお知らせ')
    information2 = InformationEntity('111','2023/8/24','第一体育館修理のため休館のお知らせ')
    information3 = InformationEntity('111','2023/8/24','第一体育館修理のため休館のお知らせ')

    information_list = [information,information2,information3]


    return render_template('/page/mypage.html',test=test, user=user, reserinfo_list= reserinfo_list, past_list=past_list, information_list=information_list)

    


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
    test = "申請しました"
        # #下記のように、フォーム要素のname属性から値を取得し変数に代入する
        # test = request.form.get('test')
        # test2 = request.form.get('test2')
        # test3 = request.form.get('test3')

        # #下記のように、変数に代入した値をDBに格納する処理を行う
        # post = Post(test=test, test2=test2, test3=test3)
        # dbConnect.Test(post)
    return (test)
    # return redirect ('/mypage')    #マイページにリダイレクト（あとから有効化する）
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