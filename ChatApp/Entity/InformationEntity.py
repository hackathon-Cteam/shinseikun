class InformationEntity:
    """通知情報一覧を保持するEntityクラス"""

    def __init__(self, id, infor_time, infor_message):
        """コンストラクタ
        
        Args:
        * id (String): ユーザーID
        * infor_time (String):通知受信日
        * infor_message (String):通知の内容メッセージ
        """

        self.id = id
        self.infor_time = infor_time
        self.infor_message = infor_message