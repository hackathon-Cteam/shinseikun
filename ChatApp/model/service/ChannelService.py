from common.ErrorMessage import ErrorMessage
from model.repository.ChannelRepository import ChannelRepository

class ChannelService :
    """チャンネルテーブルにアクセスするためのクラス"""

    def getChannelList(self):
        """チャンネル一覧を取得する
        
        Return: チャンネル情報
        """
        return ChannelRepository().getChannelAll().reverse()

    def addChannel(self, userId, name, description):
        """チャンネルを追加する

        Args:
        - userId (String): ユーザーID
        - name (String): チャンネル名
        - description (String): チャンネルについての説明

        Throws:
        - ValueError: 指定されたチャンネル名ですでにチャンネル情報があった場合にスロー
        """
        if self.__getChannelByName(name):
            raise ValueError(ErrorMessage.FAILD_ADD_CHANNEL_ALREADY_EXIST)
        ChannelRepository().addChannel(userId, name, description)


    def updateChannel(self, userId, name, description, channelId):
        """チャンネルを更新する
        
        Args:
        - userId (String): ユーザーID
        - name (String): チャンネル名
        - description (String): チャンネルについての説明
        - channelId (String): チャンネルID
        """
        ChannelRepository().updateChannel(userId, name, description, channelId)

    def deleteChannel(self, channelId, userId):
        """チャンネルを削除する
        
        Args:
        - channelId (String): チャンネルID
        - userId (String): ユーザーID

        Throws:
        - ValueError: チャンネルを作成したユーザー以外が削除を実行した場合にスロー
        """
        if self.getChannelById(channelId)['uid'] != userId:
            raise ValueError(ErrorMessage.FAILD_DELETE_CHANNEL_NOT_PERMISSION)
        ChannelRepository().deleteChannel(channelId)


    def getChannelById(self, id):
        """指定されたチャンネル名のチャンネル情報を取得する

        Args:
        - id (String): チャンネルID

        Return: チャンネル情報
        """
        return ChannelRepository().getChannelById(id)

    def __getChannelByName(self, name):
        """指定されたチャンネル名のチャンネル情報を取得する

        Args:
        - name (String): チャンネル名

        Return: チャンネル情報
        """
        return ChannelRepository().getChannelByName(name)

    def __getChannelAll():
        """全チャンネル情報を取得する
        
        Return: 全チャンネル情報
         """
        return ChannelRepository().getChannelAll()