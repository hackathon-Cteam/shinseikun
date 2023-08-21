from Entity.ChannelEntity import ChannelEntity
from Entity.ChatMessageEntity import ChatMessageEntity
from Entity.UserEntity import UserEntity
from Entity.ReserveInfoEntity import ReserveInfoEntity
from Entity. PastUsageEntity import PastUsageEntity
from Entity. InformationEntity import InformationEntity
from flask import Flask, request, redirect, render_template, session, flash, abort
from datetime import timedelta
from jinja2 import Template
import uuid


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
    #user = UserEntity('345', 'NRK', 'rrr@gmail', '', '000-1111-2222', '運動部')
    #applyID = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] #申請ID「チャンネルID*ユーザーID*申請日時」
    #channelss = ["会議室5", "noyamaさん", "2023/08/11/10:30", "予約", "利用目的〇〇〇", "未受領"]
    #channelID = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    #channelnames = ["第１会議室", "第２会議室", "第５講義室", "体育館", "テニスコート"]
    channels = [
        ChannelEntity('ch-123456789', '会議室A', 'よもやまセンター 4F', '少人数用の会議室で数名〜15数名程度を収容できるクローズドな空間です。\n顧客との商談や部署の報告会議、あるいはグループワークや簡易的なブレインストーミングの場として適しています。'),
        ChannelEntity('ch-123456789', '会議室B', 'よもやまセンター 4F', '少人数用の会議室で数名〜15数名程度を収容できるクローズドな空間です。\n顧客との商談や部署の報告会議、あるいはグループワークや簡易的なブレインストーミングの場として適しています。'),
        ChannelEntity('ch-123456789', '会議室C', 'よもやまセンター 4F', '少人数用の会議室で数名〜15数名程度を収容できるクローズドな空間です。\n顧客との商談や部署の報告会議、あるいはグループワークや簡易的なブレインストーミングの場として適しています。'),
        ChannelEntity('ch-123456789', '会議室D', 'よもやまセンター 4F', '少人数用の会議室で数名〜15数名程度を収容できるクローズドな空間です。\n顧客との商談や部署の報告会議、あるいはグループワークや簡易的なブレインストーミングの場として適しています。'),
        ChannelEntity('ch-123456789', '多目的ホール', 'よもやまセンター 4F', '少人数用の会議室で数名〜15数名程度を収容できるクローズドな空間です。\n顧客との商談や部署の報告会議、あるいはグループワークや簡易的なブレインストーミングの場として適しています。'),
        ChannelEntity('ch-123456789', '体育館', 'よもやまセンター 4F', '少人数用の会議室で数名〜15数名程度を収容できるクローズドな空間です。\n顧客との商談や部署の報告会議、あるいはグループワークや簡易的なブレインストーミングの場として適しています。')
    ]
    reserveInfos = [
        ReserveInfoEntity('usr-123456710', 'rsv-123456710', '会議室A', '2024/1/2/12:00', '2024/1/3/14:00', '【利用目的】会議での利用のため', '申請太郎', 'taro.shinsei@gmail.com', '09099999991', '2023/12/1/12:34', '予約', '未受領'),
        ReserveInfoEntity('usr-123456711', 'rsv-123456711', '会議室B', '2024/1/3/12:00', '2024/1/4/14:00', '【利用目的】会議での利用のため', '申請太郎', 'taro.shinsei@gmail.com', '09099999991', '2023/12/1/12:34', '予約', '未受領'),
        ReserveInfoEntity('usr-123456712', 'rsv-123456712', '会議室C', '2024/1/4/12:00', '2024/1/5/14:00', '【利用目的】会議での利用のため', '申請太郎', 'taro.shinsei@gmail.com', '09099999991', '2023/12/1/12:34', '予約', '未受領'),
        ReserveInfoEntity('usr-123456713', 'rsv-123456713', '会議室D', '2024/1/5/12:00', '2024/1/6/14:00', '【利用目的】会議での利用のため', '申請太郎', 'taro.shinsei@gmail.com', '09099999991', '2023/12/1/12:34', '予約', '未受領'),
        ReserveInfoEntity('usr-123456714', 'rsv-123456714', '会議室E', '2024/1/6/12:00', '2024/1/7/14:00', '【利用目的】会議での利用のため', '申請太郎', 'taro.shinsei@gmail.com', '09099999991', '2023/12/1/12:34', '予約', '未受領'),
        ReserveInfoEntity('usr-123456715', 'rsv-123456715', '会議室F', '2024/1/7/12:00', '2024/1/8/14:00', '【利用目的】会議での利用のため', '申請太郎', 'taro.shinsei@gmail.com', '09099999991', '2023/12/1/12:34', '予約', '未受領'),
        ReserveInfoEntity('usr-123456716', 'rsv-123456716', '会議室G', '2024/1/8/12:00', '2024/1/9/14:00', '【利用目的】会議での利用のため', '申請太郎', 'taro.shinsei@gmail.com', '09099999991', '2023/12/1/12:34', '予約', '未受領'),
        ReserveInfoEntity('usr-123456717', 'rsv-123456717', '会議室H', '2024/1/9/12:00', '2024/1/10/14:00', '【利用目的】会議での利用のため', '申請太郎', 'taro.shinsei@gmail.com', '09099999991', '2023/12/1/12:34', '予約', '未受領'),
        ReserveInfoEntity('usr-123456718', 'rsv-123456718', '会議室I', '2024/1/10/12:00', '2024/1/11/14:00', '【利用目的】会議での利用のため', '申請太郎', 'taro.shinsei@gmail.com', '09099999991', '2023/12/1/12:34', '予約', '未受領'),
        ReserveInfoEntity('usr-123456719', 'rsv-123456719', '会議室J', '2024/1/11/12:00', '2024/1/12/14:00', '【利用目的】会議での利用のため', '申請太郎', 'taro.shinsei@gmail.com', '09099999991', '2023/12/1/12:34', '予約', '未受領'),
        ReserveInfoEntity('usr-123456712', 'rsv-123456713', '会議室K', '2024/1/12/12:00', '2024/1/13/14:00', '【利用目的】会議での利用のため', '申請太郎', 'taro.shinsei@gmail.com', '09099999991', '2023/12/1/12:34', '予約', '未受領'),
        ReserveInfoEntity('usr-123456713', 'rsv-123456714', '会議室M', '2024/1/13/12:00', '2024/1/14/14:00', '【利用目的】会議での利用のため', '申請太郎', 'taro.shinsei@gmail.com', '09099999991', '2023/12/1/12:34', '予約', '未受領')
    ]
    return render_template('page/kanrisyagamen.html', channels=channels, reserveInfos=reserveInfos)

    

    # タスク一覧のデータ取得(チャンネル名, 申請者名, 申請日時, 申請内容, 利用目的, ステータス)
    # チャンネル一覧のデータ（チャンネル名）
            

