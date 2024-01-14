# ======================
# 用户脚本文件操作处理
# 1. 文件的上传
# 2. 文件的下载
# 3. 文件列表的获取
# 4. 文件的删除
# ======================
import db
import scriptFile
import json

errorCode = {
    "status": False,
    "msg": "body to json failed"
}

successCode = {
    "status": True,
    "msg": "body to json success",
}

class fileHandler:
    def __init__(self):
        self.sqlManagerObj = db.CSqlManager()
        self.sqlManagerObj.intiDataBase()
    def uploadScript(self, jsonObj: json):
        '''
            {
                "userName":"123",
                "password":"123",
                "filename":"script1.lua",
                "file":"file base64"
            }
            返回json:
            {
                "status":True / False,
                "msg":"body to json failed / success"
            }
        '''
        try:
            userName =  jsonObj["userName"]
            password = jsonObj["password"]
            filename = jsonObj["filename"]
            file = jsonObj["file"]
            # 1. 登陆校验
            if self.sqlManagerObj.QueryUser(userName, password):
                # 2. 文件上传
                scriptFileManagerObj = scriptFile.CFileManager('script')
                scriptFileManagerObj.upLoadScriptFile_str(userName, filename, file)
                
                return successCode
                # 3. 返回结果
            else:
                return errorCode
               
        except Exception:
            return errorCode

    def downloadScript(self, jsonObj: json):
        '''
            {
                "userName":"123",
                "password":"123",
                "filename":"script1.lua"
            }
            返回json:
            {
                "status":True / False,
                "msg":"body to json failed / success",
                "file":""
            }
        '''
        try:
            userName =  jsonObj["userName"]
            password = jsonObj["password"]
            filename = jsonObj["filename"]
            # 1. 登陆校验
            if self.sqlManagerObj.QueryUser(userName, password):
                # 2. 文件下载
                scriptFileManagerObj = scriptFile.CFileManager('script')
                file = scriptFileManagerObj.getUserScriptFile_str(userName, filename)
                successCode["file"] = file
                # 3. 返回结果
                return successCode
            else:
                return errorCode
               
        except Exception:
            return errorCode

    def getScriptList(self, jsonObj: json):
        '''
            {
                "userName":"123",
                "password":"123"
            }
            返回json:
            {
                "status":True / False,
                "msg":"body to json failed / success",
                "scropt_list": []
            }
        '''
        try:
            userName =  jsonObj["userName"]
            password = jsonObj["password"]
            # 1. 登陆校验
            if self.sqlManagerObj.QueryUser(userName, password):
                # 2. 获取文件列表
                scriptFileManagerObj = scriptFile.CFileManager('script')
                scropt_list = scriptFileManagerObj.getUserScriptFileList(userName)
                # 3. 返回结果
                successCode["scropt_list"] = scropt_list
                return successCode
            else:
                return errorCode
               
        except Exception:
            return errorCode





