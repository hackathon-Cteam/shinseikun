import json
from Entity.ChannelEntity import ChannelEntity
from Entity.ChatMessageEntity import ChatMessageEntity
from Entity.ReservationEntity import ReservationEntity
from Entity.UserEntity import UserEntity
from Entity.ReserveInfoEntity import ReserveInfoEntity
from Entity. PastUsageEntity import PastUsageEntity
from Entity. InformationEntity import InformationEntity
from common.util.DataTimeConverter import DataTimeConverter
from flask import Flask, request, redirect, render_template, session, flash, abort, Response
from datetime import timedelta
import uuid

from model.external.DBManager import DBManager

# アプリの設定
app = Flask(__name__, static_folder='view/static', template_folder='view/templates')
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)

# 画面表示の呼び出し


# ログイン画面のルート
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form.get('userid')
        password = request.form.get('password')
        
        
        with DBManager('users') as userDB:
            users = userDB.getData()
            
        for user in users:
            uid = user['uid']
            pass_word = user['password']
            
        if userid == uid and password == pass_word:
            user_id = str(uuid.uuid4())  # ランダムなユーザーIDを生成
            session['uid'] = user_id  # セッションにユーザー情報を保存
            return redirect(url_for('index'))
        else:
            return "Invalid credentials. Please try again."  # 画面にエラーを表示して再入力を促すよう修正したい

    return render_template('/page/login.html')


# ログアウト
@app.route('/logout')
def logout():
    session.clear()
    return redirect('login')


# チャンネル一覧ページのルート
@app.route('/')
def index():
    uid = session.get('uid')
    if uid is None:
        return redirect('/login')
    else:
        try:
            with DBManager('channels') as channelDB:
                channels = channelDB.getData()
        except ValueError:
            print('エラー')
       
        return render_template('/page/channel_list.html',channels=channels)

# サインアップ
@app.route('/signup',methods=['POST'])
def signup():
    name = request.form.get('name')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    
    # user_data = {
    #     'uid': ,
    #     'user_name': name,
    #     'email': email,
    #     'password': password1
    #     'phone': ,  
    #     'user_type': ,  
    #     'group_name': ,  
    #     'created_at': 
    # }
    
    # with DBManager('users') as userDB:
    #     userDB.addData(user_data)
    
    # 仮でユーザー情報をセッションに保存 
    session['new_user_info'] = {
        'name': name,
        'email': email,
        'password1': password1,
        'password2': password2
    }
    
    user_id = str(uuid.uuid4())  # ランダムなユーザーIDを生成
    session['uid'] = user_id  # セッションにユーザー情報を保存
    return redirect('/')


# チャット画面ルート
@app.route('/talk/<channelId>')
def talk(channelId):
    channel = None
    with DBManager('channels') as channelDB:
        channel = channelDB.getDataByColumns(['id', 'name', 'overview', 'description'], f'id="{channelId}"')[0]

    messages = None
    with DBManager('messages') as messageDB:
        messages = messageDB.getData(f'cid="{channelId}"')

    users = None
    with DBManager('users') as usersDB:
        users = usersDB.getDataByColumns(['uid', 'user_name', 'user_type'])
    
    chatList = []
    for message in messages:
        user = list(filter(lambda user : user['uid'] == message['uid'], users))[0]
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

    users = None
    with DBManager('users') as usersDB:
        users = usersDB.getData()

    channelList = []
    for channel in channels:
        channelList.append(ChannelEntity(channel['id'], channel['name'], channel['overview'], channel['description'], channel['img']))
    
    reservations = None
    with DBManager('reservations') as reservationDB:
        reservations = reservationDB.getData()

    reservationList = []
    for reservation in reservations:
        user = list(filter(lambda user : user['uid'] == reservation['uid'], users))[0]
        channel = list(filter(lambda channel : channel['id'] == reservation['cid'], channels))[0]

        status = 'キャンセル' if reservation['cancel_at'] is not None else '承認' if reservation['approval_at'] is not None else '受領' if reservation['received_at'] is not None else '未受領'
        reservationList.append(ReserveInfoEntity(
            user['uid'], reservation['id'], channel['id'], channel['name'], f'{DataTimeConverter.convertStr(reservation["start_use"])}〜{DataTimeConverter.convertStr(reservation["end_use"])}',
            reservation['purpose'], user['user_name'], status
        ))

    return render_template('page/kanrisyagamen.html', channels= channelList, userType= 'admin', reserveInfos= reservationList)


