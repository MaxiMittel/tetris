class gameServerObject(object):

    def __init__(self,ip,port,name,serverType,metric=None):
        self.__ip = ip
        self.__port = port
        self.__name = name
        self.__serverType = serverType
        self.__metric = metric


    def makeGameServerObject(ip,port,name,serverType):
        return gameServerObject(ip,port,name,serverType)


    def getIp(self):
        return self.__ip

    def getPort(self):
        return self.__port

    def getName(self):
        return self.__name

    def getServerType(self):
        return self.__serverType

    def getMetric(self):
        return self.__metric


    def setMetric(self, metric):
        self.__metric = metric


