import pymysql

class DBManager:
    """データベースを操作するクラス"""

    def __init__(self, tableName):
        """コンストラクタ

        DBManagerを生成した段階でDBへの接続をスタートする

        DBManagerはwith文を使ってDBへの接続を自動的にクローズすることができる

        Args:
        * tableName (String): テーブル名
        
        Throws:
        * ConnectionError: DB接続に失敗した場合にスロー
        """
        self.tableName = tableName
        try:
            print(f'calls the process of open {self.tableName}.')
            self.connection = pymysql.connect(
                host = "db", db = "chatapp", user = "testuser", password = "testuser", charset = "utf8", cursorclass = pymysql.cursors.DictCursor
            )
            print(f'open the connection with {self.tableName}.')
        except:
            raise

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        print(f'calls the process of close {self.tableName}.')
        self.connection.close()
        print(f'close the connection with {self.tableName}.')

    def getDataAll(self):
        """全データを取得する"""
        with self.connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM {self.tableName};')
            return cursor.fetchone()

    def getDataByColumns(self, columns):
        """指定されたカラムのデータを取得する
        
        Args:
        * columns (String or list): 取得するカラム名で複数指定する場合はリストで指定
        """
        with self.connection.cursor() as cursor:
            cursor.execute(f'SELECT {columns if not isinstance(columns, list) else ", ".join(columns)} FROM {self.tableName};')
            return cursor.fetchone()

    def addData(self, data):
        """データを追加する
        
        Args:
        * data (dictionary): keyがカラム名、valueに値が入った辞書型
        """
        columns = []
        values = []
        for key, value in data.items():
            columns.append(key)
            values.append(value)

        with self.connection.cursor() as cursor:
            cursor.execute(f'INSERT INTO {self.tableName} ({", ".join(columns)}) VALUES ({", ".join(values)})')

        self.connection.commit()

    def updateData(self, data, condition):
        """データを更新する
        
        Args:
        * data (dictionary): keyがカラム名、valueに値が入った辞書型
        * condition (String): [カラム名]=[value]形式の文字列でWHERE句で指定する条件
        """
        setValues = []
        for key, value in data.items():
            setValues.append(f'{key}={value}')

        with self.connection.cursor() as cursor:
            cursor.execute(f'UPDATE {self.tableName} SET { ", ".join(setValues)} WHERE {condition}')
        self.connection.commit()

    def deleteData(self, condition):
        """データを削除する

        Args:
        * condition (String): [カラム名]=[value]形式の文字列でWHERE句で指定する条件
        """
        with self.connection.cursor() as cursor:
            cursor.execute(f'DELETE FROM {self.tableName} WHERE {condition}')
        self.connection.commit()
