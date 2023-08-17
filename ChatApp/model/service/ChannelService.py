from model.external.DBManager import DBManager
from common.ErrorMessage import ErrorMessage

class ChannelService :
    """チャンネルに関する情報を取得するサービスクラス"""

    """DBのチャンネルに関するテーブル名"""
    CHANNEL_DB = 'channels'