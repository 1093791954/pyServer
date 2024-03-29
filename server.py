# ------------------------------------
# 服务器
# 简述：项目从该文件启动
# 功能：1、zmq服务器的启动
#       2、连接对象信息的分发
#       3、采用被动管理的方式，
#          管理用户设置需要请求，
#          普通用户获取管理用户的请求进行处理，并将结果记录到服务器，供给管理用户获取。
# ------------------------------------
import os
import zmq
import socket
import db
from threading import Thread
import time
import json

import login_handle
import file_handle
import signal_handle
import heartbeat_handle
import userInfo_handle

class CServer:
    connections = {}
    def __init__(self):
        self.sqlManagerObj = db.CSqlManager()
        self.sqlManagerObj.intiDataBase()
        pass

    #工作线程接收用户信息
    def WorkThread(self):
        # ROUTER套接字接收的消息是一个帧列表
        # 第一个帧是发送消息的客户端的标识符
        # 第二个帧是消息内容
        message = self.zmqsocket.recv_string()
        '''
        {
            "packageType":"AgentLogin"
            "body" : {}
        }
        '''

        # 解析消息为JSON格式
        try:
            message_json = json.loads(message)
            package_id = message_json["packageId"]
            package_type = message_json["packageType"]
            body = message_json["body"]
            retJson : json
            if package_type == "AgenLogin":
                retJson = login_handle.AgentUserLogin(body)
            if package_type == "NormalLogin":
                retJson = login_handle.NormalUserLogin(body)
            if package_type == "AgentUpload":
                retJson = file_handle.uploadScript(body)
            if package_type == "AgentDownload":
                retJson = file_handle.downloadScript(body)
            if package_type == "AgentGetList":
                retJson = file_handle.getScriptList(body)
            if package_type == "normalDownload":
                retJson = file_handle.downloadScript_normalUser(body)
            if package_type == "normalGetList":
                retJson = file_handle.getScriptList_normalUser(body)
            if package_type == "AgentGetSignal":
                retJson = signal_handle.agentGetSignal(body)
            if package_type == "AgentSetSignal":
                retJson = signal_handle.agentSetSignal(body)
            if package_type == "normalGetSignal":
                retJson = signal_handle.normalGetSignal(body)
            if package_type == "AgentHeart":
                retJson = heartbeat_handle.agentUserHeartbeat(body)
            if package_type == "normalHeart":
                retJson = heartbeat_handle.normalUserHeartbeat(body)
            if package_type == "normalSetInfo":
                retJson = userInfo_handle.normalSetInfo(body)
            message_json["body"] = retJson
            self.zmqsocket.send_string(message_json.dumps(response))
        except json.JSONDecodeError:
            '''
            {
                "status":0,
                "msg":"body to json failed"
            }
            '''
            response = {
                "status": 1,
                "msg": "body to json failed"
            }
            self.zmqsocket.send_string(json.dumps(response))
        pass

    def start(self):
        self.context = zmq.Context()
        self.zmqsocket = self.context.socket(zmq.REP)
        self.zmqsocket.bind("tcp://127.0.0.1:9990")
        self.thread = Thread(target=self.WorkThread)
        self.thread.start()
        pass



if __name__ == '__main__':
    server = CServer()
    server.start()
    print("服务器开启成功，绑定IP：0.0.0.0 : 9990")
    os.system("pause")
    while True:
        try:
            os.system("cls")
            print("1 - 注册新管理者")
            print("q/Q - 退出")
            user_input = input("请输入：")
            if user_input == '1':
                input_userName = input('新用户名：')
                input_password = input('新用户密码：')
                server.sqlManagerObj.registerUser(input_userName,input_password)
                continue
            if user_input == 'q' or user_input == 'Q':
                break
        except Exception as e:
            print("异常，程序退出")
            os._exit(0)

            
