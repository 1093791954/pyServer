# ####################################
# 服务器连接对象管理                  #
# 简述：服务器连接进来的对象统一进行管 #
#       理，以便后续控制。            #
# 功能：1、连接对象记录              #
#       2、连接对象查找              #
#       3、连接对象心跳              #
# ####################################

from threading import Thread

class CConnector:
    def __init__(self) -> None:
        pass


global_connectorManager = CConnector()
