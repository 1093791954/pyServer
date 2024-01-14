# ======================
# 用户登陆处理
# 1. 用户账号密码校验
# 2. 用户管理中增加用户
# ======================
import ConnectionObj
import json
import db


errorCode = {
    "status": False,
    "msg": "body to json failed"
}

successCode = {
    "status": True,
    "msg": "body to json success",
}

class LoginHandler:

    def __init__(self):
        self.sqlManagerObj = db.CSqlManager()
        self.sqlManagerObj.intiDataBase()
        self.connectionObj = ConnectionObj.CConnector()

    def AgentUserLogin(self, jsonObj: json):
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
        userName = jsonObj["userName"]
        password = jsonObj["password"]
        # 1. 登陆校验
        if self.sqlManagerObj.QueryUser(userName, password):
            ## 2. 用户管理中增加用户
            self.ConnectionObj.AddAgentUser(userName, password)
            # 3. 返回结果
            return successCode
        else:
            return errorCode
        

        pass

    def NormalUserLogin(self, jsonObj: json):
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
        token = jsonObj["token"]
        ## 1. 登陆校验
        if self.sqlManagerObj.QueryToken(token):
            ## 2. 用户管理中增加用户
            self.ConnectionObj.AddNormalUser(token)
            # 3. 返回结果
            return successCode
        else:
            return errorCode
        pass
