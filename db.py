# ###############################
# 数据库
# 记录用户信息
# ###############################
import sqlite3
import os
from datetime import datetime
import random
import string

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
            '''
            建表 用户账号信息表
            ID              ID
            account         账号
            password        密码
            mac_address     MAC地址
            created_at      创建时间
            '''
            c.execute('CREATE TABLE AgentUser ('
                    'id INTEGER,'
                    'account TEXT PRIMARY KEY,'
                    'password TEXT,'
                    'mac_address TEXT,'
                    'created_at TEXT'
                    ');'
            )
            '''
            建表 用户请求，比如管理端需要下面的用户报告状态，那么修改表中的某列，供给下级用户查看来执行
            account         账号
            agentStatus     管理者信号灯    整数类型
            '''
            c.execute('CREATE TABLE UserRequest ('
                      'account TEXT PRIMARY KEY,'
                      'agentStatus INTEGER,'
                      'FOREIGN KEY (account) REFERENCES AgentUser(account)'
                      ');'
            )
            '''
            建表 用户附加码表
            account         账号
            additionalCode  附加代码    字符串类型
            '''
            c.execute('CREATE TABLE UserRequest ('
                      'account TEXT PRIMARY KEY,'
                      'additionalCode TEXT,'
                      'FOREIGN KEY (account) REFERENCES AgentUser(account)'
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
    def registerUser(self , userName : str , password : str) -> tuple[bool , str , str]:
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

            # 生成随机的16字符的字符串
            additionalCode = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=16))

            # 插入 UserRequest 表
            userRequestSql = "INSERT INTO UserRequest (account, additionalCode) VALUES ('{}', '{}');".format(userName, additionalCode)
            c.execute(userRequestSql)
            self.userDb.commit()  # 如果执行成功则提交事务

            c.close()
            return True, '成功' , userRequestSql
        except Exception as e:
            self.userDb.rollback()  # 如果发生错误则回滚事务
            return False, e , ''

    # 查询用户是否存在
    def QueryUser(self, userName: str, password: str) -> tuple[bool, str]:
        try:
            sql_statement = "SELECT * FROM AgentUser WHERE account = '{}' AND password = '{}';".format(userName, password)
            c = self.userDb.cursor()
            c.execute(sql_statement)
            result = c.fetchone()
            c.close()
            if result:
                return True, "查询成功"
            else:
                return False, "用户不存在"
        except Exception as e:
            return False, str(e)
    
    # 验证附加码
    def verifyToken(self, token: str) -> tuple[bool, str]:
        try:
            sql_statement = "SELECT additionalCode FROM UserRequest WHERE additionalCode = '{}';".format(token)
            c = self.userDb.cursor()
            c.execute(sql_statement)
            result = c.fetchone()
            c.close()
            if result:
                return True, "验证成功"
            else:
                return False, "验证失败"
        except Exception as e:
            return False, str(e)
        

sqlite3_manager  = CSqlManager()
