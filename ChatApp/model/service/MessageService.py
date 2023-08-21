from Entity.ChatMessageEntity import ChatMessageEntity
from model.external.DBManager import DBManager
from model.repository.MessageRepository import MessageRepository

class MessageService:
    """Message情報を取得するためのクラス"""

    """DBのチャンネルに関するテーブル名"""
    MESSAGE_DB = 'messages'