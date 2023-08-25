class ChatMessageEntity:
    """チャットメッセージ情報を保持するEntityクラス"""

    def __init__(self, id, senderName, senderType, text, date):
        """コンストラクタ
        
        Args:
        * senderName (String): 投稿者名
        * senderType (String): 投稿者のタイプ(admin or user)
        * text (String): メッセージテキスト
        * date (String): 投稿日時
        """
        self.id = id
        self.senderName = senderName
        self.senderType = senderType
        self.text= text
        self.date = date
