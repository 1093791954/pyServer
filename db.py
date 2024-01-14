# ###############################
# 数据库
# 记录用户信息
# ###############################
import sqlite3
import os
from datetime import datetime

class CSqlManager:
    def __init__(self):
        pass

    def intiDataBase(self):
        if os.path.exists('user.db'):
            #文件存在
            print('数据库存在，无需初始化！')
            self.userDb = sqlite3.connect('user.db')
        else:
            #文件不存在
            print('数据库不存在，开始创建数据库！')
            self.userDb = sqlite3.connect('user.db')
            c = self.userDb.cursor()
            c.execute('CREATE TABLE AgentUser ('
                    'id INTEGER,'
                    'account TEXT PRIMARY KEY,'
                    'password TEXT,'
                    'mac_address TEXT,'
                    'created_at TEXT'
                    ');'
            )
            c.close()

    def getAgentUserCount(self) -> int:
        c = self.userDb.cursor()
        c.execute('SELECT COUNT(*) FROM AgentUser')
        result = c.fetchone()[0]
        c.close()
        return result

    # 注册用户
    def registerUser(self , userName : str , password : str) -> tuple[bool , str]:
        nowTime = datetime.now()
        formatted_time = nowTime.strftime("%Y-%m-%d")
        id = self.getAgentUserCount()
        id = id + 1
        mac = 'NULL'
        table_name = 'AgentUser'
        sql_statement = "INSERT INTO {} (id, account, password, mac_address, created_at) VALUES ({}, '{}', '{}', '{}', '{}');".format( table_name, id, userName, password, mac, formatted_time )
        try:
            c = self.userDb.cursor()
            c.execute(sql_statement)
            self.userDb.commit()  # 如果执行成功则提交事务
            c.close()
            #print("SQL语句执行成功！")
            return True,'成功'
        except Exception as e:
            self.userDb.rollback()  # 如果发生错误则回滚事务
            #print("执行SQL语句时发生错误:", e)
            # 如果希望将异常继续传播，可以重新引发异常
            # raise e
            return False,e

    #查询用户是否存在
    def QueryUser(self, userName : str) -> bool :
        pass
