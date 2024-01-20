'''
代理和普通用户对于信号的获取和设置
'''
import json
import ConnectionObj
import db
# 代理用户设置信号
def agentSetSignal(jsonObj : json)->json:
    '''
        根据db.py 的 SetSignal 设置
    '''
    '''
        {
            "userName":"123",
            "password":"123",
            "signal":1             --- 整数型
        }
        返回json:
        {
            "status":True / False,
            "msg":"body to json failed / success"
        }
    '''
    retJson : json
    try:
        userName = jsonObj["userName"]
        password = jsonObj["password"]
        signal = jsonObj["signal"]
        # 1. 登陆校验
        isSuccess , errMsg = db.sqlite3_manager.QueryUser(userName, password)
        if isSuccess:
            # 2. 设置信号
            db.sqlite3_manager.SetSignal(userName, signal)
            retJson['status'] = True
            retJson['msg'] = 'Success'
            return retJson
        else:
            retJson['status'] = False
            retJson['msg'] = errMsg
            return retJson
    except Exception as e:
            retJson['status'] = False
            retJson['msg'] = str(e)
            return retJson


# 代理用户获取信号
def agentGetSignal(jsonObj : json)->json:
    '''
        根据db.py 的 GetSignal 设置
    '''
    '''
        {
            "userName":"123",
            "password":"123"
        }
        返回json:
        {
            "status":True / False,
            "msg":"body to json failed / success"
        }
    '''
    retJson : json
    try:
        userName = jsonObj["userName"]
        password = jsonObj["password"]
        # 1. 登陆校验
        isSuccess , errMsg = db.sqlite3_manager.QueryUser(userName, password)
        if isSuccess:
            # 2. 获取信号
            isSuccess , errMsg , signal = db.sqlite3_manager.GetSignalByUserName(userName)
            if isSuccess:
                retJson['status'] = True
                retJson['msg'] = 'Success'
                retJson['signal'] = signal
                return retJson
            else:
                retJson['status'] = False
                retJson['msg'] = errMsg
                return retJson
        else:
            retJson['status'] = False
            retJson['msg'] = errMsg
            return retJson
    except Exception as e:
            retJson['status'] = False
            retJson['msg'] = str(e)
            return retJson




# 普通用户获取信号
def normalGetSignal(jsonObj : json)->json:
    '''
        需要先根据token找到父的账号，在进行获取。
    '''
    '''
        {
            "token":"123"
        }
        返回json:
        {
            "status":True / False,
            "msg":"body to json failed / success"
        }
    '''
    retJson : json
    try:
        token = jsonObj["token"]
        # 1. 登陆校验
        isSuccess , errMsg = db.sqlite3_manager.verifyToken(token)
        if isSuccess:
            # 2. 获取信号
            isSuccess , errMsg , signal = db.sqlite3_manager.GetSignal(token)
            if isSuccess:
                retJson['status'] = True
                retJson['msg'] = 'Success'
                retJson['signal'] = signal
                return retJson
            else:
                retJson['status'] = False
                retJson['msg'] = errMsg
                return retJson
        else:
            retJson['status'] = False
            retJson['msg'] = errMsg
            return retJson
    except Exception as e:
            retJson['status'] = False
            retJson['msg'] = str(e)
            return retJson
