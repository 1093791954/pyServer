# ####################################
# 服务器连接对象管理                  #
# 简述：服务器连接进来的对象统一进行管 #
#       理，以便后续控制。            #
# 功能：1、连接对象记录              #
#       2、连接对象查找              #
#       3、连接对象心跳              #
# ####################################

from threading import Thread
import json
from threading import Thread,Lock
import time
import datetime

class CConnector:
    '''
    管理用户的管理JSON
    {
        "userName":{"heartbeat":60},
        "userName":{"heartbeat":60},
        "userName":{"heartbeat":60},
    }
    '''
    agentUser : json
    '''
    管理用户的管理JSON
    {
        "token":{"heartbeat":60 , "info":""},
        "token":{"heartbeat":60 , "info":""},
        "token":{"heartbeat":60 , "info":""},
    }
    '''
    normalUser : json
    
    lock_agent = Lock()
    lock_normal = Lock()

    def __init__(self) -> None:
        Thread(target=self.thread_heart).start()

    # 心跳线程
    def thread_heart(self):
        current_time = datetime.datetime.now()
        while True:
            new_time = datetime.datetime.now()
            time_diff = (new_time - current_time).total_seconds()
            if time_diff > 1:
                current_time = new_time
                
                self.lock_agent.acquire()  # Acquire the lock
                self.lock_normal.acquire()  # Acquire the lock
                try:
                    for user in self.agentUser:
                        self.agentUser[user]["heartbeat"] -= 1
                        if self.agentUser[user]["heartbeat"] == 0:
                            del self.agentUser[user]
                    
                    for token in self.normalUser:
                        self.normalUser[token]["heartbeat"] -= 1
                        if self.normalUser[token]["heartbeat"] == 0:
                            del self.normalUser[token]
                finally:
                    self.lock_agent.release()  # Release the lock
                    self.lock_normal.release()  # Release the lock
    
    # 新增管理用户
    def addAgentUser(self, userName: str) -> None:
        self.lock_agent.acquire()  # Acquire the lock
        try:
            # Add JSON object to the member variable
            self.agentUser[userName] = {"heartbeat": 60}
        finally:
            self.lock_agent.release()  # Release the lock

    # 新增普通用户
    def addNormalUser(self, token: str) -> None:
        self.lock_normal.acquire()  # Acquire the lock
        try:
            # Add JSON object to the member variable
            self.normalUser[token] = {"heartbeat": 60, "info": ""}
        finally:
            self.lock_normal.release()  # Release the lock

    # 刷新管理用户心跳
    def refreshAgentUser(self, userName: str) -> None:
        self.lock_agent.acquire()  # Acquire the lock
        try:
            if userName in self.agentUser:
                self.agentUser[userName]["heartbeat"] = 60
        finally:
            self.lock_agent.release()  # Release the lock

    # 刷新普通用户心跳
    def refreshNormalUser(self, token: str) -> None:
        self.lock_normal.acquire()  # Acquire the lock
        try:
            if token in self.normalUser:
                self.normalUser[token]["heartbeat"] = 60
        finally:
            self.lock_normal.release()  # Release the lock

    # 判断代理用户是否存在
    def queryAgentUser(self, userName: str) -> bool:
        self.lock_agent.acquire()  # Acquire the lock
        try:
            if userName in self.agentUser:
                return True
            else:
                return False
        finally:
            self.lock_agent.release()  # Release the lock

    # 判断普通用户是否存在
    def queryNormalUser(self, token: str) -> bool:
        self.lock_normal.acquire()  # Acquire the lock
        try:
            if token in self.normalUser:
                return True
            else:
                return False
        finally:
            self.lock_normal.release()  # Release the lock


global_connectorManager = CConnector()
