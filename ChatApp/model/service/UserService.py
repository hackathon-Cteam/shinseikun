import hashlib
from model.repository.UserRepository import UserRepository
from common.ErrorMessage import ErrorMessage

class UserService:
    """UserDBにアクセスするためのサービスクラス"""

    def createNewUser(self, name, mail, password, userId):
        """新しいユーザー情報を作成する

        Args:
        - name (String): ユーザー名
        - mail (String): メールアドレス
        - password (String): パスワード
        - userId (String): ユーザーID

        Throws: 
        - ValueError: すでにユーザーが登録されていた場合にスロー
        """
        if self.__getUser(mail) is not None:
            print('in error. already registered users')
            raise ValueError(ErrorMessage.FAILD_CREATE_USER)

        UserRepository().addUser(userId, name, mail, self.__hashString(password))

    def login(self, mail, password):
        """ログイン処理
        Args:
        - mail (String): メールアドレス
        - password (String): パスワード

        Return: ユーザー情報

        Throws:
        - ValueError: ユーザー情報がない場合やパスワードが間違っている場合にスロー
        """
        user = self.__getUser(mail)
        if user is None:
            raise ValueError(ErrorMessage.FAILD_LOGIN_NOT_EXIST)

        if self.__hashString(password) != user['password']:
            raise ValueError(ErrorMessage.FAILD_LOGIN_MISTAKE_PASSWORD)

        return user['uid']

    def __getUser(self, mail):
        """ユーザー情報を取得する

        Args:
        - mail (String): メールアドレス

        Return: ユーザー情報
        """
        return UserRepository().getUser(mail)
    
    def __hashString(selr, str):
        """文字列をハッシュ化する
        
        Args:
        - str (String): ハッシュ化する文字列

        Return: ハッシュ化された文字列
        """
        return hashlib.sha256(str.encode('utf-8')).hexdigest()


