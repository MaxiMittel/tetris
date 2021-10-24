import requests
import time
from threading import Thread
from util.metric import *
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

lbPath = None

def registerService(myIp, myPort, myName, myType):
    """
    Registers a server
    """
    #Register at Directory service
    try:
        ip = os.environ.get("DIR_IP")
        port = os.environ.get("DIR_PORT")
        endpoint = "http://{}:{}/directory-service/heartbeat".format(ip, port) 
        content = {"ip": myIp, "port": myPort, "name": myName, "type": myType}
        requests.post(url= endpoint, json= content)
        Thread(target=heartbeatTask, args=(myIp, myName, True), daemon=True).start()
    except Exception as e:
        print("Exception when registering to DS: " + str(e))
        return False


def heartbeatTask(isRegistered):
    """
    Send server metric to directory service at even interval
    """
    while True:
        if isRegistered:
            try:
                ip = os.environ.get("DIR_IP")
                port = os.environ.get("DIR_PORT")
                endpoint = "http://{}:{}/directory-service/heartbeat".format(ip, port)
                requests.post(url= endpoint)
                
            except Exception as e:
                print("exception")
        else:
            time.sleep(1)
        time.sleep(int(os.environ.get("HEARTBEAT_FREQUENCY")))