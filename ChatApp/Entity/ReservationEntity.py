class ReservationEntity:
    """申請情報を保持するEntityクラス"""

    def __init__(self, id, reserve_time, message):
        """コンストラクタ
        
        Args:
        * id (String): ユーザーID
        * reserve_time(String):メッセージ受信した日
        * message(String):申請状況についてのメッセージ
        """

        self.id = id
        self.reserve_time = reserve_time
        self.message = message