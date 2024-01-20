import ConnectionObj
import json
import db

# 普通用户设置用户信息
def normalSetInfo(jsonObj:json)->json:
    '''
    {
        "token":"token",
        "info":"123456789123456789"
    }
    '''
    retJson : json
    try:
        token = jsonObj["token"]
        info = jsonObj["info"]
        # 1. 登陆校验
        isSuccess , errMsg = db.sqlite3_manager.verifyToken(token)
        if isSuccess:
            # 2. 设置信息
            isSuccess , errMsg = ConnectionObj.global_connectorManager.setNormalUserInfo(token, info)
            retJson['status'] = isSuccess
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