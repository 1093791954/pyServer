import ConnectionObj
import json

# 代理用户心跳处理函数
def agentUserHeartbeat(jsonObj : json)->json:
    '''
    {
        "userName":"123",
        "password":"123"
    }
    '''
    pass

# 普通用户心跳处理函数
def normalUserHeartbeat(jsonObj:json)->json:
    '''
    {
        "token":"token"
    }
    '''
    pass