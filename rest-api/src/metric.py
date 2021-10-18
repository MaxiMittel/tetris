
import psutil

def calculateMetric(serverIp, serverName):
    metric = psutil.cpu_percent()
    return {"ip": serverIp, "name": serverName, "usage": str(metric) }
