
class serverObject(object):

    def __init__(self,ip,port,name,metric=0):
        self.__ip = ip
        self.__port = port
        self.__name = name
        self.__metric = metric

    def makeServerObject(ip,port,name):
        return serverObject(ip,port,name)

    def getIp(self):
        return self.__ip
    def setIp(self, ip):
        self.__ip = ip
    
    def getPort(self):
        return self.__port
    def setPort(self, port):
        self.__port = port
    
    def getName(self):
        return self.__name
    def setName(self, name):
        self.__name = name

    def getMetric(self):
        return self.__metric
    def setMetric(self, metric):
        self.__metric = metric



