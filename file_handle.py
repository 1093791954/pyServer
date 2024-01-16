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



# 管理用户上传脚本
def uploadScript( jsonObj: json):
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
    retJson : json
    try:
        userName =  jsonObj["userName"]
        password = jsonObj["password"]
        filename = jsonObj["filename"]
        file = jsonObj["file"]
        # 1. 登陆校验
        isSuccess , errMsg = db.sqlite3_manager.QueryUser(userName, password)
        if isSuccess:
            # 2. 文件上传
            scriptFileManagerObj = scriptFile.CFileManager('script')
            scriptFileManagerObj.upLoadScriptFile_str(userName, filename, file)
            
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
    
# 管理用户下载脚本
def downloadScript( jsonObj: json):
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
    retJson : json
    try:
        userName =  jsonObj["userName"]
        password = jsonObj["password"]
        filename = jsonObj["filename"]
        # 1. 登陆校验
        isSuccess , errMsg = db.sqlite3_manager.QueryUser(userName, password)
        if isSuccess:
            # 2. 文件下载
            scriptFileManagerObj = scriptFile.CFileManager('script')
            file = scriptFileManagerObj.getUserScriptFile_str(userName, filename)
            if file:
                retJson['status'] = True
                retJson['msg'] = file
            else:
                retJson['status'] = False
                retJson['msg'] = 'File not found'
            return retJson
        else:
            retJson['status'] = False
            retJson['msg'] = errMsg
            return retJson
    except Exception as e:
        retJson['status'] = False
        retJson['msg'] = str(e)
        return retJson
    
# 管理用户获取脚本列表
def getScriptList( jsonObj: json):
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
    retJson  : json
    try:
        userName =  jsonObj["userName"]
        password = jsonObj["password"]
        # 1. 登陆校验
        isSuccess , errMsg = db.sqlite3_manager.QueryUser(userName, password)
        if isSuccess:
            # 2. 获取文件列表
            scriptFileManagerObj = scriptFile.CFileManager('script')
            scropt_list = scriptFileManagerObj.getUserScriptFileList(userName)
            retJson['status'] = True
            retJson['msg'] = json.dumps(scropt_list)
            return retJson
        else:
            retJson['status'] = False
            retJson['msg'] = errMsg
            return retJson
    except Exception as e:
        retJson['status'] = False
        retJson['msg'] = str(e)
        return retJson
