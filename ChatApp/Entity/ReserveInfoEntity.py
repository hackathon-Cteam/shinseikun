class ReserveInfoEntity:
    """申請情報を保持するEntityクラス"""

    def __init__(
            self,
            userId,
            rsvId,
            cid,
            channelName,
            useDate,
            rsvPurpose,
            rsvUserName,
            status
        ):
        """コンストラクタ
        
        Args:
        * userId (String): 申請をしたユーザーのID
        * rsvId (String): 申請ID
        * cid (String): チャンネルID
        * channelName (String): 申請対象のチャンネル（施設等）の名称
        * userDate (String): 予約時間
        * rsvPurpose (String): 利用目的
        * rsvUserName (String): 申請者（当日の利用者）の名前
        * status (String): 申請受理のステータス（未受領or受領or承認or否認等）
        """
        self.userId = userId
        self.rsvId = rsvId
        self.cid = cid
        self.channelName = channelName
        self.useDate = useDate
        self.rsvPurpose = rsvPurpose
        self.rsvUserName = rsvUserName
        self.status = status
        