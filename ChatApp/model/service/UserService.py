from model.external.DBManager import DBManager
from common.ErrorMessage import ErrorMessage

class UserService:
    """User情報を取得するためのサービスクラス"""

    """DBのチャンネルに関するテーブル名"""
    USER_DB = 'users'