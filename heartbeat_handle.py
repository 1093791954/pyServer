import ConnectionObj
import json
import db

# 代理用户心跳处理函数
def agentUserHeartbeat(jsonObj : json)->json:
    '''
    {
        "userName":"123",
        "password":"123"
    }
    '''
    try:
        userName = jsonObj["userName"]
        password = jsonObj["password"]
        # 1. 登陆校验
        isSuccess , errMsg = db.sqlite3_manager.QueryUser(userName, password)
        if isSuccess:
            ConnectionObj.global_connectorManager.refreshAgentUser(userName)
    except Exception as e:
        pass

# 普通用户心跳处理函数
def normalUserHeartbeat(jsonObj:json)->json:
    '''
    {
        "token":"token"
    }
    '''
    try:
        token = jsonObj["token"]
        # 1. 附加码校验
        isSuccess , errMsg = db.sqlite3_manager.verifyToken(token)
        if isSuccess:
            ConnectionObj.global_connectorManager.refreshNormalUser(token)
    except Exception as e:
        pass