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