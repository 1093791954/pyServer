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
            c.execute('CREATE TABLE UserSignal ('
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
        
    # 通过附加码查找其管理者
    def QueryTokenParent(self, token: str) -> tuple[bool, str, str]:
        '''
        查询令牌的父级账户。

        参数:
            token (str): 令牌字符串。

        返回值:
            tuple[bool, str, str]: 包含查询结果的元组，元组包含以下三个元素:
                - bool: 查询是否成功的标志，True表示成功，False表示失败。
                - str: 查询结果的描述信息，成功时为"查询成功"，失败时为具体的错误信息。
                - str: 查询结果的父级账户，成功时为父级账户的名称，失败时为None。
        '''
        try:
            sql_statement = "SELECT account FROM UserRequest WHERE additionalCode = '{}';".format(token)
            c = self.userDb.cursor()
            c.execute(sql_statement)
            result = c.fetchone()
            c.close()
            if result:
                return True, "查询成功", result[0]
            else:
                return False, "附加码不存在", None
        except Exception as e:
            return False, str(e), None

    # 设置信号
    def SetSignal(self, userName: str, signal: int) -> tuple[bool, str]:
        try:
            # 查询当前的agentStatus值
            c = self.userDb.cursor()
            c.execute("SELECT agentStatus FROM UserSignal WHERE userName = ?;", (userName,))
            result = c.fetchone()
            if result is None:
                c.close()
                return False, "无法获取当前的agentStatus值"

            current_status = result[0]
            new_status = current_status | signal

            # 更新agentStatus值
            c.execute("UPDATE UserSignal SET agentStatus = ? WHERE userName = ?;", (new_status, userName))
            self.userDb.commit()
            c.close()

            return True, "设置信号成功"
        except Exception as e:
            return False, str(e)

    # 获取信号
    def GetSignal(self, token: str) -> tuple[bool, str, int]:
        try:
            # 查询additionalCode对应的account
            sql_statement = "SELECT account FROM UserRequest WHERE additionalCode = '{}';".format(token)
            c = self.userDb.cursor()
            c.execute(sql_statement)
            result = c.fetchone()
            c.close()
            if result is None:
                return False, "无法找到对应的账户", 0

            account = result[0]

            # 查询对应的agentStatus
            sql_statement = "SELECT agentStatus FROM UserSignal WHERE userName = '{}';".format(account)
            c = self.userDb.cursor()
            c.execute(sql_statement)
            result = c.fetchone()
            c.close()
            if result is None:
                return False, "无法找到对应的信号", 0

            agentStatus = result[0]

            return True, "获取信号成功", agentStatus
        except Exception as e:
            return False, str(e), 0
        
    # 获取信号 - 通过用户名
    def GetSignalByUserName(self, userName: str) -> tuple[bool, str, int]:
        try:
            # 查询对应的agentStatus
            sql_statement = "SELECT agentStatus FROM UserSignal WHERE userName = '{}';".format(userName)
            c = self.userDb.cursor()
            c.execute(sql_statement)
            result = c.fetchone()
            c.close()
            if result is None:
                return False, "无法找到对应的信号", 0

            agentStatus = result[0]

            return True, "获取信号成功", agentStatus
        except Exception as e:
            return False, str(e), 0

sqlite3_manager  = CSqlManager()
