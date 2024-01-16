'''
代理和普通用户对于信号的获取和设置
'''
import json

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
    pass

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
    pass

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
    pass
