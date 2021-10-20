import requests
import psutil
import time
from threading import Thread

loadbalancerAddressAndPort = "http://192.168.1.204:7777"

def calculateMetric(serverIp, serverName):
    """
    Calculates a metric for deciding least loaded server
    """
    metric = psutil.cpu_percent()
    return {"ip": serverIp, "name": serverName, "usage": str(metric) }

def registerAtLoadBalancer(myIp, myPort, myName, myType):
    """
    Registers a server at the load balancer
    """
    regmsg = {"ip": myIp, "port": myPort, "name": myName, "type": myType}
    endpoint = loadbalancerAddressAndPort + "/register"
    try:
        requests.post(url= endpoint, json= regmsg)
        Thread(target=heartbeatTask, args=(myIp, myName, True), daemon=True).start()
        
    except:
        return False

def heartbeatTask(myIp, myName, isRegistered):
    """
    Send server metric to loadbalancer at even interval
    """
    while True:
        if isRegistered:
            try:
                endpoint = loadbalancerAddressAndPort + "/usage"
                metric = calculateMetric(myIp, myName)
                requests.post(url= endpoint, json= metric)
                
            except Exception as e:
                print("exception")
        else:
            time.sleep(1)
        time.sleep(10)