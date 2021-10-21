from datetime import datetime

class serverObject(object):

    def __init__(self,ip,port,name,metric=100):
        self.__ip = ip
        self.__port = port
        self.__name = name
        self.__metric = metric
        self.__lastContact = datetime.now()

    def makeServerObject(ip,port,name):
        return serverObject(ip,port,name)

    def getIp(self):
        return self.__ip

    def getPort(self):
        return self.__port

    def getName(self):
        return self.__name

    def getMetric(self):
        return self.__metric
    def setMetric(self, metric):
        self.__metric = metric

    def getLastContact(self):
        return self.__lastContact
    def setLastContact(self, lastContact):
        self.__lastContact = lastContact


