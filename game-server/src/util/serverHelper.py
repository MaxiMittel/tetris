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
        endpoint = "http://{}:{}/directory-service/register".format(ip, port) 
        content = {"ip": myIp, "port": myPort, "name": myName, "type": myType}
        requests.post(url= endpoint, json= content)
    except Exception as e:
        print("Exception when registering to DS: " + str(e))
        return False