# 管理者アカウント編集画面
#@app.route('/admin-edit')
#def adminEdit():
    # 管理者情報
#    return render_template('page/kanrisya-edit.html')


# ユーザー画面
@app.route('/mypage/<userId>')
def mypage(userId):
    # TODO: userIDはリクエストurlに含めるようにする
    userId = '970af84c-dd40-47ff-af23-282b72b7cca8'
    # ユーザー情報
    userInfo = None
    with DBManager('users') as usersDB:
        user = usersDB.getData(f'uid="{userId}"')[0]
        userInfo = UserEntity(user['uid'], user['user_name'], user['email'], user['password'], user['phone'], user['group_name'])

    channels = None
    with DBManager('channels') as channelDB:
        channels = channelDB.getDataByColumns(['id', 'name'])

    # 申請中の一覧
    reservations = None
    with DBManager('reservations') as reservationDB:
        reservations = reservationDB.getData(f'uid="{userId}"')

    reserinfo_list = []
    past_list = []
    if reservations:
        reservations.sort(key= lambda reserinfo: reserinfo['start_use'])
        for reservation in reservations:
            targetName = list(filter(lambda channel : channel['id'] == reservation['cid'], channels))[0]['name']
            cancelDate = reservation['cancel_at']
            # 過去の利用歴
            if DataTimeConverter.createDatetimeNow() > reservation['end_use']:
                past_list.append(PastUsageEntity(reservation['id'], DataTimeConverter.convertStr(reservation['created_at']), f'{targetName}を利用しました' if cancelDate is None else f'{targetName}をキャンセルしました'))
                continue

            # 申請情報
            reserinfo_list.append(ReservationEntity(
                reservation['id'],
                f'{DataTimeConverter.convertStr(reservation["start_use"])}〜{DataTimeConverter.convertStr(reservation["end_use"])} {targetName}',
                'キャンセル済' if reservation['cancel_at'] is not None else '利用予約完了' if reservation['approval_at'] is not None else '利用予約申請中',
                reservation['cid'],
            ))

    # 通知情報の一覧
    information = InformationEntity('111','2023/8/24','第一体育館修理のため休館のお知らせ')
    information2 = InformationEntity('111','2023/8/24','第一体育館修理のため休館のお知らせ')
    information3 = InformationEntity('111','2023/8/24','第一体育館修理のため休館のお知らせ')

    information_list = [information,information2,information3]

    return render_template('/page/mypage.html', userType= 'user', user= userInfo, reserinfo_list= reserinfo_list, past_list= past_list, information_list=information_list)


# 申請フォーム画面
@app.route('/form')
def form():
    # チャンネル情報
    channels = None
    with DBManager('channels') as channelDB:
        channels = channelDB.getData()

    channelList = []
    for channel in channels:
        channelList.append(ChannelEntity(channel['id'], channel['name'], channel['overview'], channel['description'], channel['img']))

    # TODO: userIDはリクエストurlに含めるようにする(？)
    userId = '970af84c-dd40-47ff-af23-282b72b7cca8'
    # ユーザー情報
    userInfo = None
    with DBManager('users') as usersDB:
        user = usersDB.getData(f'uid="{userId}"')[0]
        userInfo = UserEntity(user['uid'], user['user_name'], user['email'], user['password'], user['phone'], user['group_name'])

    return render_template('page/application-form.html', channels=channelList, user=userInfo)

# POST(処理の呼び出し)
# ログイン処理のルート

