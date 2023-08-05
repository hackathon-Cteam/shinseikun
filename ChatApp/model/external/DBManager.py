import pymysql

class DBManager:
    """データベースを操作するクラス"""

    """ホスト名"""
    HOST = 'db'

    """DB名"""
    DB_NAME = 'chatapp'

    """DBにログインするユーザー"""
    DB_USER = 'testuser'

    """使用するパスワード"""
    DB_PASSWORD = 'testuser'

    """使用する文字セット"""
    CHARSET = 'utf8'

    """SQLで使用する区切り文字"""
    DELIMITER = ', '

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
            print(f'call the process of open {self.tableName}.')
            self.connection = pymysql.connect(
                host = self.HOST, db = self.DB_NAME, user = self.DB_USER, password = self.DB_PASSWORD, charset = self.CHARSET,
                cursorclass = pymysql.cursors.DictCursor
            )
            print(f'open the connection with {self.tableName}.')
        except:
            raise

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        print(f'call the process of close {self.tableName}.')
        self.connection.close()
        print(f'close the connection with {self.tableName}.')

    def getData(self, filterSql=None):
        """データを取得する
        
         Args:
        * filterSql (String): WHERE句で指定する条件のSQL文。条件でデータを絞り込む場合に指定する。
        """
        whereSql = '' if filterSql is None else f' WHERE {filterSql}'
        return self.execGetQuery(f'SELECT * FROM {self.tableName}{whereSql}')

    def getDataByColumns(self, columns, filterSql=None):
        """指定されたカラムのデータを取得する
 
        Args:
        * columns (String or List): 単体の場合はカラム名、複数指定する場合はカラム名のリスト
        * filterSql (String): WHERE句で指定する条件のSQL文。条件でデータを絞り込む場合に指定する。
        """
        whereSql = '' if filterSql is None else f' WHERE {filterSql}'
        return self.execGetQuery(f'SELECT {columns if not isinstance(columns, list) else self.DELIMITER.join(columns)} FROM {self.tableName}{whereSql}')

    def addData(self, data):
        """データを追加する
        
        Args:
        * data (Dictionary): keyがカラム名、valueに値が入った辞書型
        """
        columns = []
        values = []
        for key, value in data.items():
            columns.append(key)
            values.append(f'"{value}"')

        self.execAlterQuery(f'INSERT INTO {self.tableName} ({self.DELIMITER.join(columns)}) VALUES ({self.DELIMITER.join(values)})')

    def updateData(self, data, condition):
        """データを更新する
        
        Args:
        * data (Dictionary): 更新する内容。keyがカラム名、valueに値が入った辞書型
        * condition (String): WHERE句で指定する変更対象を絞り込むためのクエリ文字列
        """
        setValues = []
        for key, value in data.items():
            setValues.append(f'{key}="{value}"')

        self.execAlterQuery(f'UPDATE {self.tableName} SET {self.DELIMITER.join(setValues)} WHERE {condition}')

    def deleteData(self, condition):
        """データを削除する

        Args:
        * condition (String): WHERE句で指定する条件のクエリ文字列
        """
        self.execAlterQuery(f'DELETE FROM {self.tableName} WHERE {condition}')

    def execGetQuery(self, query):
        """情報を取得するクエリを実行する
        
        Args:
        * query (String): 実行するSQL文

        Return: keyがカラム名、valueにデータが入った辞書型の配列

        Throws:
        * Exception: クエリ実行に失敗した場合にスロー
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as error:
            print(f'{error} in DBManager.execGetQuery')
            raise

    def execAlterQuery(self, query):
        """テーブル内の情報を変化させるクエリを実行する
        
        Args:
        * query (String): 実行するSQL文

        Throws:
        * Exception: クエリ実行に失敗した場合にスロー
        """
        try:
            with self.connection.cursor() as cursor:
                print(f'exec sql: {query}')
                cursor.execute(query)
                self.connection.commit()
        except Exception as error:
            print(f'{error} in DBManager.execAlterQuery')
            raise