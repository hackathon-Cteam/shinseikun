class ChannelEntity:
    """チャンネル情報を保持するEntityクラス"""

    def __init__(self, id, name, overview, description):
        """コンストラクタ
        
        Args:
        * id (String): チャンネルID
        * name (String): チャンネル名
        * overview (String): チャンネル概要
        * description (String): チャンネル説明
        """
        self.id = id
        self.name = name
        self.overview = overview
        self.description = description
