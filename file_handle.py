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

def uploadScript(jsonObj : json):
    '''
        {
            "userName":"123",
            "password":"123",
            "filename":"script1.lua",
            "file":"base64"
        }
        返回json:
        {
            "status":True / False,
            "msg":"body to json failed / success"
        }
    '''
    pass

def downloadScript(jsonObj:json):
    '''
        {
            "userName":"123",
            "password":"123",
            "filename":"script1.lua"
        }
        返回json:
        {
            "status":True / False,
            "msg":"body to json failed / success"
        }
    '''
    pass

def getScriptList(jsonObj : json):
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




