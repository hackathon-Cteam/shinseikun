import pymysql
from model.repository.BaseRepository import BaseRepository

class UserRepository(BaseRepository):
    __TABLE_NAME = 'users'
    __COLUMN_ID = 'uid'
    __COLUMN_NAME = 'user_name'
    __COLUMN_MAIL = 'email'
    __COLUMN_PASSWORD = 'password'

    def addUser(self, id, name, mail, password):
        """テーブルにユーザー情報を追加する
        
        Args:
        - id (String): ユーザーID
        - name (String): ユーザー名
        - mail (String): メールアドレス
        - password: (String): パスワード
        """
        try:
            # TODO: createSql~なメソッドを追加してもっと読みやすくしたい
            self.connection.cursor().execute(
                self.FORMAT_SQL_INSERT_INTO.format(
                    self.__TABLE_NAME,
                    '{}, {}, {}, {}'.format(self.__COLUMN_ID, self.__COLUMN_NAME, self.__COLUMN_MAIL, self.__COLUMN_PASSWORD),
                    '%s, %s, %s, %s'
                ),
                (id, name, mail, password)
            )
            self.connection.commit()
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            # TODO: withを使って自動クローズさせたい
            self.connection.close()


    def getUserId(self, mail):
        """ユーザーIDの取得
        
        Args:
        - mail (String): メールアドレス

        Return: ユーザーID
        """
        try:
            cur = self.connection.cursor()
            # TODO: createSql~なメソッドを追加してもっと読みやすくしたい
            cur.execute(self.FORMAT_SQL_SELECT_WHERE.format(self.__COLUMN_ID, self.__TABLE_NAME, 'email=%s'), mail)
            return cur.fetchone()
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            # TODO: withを使って自動クローズさせたい
            self.connection.close()


    def getUser(self, mail):
        """ユーザー情報を取得する
        Args:
        - mail (String): メールアドレス
        
        Return: ユーザー情報
        """
        try:
            cur = self.connection.cursor()
            cur.execute(self.FORMAT_SQL_SELECT_WHERE.format(self.COLUMN_ALL, self.__TABLE_NAME, 'email=%s'), mail)
            return cur.fetchone()
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            # TODO: withを使って自動クローズさせたい
            self.connection.close()