import pymysql
from model.repository.BaseRepository import BaseRepository

class MessageRepository(BaseRepository):
    __TABLE_NAME = 'messages'
    __COLUMN_USER_ID = 'uid'
    __COLUMN_CHANNEL_ID = 'cid'
    __COLUMN_NAME = 'user_name'
    __COLUMN_MESSAGE = 'message'

    def getMessageAll(self, channelId):
        try:
            cur = self.connection.cursor()
            # TODO: createSql~なメソッドを追加してもっと読みやすくしたい
            cur.execute(
                'SELECT id, u.uid, user_name, message FROM messages AS m INNER JOIN users AS u ON m.uid = u.uid WHERE cid = %s;',
                channelId
            )
            return cur.fetchone()
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            # TODO: withを使って自動クローズさせたい
            self.connection.close()


    def addMessage(self, userId, channelId, message):
        try:
            # TODO: createSql~なメソッドを追加してもっと読みやすくしたい
            self.connection.cursor().execute(
                self.FORMAT_SQL_INSERT_INTO.format(
                    self.__TABLE_NAME,
                    '{}, {}, {}'.format(self.__COLUMN_USER_ID, self.__COLUMN_CHANNEL_ID, self.__COLUMN_MESSAGE),
                    '%s, %s, %s'
                ),
                (userId, channelId, message)
            )
            self.connection.commit()
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            # TODO: withを使って自動クローズさせたい
            self.connection.close()


    def deleteMessage(self, messageId):
        try:
            self.connection.cursor().execute(self.FORMAT_SQL_DELETE_WHERE.format(self.__TABLE_NAME, 'id=%s'), (messageId))
            self.connection.commit()
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            # TODO: withを使って自動クローズさせたい
            self.connection.close()