# 申請フォームのルート
@app.post('/apply')
def apply():
    # TODO: userIDはリクエストurlに含めるようにする(？)
    userId = '970af84c-dd40-47ff-af23-282b72b7cca8'
    cid = request.form.get('facility')
    year, month, day = request.form.getlist('date')
    start_hour, start_minute, end_hour, end_minute = request.form.getlist('time')
    purpose = request.form.get('purpose')
    name = request.form.get('name')    #当日の利用者名（フォームで編集された場合は、ログイン中のユーザー名とイコールでない）
    email = request.form.get('email')    #当日の利用者のメールアドレス（フォームで編集された場合は、ログイン中のユーザーのメールアドレスとイコールでない）
    phone = request.form.get('phone')    #当日の利用者の電話番号（フォームで編集された場合は、ログイン中のユーザーの電話番号とイコールでない）

    #日時データの加工（かわりにDataTimeConverterが使えるか？）
    start_use = year + "-" + month + "-" + day + " " + start_hour + ":" + start_minute + ":00"
    end_use = year + "-" + month + "-" + day + " " + end_hour + ":" + end_minute +":00"
    # reserve_data = cid + "//" + start_use + "//" + end_use + "//" + purpose + "//" + name + "//" + email + "//" + phone

    #reservationデータベースへの追加処理
    try:
        with DBManager('reservations') as reservationDB:
            reservationDB.addData({ 'uid': userId, 'cid': cid, 'purpose': purpose, 'start_use': start_use , 'end_use': end_use })
        return redirect ('/mypage/<userId>')    #マイページにリダイレクト
    except  Exception as error:
        return Response(response= json.dumps({'message': error}), status= 500)

# メッセージ投稿のアクション
@app.post('/post-message')
def postMessage():
    # TODO: userIDはセッション情報から取得する予定
    userId = '970af84c-dd40-47ff-af23-282b72b7cca8'
    try:
        with DBManager('messages') as messageDB:
            messageDB.addData({ 'uid': userId, 'cid': request.json['channelId'], 'message': request.json['message'] })
        return Response(response= json.dumps({'message': 'successfully posted'}), status= 200)
    except  Exception as error:
        return Response(response= json.dumps({'message': error}), status= 500)


# メッセージ削除
@app.post('/delete-message')
def deleteMessage():
    try:
        with DBManager('messages') as messageDB:
            messageDB.deleteData(f'id={request.json["messageId"]}')
        return Response(response= json.dumps({'message': 'successfully deleted'}), status= 200)
    except  Exception as error:
        return Response(response= json.dumps({'message': error}), status= 500)

# チャンネル削除のアクション
@app.post('/delete-channel')
def deleteChannel():
    try:
        with DBManager('channels') as channelDB:
            channelDB.deleteData(f'id={request.json["channelId"]}')
        return Response(response= json.dumps({'message': 'successfully deleted'}), status= 200)
    except  Exception as error:
        return Response(response= json.dumps({'message': error}), status= 500)

# チャンネル追加のアクション
@app.post('/add-channel')
def addChannel():
    try:
        with DBManager('channels') as channelDB:
            channelDB.addData({
                'name': request.json["channelName"],
                'overview': f'{request.json["channelName"]}についてはお問い合わせください。',
                'description': f'{request.json["channelName"]}の詳細についてはお問い合わせください。', 'img': 'no-img.jpg'
            })
            cid = channelDB.getDataByColumns('id', f'name="{request.json["channelName"]}"')[0]['id']
        return Response(response= json.dumps({'channelId': cid }), status= 200)
    except  Exception as error:
        return Response(response= json.dumps({'message': error}), status= 500)


# 管理者アカウント変更アクション
# 申請受領のアクション
@app.post('/received-reservation')
def receivedReservation():
    try:
        with DBManager('reservations') as reservationDB:
            reservationDB.updateData({ 'received_at': DataTimeConverter.createDatetimeNow()}, f'id={request.json["reserinfoId"]}')
        return Response(response= json.dumps({'message': 'successfully received'}), status= 200)
    except  Exception as error:
        return Response(response= json.dumps({'message': error}), status= 500)
    

# 申請承認のアクション
@app.post('/approval-reservation')
def approvalReservation():
    try:
        with DBManager('reservations') as reservationDB:
            reservationDB.updateData({ 'approval_at': DataTimeConverter.createDatetimeNow()}, f'id={request.json["reserinfoId"]}')
        return Response(response= json.dumps({'message': 'successfully approval'}), status= 200)
    except  Exception as error:
        return Response(response= json.dumps({'message': error}), status= 500)


# 申請キャンセルのアクション
@app.post('/cancel-reservation')
def cancelReservation():
    try:
        with DBManager('reservations') as reservationDB:
            reservationDB.updateData({ 'cancel_at': DataTimeConverter.createDatetimeNow()}, f'id={request.json["reserinfoId"]}')
        return Response(response= json.dumps({'message': 'successfully cancel'}), status= 200)
    except  Exception as error:
        return Response(response= json.dumps({'message': error}), status= 500)

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