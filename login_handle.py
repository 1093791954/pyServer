# ======================
# 用户登陆处理
# 1. 用户账号密码校验
# 2. 用户管理中增加用户
# ======================
import ConnectionObj
import json
import db


def AgentUserLogin( jsonObj: json) -> json:
    # 管理用户登陆
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
    userName = jsonObj["userName"]
    password = jsonObj["password"]
    # 1. 登陆校验
    isSuccess , errMsg = db.sqlite3_manager.QueryUser(userName, password)
    if isSuccess:
        # 3. 返回结果
        retJson['status'] = True
        retJson['msg'] = 'success'
        return retJson
    else:
        retJson['status'] = False
        retJson['msg'] = errMsg
        return retJson
    pass
def NormalUserLogin( jsonObj: json):
    # 普通用户登陆
    '''
    {
        "token":"token"
    }
    返回json:
    {
        "status":True / False,
        "msg":"body to json failed / success"
    }
    '''
    retJson: json
    token = jsonObj["token"]
    ## 1. 登陆校验
    isSuccess , errMsg = db.sqlite3_manager.QueryToken(token)
    if isSuccess:
        # 3. 返回结果
        retJson['status'] = True
        retJson['msg'] = 'success'
        return retJson
    else:
        retJson['status'] = False
        retJson['msg'] = errMsg
        return retJson
    pass