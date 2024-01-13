import os
import zmq
import socket
import db
from threading import Thread
import time



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
        identity, message = self.zmqsocket.recv_multipart()
        print("Received request: %s" % message)

        #  Do some 'work'
        time.sleep(1)
        
        #  Send reply back to client
        self.zmqsocket.send(b"World")
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

            
