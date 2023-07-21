from enum import Enum

class ErrorMessage(Enum):
    FAILD_CREATE_USER = 'already registered users.'
    FAILD_LOGIN_NOT_EXIST = 'not exist user.'
    FAILD_LOGIN_MISTAKE_PASSWORD = 'mistake password.'
    FAILD_ADD_CHANNEL_ALREADY_EXIST = 'already registered channels.'
    FAILD_DELETE_CHANNEL_NOT_PERMISSION = 'not authorized to delete channels.'
