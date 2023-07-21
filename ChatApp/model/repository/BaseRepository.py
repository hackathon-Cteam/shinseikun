import pymysql

class BaseRepository:
    """リポジトリのベースクラス"""

    FORMAT_SQL_INSERT_INTO = 'INSERT INTO {} ({}) VALUES ({});'
    FORMAT_SQL_SELECT = 'SELECT {} FROM {};'
    FORMAT_SQL_SELECT_WHERE = 'SELECT {} FROM {} WHERE {};'
    FORMAT_SQL_UPDATE_WHERE = "UPDATE {} SET {} WHERE {};"
    FORMAT_SQL_DELETE_WHERE = "DELETE FROM {} WHERE {};"
    COLUMN_ALL = '*'

    def __init__(self):
        """コンストラクタ"""
        try:
            self.connection = pymysql.connect(host = "db", db = "chatapp", user = "testuser", password = "testuser",
                charset = "utf8", cursorclass = pymysql.cursors.DictCursor
            )
        except (ConnectionError):
            print("コネクションエラーです")
