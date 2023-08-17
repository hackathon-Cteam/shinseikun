from model.external.DBManager import DBManager
from common.ErrorMessage import ErrorMessage

class ReservationsService:
    """User情報を取得するためのサービスクラス"""

    """DBのチャンネルに関するテーブル名"""
    RESERVATION_DB = 'reservations'