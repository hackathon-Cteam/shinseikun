class User:
    """ユーザークラス"""

    def __init__(self, uid, name, email, password):
        """コンストラクタ
        
        Args:
        - uid (String): ユーザーID
        - name (String): ユーザー名
        - email (String): メールアドレス
        - password (String): パスワード
        """
        self.uid = uid
        self.name = name
        self.email = email
        self.password = password

    # 以下getter
    def getUid(self):
        return self.uid

    def getUserName(self):
        return self.name

    def getUserEmail(self):
        return self.email
    
    def getUserPassword(self):
        return self.password
    
