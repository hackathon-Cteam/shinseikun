class PastUsageEntity:
    """過去利用歴を保持するEntityクラス"""

    def __init__(self, id, past_usege, result):
        """コンストラクタ
        
        Args:
        * id (String): ユーザーID
        * past_usege:過去に予約した日時
        * result:利用したかキャンセルしたかについての結果記録
        """

        self.id = id
        self.past_usege = past_usege
        self.result = result