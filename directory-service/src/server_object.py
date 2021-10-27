from json import JSONEncoder


class ServerObject(object):

    def __init__(self, ip, port, name, metric=100):
        self.__ip = ip
        self.__port = port
        self.__name = name
        self.__metric = metric

    def makeServerObject(ip, port, name):
        return ServerObject(ip, port, name)

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


class serverObjectJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ServerObject):
            return {
                'ip': obj.getIp(),
                'port': obj.getPort(),
                'name': obj.getName()
            }
        return super(serverObjectJSONEncoder, self).default(obj)
