class UserEntity:
    """ユーザー情報を保持するEntityクラス"""

    def __init__(self, id, name, email, password, phone, group):
        """コンストラクタ
        
        Args:
        * id (String): ユーザーID
        * name (String): ユーザー氏名
        * email (String): ユーザーメールアドレス
        * password (String): ユーザーメールアドレス
        * phone (String): ユーザー電話番号
        * group (String): ユーザー所属
        """
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        self.group = group