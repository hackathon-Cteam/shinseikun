import uuid
import re
from flask import Flask, request, redirect, render_template, session, flash, abort
from datetime import timedelta
from common.ErrorMessage import ErrorMessage
from model.service.UserService import UserService
from model.service.MessageService import MessageService
from model.service.ChannelService import ChannelService

USER_SERVICE = UserService()
"""ユーザーテーブルにアクセスするクラス"""

MESSAGE_SERVICE = MessageService()
"""メッセージテーブルにアクセスするクラス"""

CHANNEL_SERVICE = ChannelService()
"""チャンネルテーブルにアクセスするクラス"""

PATTERN_MAIL = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
"""メール形式"""

# エラーメッセージ
ERROR_MESSAGE_FOR_FOAM_ENPTY = '空のフォームがあるようです'
"""空のフォームがある場合に表示するエラーメッセージ"""

ERROR_MESSAGE_FOR_SIGNUP_DIFFERENT_PASWORD = '二つのパスワードの値が違っています'
"""登録するパスワードが一致しない場合に表示するエラーメッセージ"""

ERROR_MESSAGE_FOR_SIGNUP_IRREGULAR_MAIL = '正しいメールアドレスの形式ではありません'
"""登録するメール形式が不正な場合に表示するエラーメッセージ"""

ERROR_MESSAGE_FOR_SIGNUP_EXIST = '既に登録されているようです'
"""すでにユーザー登録されている場合に表示するエラーメッセージ"""

ERROR_MESSAGE_FOR_LOGIN_NOT_EXIST = 'このユーザーは存在しません'
"""ユーザー情報がなかった場合に表示するエラーメッセージ"""

ERROR_MESSAGE_FOR_LOGIN_MISTAKE_PASSWORD = 'パスワードが間違っています！'
"""パスワード認証に失敗した場合に表示するエラーメッセージ"""

ERROR_MESSAGE_FOR_ADD_CHANNEL_EXIST = '既に同じ名前のチャンネルが存在しています'
"""すでにチャンネルが存在している場合に表示するエラーメッセージ"""

ERROR_MESSAGE_FOR_DELETE_CHANNEL_NOT_PERMISSION = 'チャンネルは作成者のみ削除可能です'
"""作成者以外がチャンネル削除を実行した場合に表示するエラーメッセージ"""


app = Flask(__name__, static_folder='view/static', template_folder='view/templates')
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)


@app.route('/signup')
def signup():
    """サインアップページの表示"""
    return render_template('registration/signup.html')


@app.post('/signup')
def userSignup():
    """サインアップ処理"""
    name = request.form.get('name')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2') 
    if not name or not email or not password1 or not password2:
        flash(ERROR_MESSAGE_FOR_FOAM_ENPTY)
        return redirect('/signup')
    if password1 != password2:
        flash(ERROR_MESSAGE_FOR_SIGNUP_DIFFERENT_PASWORD)
        return redirect('/signup')
    if re.match(PATTERN_MAIL, email) is None:
        flash(ERROR_MESSAGE_FOR_SIGNUP_IRREGULAR_MAIL)
        return redirect('/signup')
    try:
        userId = uuid.uuid4()
        USER_SERVICE.createNewUser(name, email, password1, userId)
        session['uid'] = str(userId)
        return redirect('/')
    except ValueError as e:
        print(e)
        flash(ERROR_MESSAGE_FOR_SIGNUP_EXIST)
        return redirect('/signup')


@app.route('/login')
def login():
    """ログインページの表示"""
    return render_template('registration/login.html')


@app.post('/login')
def userLogin():
    """ログイン処理"""
    mail = request.form.get('email')
    password = request.form.get('password')
    if not mail or not password :
        flash(ERROR_MESSAGE_FOR_FOAM_ENPTY)
        return redirect('/login')
    try:
        print('call UserService.login.')
        session['uid'] = USER_SERVICE.login(mail, password)
        return redirect('/')
    except ValueError as e:
        print(e)
        if e == ErrorMessage.FAILD_LOGIN_NOT_EXIST:
            flash(ERROR_MESSAGE_FOR_LOGIN_NOT_EXIST)
        elif e == ErrorMessage.FAILD_LOGIN_MISTAKE_PASSWORD:
            flash(ERROR_MESSAGE_FOR_LOGIN_MISTAKE_PASSWORD)
        return redirect('/login')


@app.route('/logout')
def logout():
    """ログアウト処理"""
    session.clear()
    return redirect('/login')


@app.route('/')
def index():
    return render_template('page/chat.html')
    # """チャンネル一覧ページの表示"""
    # userId = session.get('uid')
    # if userId is None:
    #     return redirect('/login')
    # return render_template('index.html', channels = CHANNEL_SERVICE.getChannelList(), uid = userId)


@app.post('/')
def addChannel():
    """チャンネルの追加"""
    userId = session.get('uid')
    if userId is None:
        return redirect('/login')
    try:
        CHANNEL_SERVICE.addChannel(userId, request.form.get('channelTitle'), request.form.get('channelDescription'))
        return redirect('/')
    except ValueError as e:
        print(e)
        render_template('error/error.html', error_message = ERROR_MESSAGE_FOR_ADD_CHANNEL_EXIST)


@app.post('/update_channel')
def updateChannel():
    """チャンネルの更新"""
    userId = session.get('uid')
    if userId is None:
        return redirect('/login')

    channelId = request.form.get('cid')
    CHANNEL_SERVICE.updateChannel(userId, request.form.get('channelTitle'), request.form.get('channelDescription'), channelId)
    return redirect('/detail/{channelId}'.format(channelId = channelId))


# チャンネルの削除
@app.route('/delete/<channelId>')
def deleteChannel(channelId):
    """チャンネルの削除
    
    Args:
    - channelId (String): チャンネルID
    """
    userId = session.get('uid')
    if userId is None:
        return redirect('/login')
    try:
        CHANNEL_SERVICE.deleteChannel(channelId, userId)
        return redirect('/')
    except ValueError as e:
        flash(ERROR_MESSAGE_FOR_DELETE_CHANNEL_NOT_PERMISSION)
        return redirect ('/')


@app.route('/detail/<channelId>')
def detail(channelId):
    """チャンネル詳細ページの表示
    
    Args:
    - channelId (String): チャンネルID
    """
    userId = session.get('uid')
    if userId is None:
        return redirect('/login')
    return render_template(
        'detail.html', messages = MESSAGE_SERVICE.getMessages(channelId), channel = CHANNEL_SERVICE.getChannelById(channelId), uid = userId
    )


@app.post('/message')
def add_message():
    """メッセージの投稿"""
    userId = session.get('uid')
    if userId is None:
        return redirect('/login')
    message = request.form.get('message')
    channelId = request.form.get('cid')
    if message:
        MESSAGE_SERVICE.addMessage(userId, channelId, message)
    return redirect('/detail/{channelId}'.format(channelId = channelId))


@app.post('/delete_message')
def deleteMessage():
    """メッセージの削除"""
    if session.get('uid') is None:
        return redirect('/login')
    messageId = request.form.get('message_id')
    if messageId:
        dbConnect.deleteMessage(messageId)
    return redirect('/detail/{channelId}'.format(channelId = request.form.get('cid')))


@app.errorhandler(404)
def showError404(error):
    """404エラーページの表示"""
    return render_template('error/404.html'),404


@app.errorhandler(500)
def showError500(error):
    """500エラーページの表示"""
    return render_template('error/500.html'),500


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)