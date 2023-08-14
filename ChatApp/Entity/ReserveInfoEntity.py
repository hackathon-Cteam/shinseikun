class ReserveInfoEntity:
    """申請情報を保持するEntityクラス"""

    def __init__(
            self,
            userId,
            rsvId,
            channelName,
            rsvTimeStart,
            rsvTimeEnd,
            rsvPurpose,
            rsvUserName,
            rsvUserEmail,
            rsvUserPhone,
            submitTime,
            category,
            status
        ):
        """コンストラクタ
        
        Args:
        * userId (String): ユーザー（ログイン中のユーザー）のID
        * rsvId (String): 申請ID
        * channelName (String): 申請対象のチャンネル（施設等）の名称
        * rsvTimeStart (String): 予約時間（開始時間）
        * rsvTimeEnd (String): 予約時間（終了時間）
        * rsvPurpose (String): 利用目的
        * rsvUserName (String): 申請者（当日の利用者）の名前
        * rsvUserEmail (String): 申請者（当日の利用者）のメールアドレス
        * rsvUserPhone (String): 申請者（当日の利用者）の電話番号
        * submitTime (String): タイムスタンプ（申請の送信日時）
        * category (String): 申請の区分（予約orキャンセル等）
        * status (String): 申請受理のステータス（未受領or受領or承認or否認等）
        """
        self.userId = userId
        self.rsvId = rsvId
        self.channelName = channelName
        self.rsvTimeStart = rsvTimeStart
        self.rsvTimeEnd = rsvTimeEnd
        self.rsvPurpose = rsvPurpose
        self.rsvUserName = rsvUserName
        self.rsvUserEmail = rsvUserEmail
        self.rsvUserPhone = rsvUserPhone
        self.submitTime = submitTime
        self.category = category
        self.status = status
        