# 管理者アカウント編集画面
#@app.route('/admin-edit')
#def adminEdit():
    # 管理者情報
#    return render_template('page/kanrisya-edit.html')

# ユーザー画面
@app.route('/mypage')
def mypage(): 
    # ユーザー情報
    user = UserEntity('345', 'NRk', 'rrr@gmail', '', '000-1111-2222', '運動部')

    # 申請中の一覧
    print(user.name)
    test= '  '
    reserinfo = ReservationEntity('333', '2023/08/11', '利用予約完了')
    reserinfo2 = ReservationEntity('444', '2023/08/10', 'キャンセル済')
    reserinfo3 = ReservationEntity('555', '2023/09/26', '利用予約申請中')
    
    reserinfo_list = [reserinfo,reserinfo2,reserinfo3]

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

    template_str = """申請ステータスアイコン"""
    template = Template(template_str)

    list_items = ["利用予約完了", "利用予約申請中"]
    print(template.render(list_items=list_items))


    


# 申請フォーム画面
@app.route('/form')
def form():
    # ログイン中のユーザーの情報（ログイン中のユーザーと一致した一件をDBから引用する処理が必要）
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

    # チャンネルDBからチャンネル名を引用（DBManagerのimport必要）
    # try:
    #     with DBManager('channels') as channelDB:
    #         channels = channelDB.getData()
    # except ValueError:
    #     print('エラー')

    return render_template('page/application-form.html', channels=channels, user=user)

# POST(処理の呼び出し)
# ログイン処理のルート

# 申請フォームのルート
@app.post('/apply')
def apply():
    #フォーム要素のname属性の指定により値を取得し変数に代入する(uid,cidの受け渡しも必要??)
    facility = request.form.get('facility')
    year, month, day = request.form.getlist('date')
    start_hour, start_minute, end_hour, end_minute = request.form.getlist('time')
    purpose = request.form.get('purpose')
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')

    #取得したデータの加工
    start_use = year + "-" + month + "-" + day + " " + start_hour + ":" + start_minute
    end_use = year + "-" + month + "-" + day + " " + end_hour + ":" + end_minute
    reserve_data = facility + "//" + start_use + "//" + end_use + "//" + purpose + "//" + name + "//" + email + "//" + phone

    # #データベースへの追加処理（DBManagerのimport必要）
    # with DBManager('reservations') as reservationDB:
    #     reservationDB.addData({id:1, uid:1111, cid:2222})

    #挙動確認用
    return (reserve_data)
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