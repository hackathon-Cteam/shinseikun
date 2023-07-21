from model.repository.MessageRepository import MessageRepository

class MessageService:
    """Messageテーブルにアクセスするためのクラス"""

    def getMessages(self, channelId):
        """チャンネルに投稿された全てのメッセージ情報を取得する
        
        Args:
        - channelId (*): チャンネルID

        Return: 全メッセージ情報
        """
        return MessageRepository().getMessageAll(channelId)

    def addMessage(selr, userId, channelId, message):
        """メッセージ情報を追加する

        Args:
        - userId (String): ユーザーID
        - channelId (String): チャンネルID
        - message (String): メッセージ
        """
        MessageRepository().addMessage(userId, channelId, message)

    def deleteMessage(self, messageId):
        """メッセージ情報を削除する
        
        Args:
        - messageID (String): メッセージID
        """
        MessageRepository().deleteMessage(messageId)