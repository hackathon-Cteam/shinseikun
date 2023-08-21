from Entity.ChannelEntity import ChannelEntity
from Entity.ChatMessageEntity import ChatMessageEntity
from Entity.UserEntity import UserEntity
from Entity.ReserveInfoEntity import ReserveInfoEntity
from Entity. PastUsageEntity import PastUsageEntity
from Entity. InformationEntity import InformationEntity
from common.util.DataTimeConverter import DataTimeConverter
from flask import Flask, request, redirect, render_template, session, flash, abort
from datetime import timedelta
import uuid

from model.external.DBManager import DBManager # TODO: コンフリクトするので削除予定

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
@app.route('/talk/<channelId>')
def talk(channelId):
    channel = None
    with DBManager('channels') as channelDB:
        channel = channelDB.getDataByColumns(['id', 'name', 'overview', 'description'], f'id="{channelId}"')[0]

    messages = None
    with DBManager('messages') as messageDB:
        messages = messageDB.getData(f'cid="{channelId}"')

    userList = None
    with DBManager('users') as usersDB:
        userList = usersDB.getDataByColumns(['uid', 'user_name', 'user_type'])
    
    chatList = []
    for message in messages:
        user = list(filter(lambda user : user['uid'] == message['uid'], userList))[0]
        chatList.append(
            ChatMessageEntity(message['id'], user['user_name'], user['user_type'], message['message'], DataTimeConverter.convertStr(message['created_at']))
        )

    return render_template(
        'page/chat.html', userType= 'admin', channel= ChannelEntity(channel['id'], channel['name'], channel['overview'], channel['description'], ''), messages= chatList
    )


# 管理者画面のルート
@app.route('/admin')
def admin():
    channels = None
    with DBManager('channels') as channelDB:
        channels = channelDB.getData()

    userList = None
    with DBManager('users') as usersDB:
        userList = usersDB.getData()

    channelList = []
    for channel in channels:
        channelList.append(ChannelEntity(channel['id'], channel['name'], channel['overview'], channel['description'], channel['img']))
    
    reservations = None
    with DBManager('reservations') as reservationDB:
        reservations = reservationDB.getData()

    # TODO: htmlに予約情報が反映できる状態になったらテンプレートへ渡すようにする
    reservationList = []
    for reservation in reservations:
        user = list(filter(lambda user : user['uid'] == reservation['uid'], userList))[0]
        channel = list(filter(lambda channel : channel['cid'] == reservation['cid'], channelList))[0]

        status = '承認' if reservation['approval_at'] is None else 'キャンセル' if reservation['cancel_at'] is None else '受領'
        # TODO: 渡す情報をもっと絞ってもいいかもしれない。htmlはまだ未反映なので必要な情報が不明確
        reservationList.append(ReserveInfoEntity(
            user['uid'], reservation['id'], channel['name'], DataTimeConverter.convertStr(reservation['start_use']), DataTimeConverter.convertStr(reservation['end_use']),
            reservation['purpose'], user['name'], user['email'], user['phone'],  DataTimeConverter.convertStr(reservation['created_at']), '', status
        ))

    return render_template('page/kanrisyagamen.html', channels=channelList, userType= 'admin')


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
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':    #POSTメソッド（フォーム送信）であれば

        # #下記のように、フォーム要素のname属性から値を取得し変数に代入する
        # test = request.form.get('test')
        # test2 = request.form.get('test2')
        # test3 = request.form.get('test3')

        # #下記のように、変数に代入した値をDBに格納する処理を行う
        # post = Post(test=test, test2=test2, test3=test3)
        # dbConnect.Test(post)

        return redirect('/mypage')    #マイページにリダイレクト

    else:    #GETメソッド（申請フォームページ読み込み）であれば
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
        # 申請情報（※ReserveInfoEntity適用のテストのため、後で削除）
        reserveInfo = ReserveInfoEntity('usr-123456789', 'rsv-123456789', '会議室A', '2024/1/1/12:00', '2024/1/1/14:00', '【利用目的】会議での利用のため', '申請太郎', 'taro.shinsei@gmail.com', '09099999999', '2023/12/1/12:34', '予約', '未受領')

        return render_template('page/application-form.html', channels=channels, user=user, reserveInfo=reserveInfo)

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