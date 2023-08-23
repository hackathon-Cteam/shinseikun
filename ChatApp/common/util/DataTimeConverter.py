import datetime

class DataTimeConverter:
    """日時データ変換クラス"""

    def createDatetimeNow():
        """現在時刻のdatetimeオブジェクトを生成する"""
        return datetime.datetime.now()

    def convertDatetime(str):
        """文字列からDatatimeオブジェクトに変換する
        
        Args:
        * str (String): 日時データを表す文字列
        """
        return datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S')
    
    def convertStr(dt, isEenableSeconds= False):
        """Datetimeオブジェクトから文字列(yyyy/mm/dd hh:mm)に変換する

        Args:
        * dt (datetime): datetimeオブジェクト
        * isEenableSeconds (boolean):  秒数まで有効にするかどうか。デフォルトは無効

        Return (String): 日本時間に変換された文字列
        """
        dt = dt + datetime.timedelta(hours=9)
        return dt.strftime('%Y/%m/%d %H:%M:%S') if isEenableSeconds else dt.strftime('%Y/%m/%d %H:%M')