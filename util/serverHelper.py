import requests
import time
from threading import Thread
import util.config as config
from util.metric import *
import random

lbPath = None

def registerService(myIp, myPort, myName, myType):
    """
    Registers a server
    """
    #Get load balancer
    try:
        endpoint = "http://" + config.DIR_IP + ":" + config.DIR_PORT + "/directory-service/getlb"
        getResponse = requests.get(url= endpoint)
        lbList = getResponse.json()
        lb = random.choice(lbList["server"])
        lbPath = "http://" + lb["ip"] + ":" + lb["port"]
    except Exception as e:
        print("Exception when getting LB from DS: " + str(e))
        return False

    #Register at load balancer
    try:
        regmsg = {"ip": myIp, "port": myPort, "name": myName, "type": myType}
        endpoint = lbPath + "/register"
        postResponse = requests.post(url= endpoint, json= regmsg)
        Thread(target=heartbeatTask, args=(myIp, myName, lbPath, True), daemon=True).start()
    except Exception as e:
        print("Exception when registering to LB: " + str(e))
        return False

    #Register at Directory service
    try:
        endpoint = "http://" + config.DIR_IP + ":" + config.DIR_PORT + "/directory-service/register" 
        content = {"ip": myIp, "port": myPort, "name": myName, "type": myType}
        postResponse = requests.post(url= endpoint, json= content)
    except Exception as e:
        print("Exception when registering to DS: " + str(e))
        return False


def heartbeatTask(myIp, myName, lbPath, isRegistered):
    """
    Send server metric to loadbalancer at even interval
    """
    while True:
        if isRegistered:
            try:
                endpoint = lbPath + "/usage"
                metric = calculateMetric(myIp, myName)
                postResponse = requests.post(url= endpoint, json= metric)
                
            except Exception as e:
                print("exception")
        else:
            time.sleep(1)
        time.sleep(10)