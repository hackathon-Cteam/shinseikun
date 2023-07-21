import pymysql
from model.repository.BaseRepository import BaseRepository

class ChannelRepository(BaseRepository):
    __TABLE_NAME = 'channels'
    __COLUMN_ID = 'id'
    __COLUMN_USER_ID = 'uid'
    __COLUMN_NAME = 'name'
    __COLUMN_ABSTRACT = 'abstract'

    def getChannelAll(self):
        """全チャンネル情報を取得する

        Return: 全チャンネル情報
        """
        try:
            cur = self.connection.cursor()
            # TODO: createSql~なメソッドを追加してもっと読みやすくしたい
            cur.execute(self.FORMAT_SQL_SELECT.format(self.COLUMN_ALL, self.__TABLE_NAME))
            return cur.fetchall()
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            # TODO: withを使って自動クローズさせたい
            self.connection.close()


    def getChannelById(self, channelId):
        """指定されたIDのチャンネルを取得する
        
        Args:
        - channelId (String): チャンネルID

        Return: チャンネル情報
        """
        try:
            cur = self.connection.cursor()
            # TODO: createSql~なメソッドを追加してもっと読みやすくしたい
            cur.execute(self.FORMAT_SQL_SELECT_WHERE.format(self.COLUMN_ALL, self.__TABLE_NAME, 'id=%s'), channelId)
            return cur.fetchone()
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            # TODO: withを使って自動クローズさせたい
            self.connection.close()


    def getChannelByName(self, channelName):
        """指定された名前のチャンネル情報を取得する

        Args:
        - channelName (String): チャンネル名
        """
        try:
            cur = self.connection.cursor()
            # TODO: createSql~なメソッドを追加してもっと読みやすくしたい
            cur.execute(self.FORMAT_SQL_SELECT_WHERE.format(self.COLUMN_ALL, self.__TABLE_NAME, 'name=%s'), channelName)
            return cur.fetchone()
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            # TODO: withを使って自動クローズさせたい
            self.connection.close()


    def addChannel(self, userId, channelName, channelDescription):
        """チャンネルを追加する
        
        Args:
        - userId (String): ユーザーID
        - channelName  (String): チャンネル名
        - channelDescription (String): チャンネルの説明
        """
        try:
            cur = self.connection.cursor()
            # TODO: createSql~なメソッドを追加してもっと読みやすくしたい
            cur.execute(
                self.FORMAT_SQL_INSERT_INTO.format(
                    self.__TABLE_NAME,
                    '{}, {}, {}'.format(self.__COLUMN_USER_ID, self.__COLUMN_NAME, self.__COLUMN_ABSTRACT),
                    '%s, %s, %s'),
                (userId, channelName, channelDescription)
            )
            self.connection.commit()
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()


    def updateChannel(self, userId, channelName, channelDescription, channelId):
        """チャンネル情報を更新する

        Args:
        - userId (String): ユーザーID
        - channelName (String): チャンネル名
        - channelDescription (String): チャンネルの説明
        - channelId (String): チャンネルID
        """
        try:
            self.connection.cursor().execute(
                self.FORMAT_SQL_UPDATE_WHERE.format(
                    self.__TABLE_NAME,
                    '{}=%s, {}=%s, {}=%s'.format(self.__COLUMN_USER_ID, self.__COLUMN_NAME, self.__COLUMN_ABSTRACT),
                    '{}=%s'.format(self.__COLUMN_ID),
                ),
                (userId, channelName, channelDescription, channelId)
            )
            self.connection.commit()
        except Exception as e:
            print(e + 'が発生しました')
            abort(500)
        finally:
            # TODO: withを使って自動クローズさせたい
            self.connection.close()


    def deleteChannel(self, channelId):
        """チャンネル情報を削除する
        
        Args:
        - channelId (String): チャンネルID
        """
        try:
            self.connection.cursor().execute(self.FORMAT_SQL_DELETE_WHERE.format(self.__TABLE_NAME, 'id=%s'), (channelId))
            self.connection.commit()
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            # TODO: withを使って自動クローズさせたい
            self.connection.close()