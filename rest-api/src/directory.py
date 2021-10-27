import requests
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

lbPath = None

def registerService(host, port, name, type):
    """
    Registers at Directory service
    """
    try:
        ip = os.environ.get("DIR_IP")
        port = os.environ.get("DIR_PORT")
        endpoint = "http://{}:{}/directory-service/register".format(ip, port) 
        content = {"ip": host, "port": port, "name": name, "type": type}
        res = requests.post(url= endpoint, json= content)
        return res.status_code == 200
    except Exception as e:
        print("Exception when registering to DS: " + str(e))
        return False