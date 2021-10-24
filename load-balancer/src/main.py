from math import e
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from requests import api
from serverObject import serverObject as so
import socket
import time
import os
import sys
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = Flask(__name__)
CORS(app)

apiServerDict = {}

@app.route("/")
def index():
    return "Success! Load balancer is running."


@app.route("/loadbalancer/notify", methods=['POST'])
def updateServers():
    content = request.json
    servers = content["servers"]

    #If a server is in apiServerDict but not in update, remove it:
    for oldServer in list(apiServerDict.values()):
        if(not list(filter(lambda server: server['name'] == oldServer.getName(), servers))):
            #print(oldServer.getName() + " is not in incoming, to be removed")
            apiServerDict.pop(oldServer.getName())

    for server in servers:
        # If server exists in apiServerDict already, update it's values:
        if server["name"] in apiServerDict.keys():
            oldServer = apiServerDict.get(server["name"])
            if oldServer.getIp() == server["ip"]:
                oldServer.setIp(server["ip"])
            if oldServer.getPort() == server["port"]:
                oldServer.setPort(server["port"])  

        # If server is not in apiServerDict, add new server object to it:
        else:
            newName = server["name"]
            newIp = server["ip"]
            newPort = server["port"]
            apiServerDict[newName] = so.makeServerObject(newIp,newPort,newName)

    # TODO REMOVE LATER, FOR TRACING
    #for a in apiServerDict.values():
    #    print("name: " + str(a.getName()), " ip: " + str(a.getIp()), " port: " + str(a.getPort()), " metric: " + str(a.getMetric()))

    return jsonify({"status": "success"})



###### Forwarding to rest api #######

@app.route("/api/<path:forwardpath>", methods=['GET'])
def forwardGetRequest(forwardpath):
    """
    Forwards ``GET``request to an API server and returns the response to the client.
    """
    content = request.json
    api = pickLeastLoadedApiServer()
    if api:
        endpoint = "http://" + str(api.getIp()) + ":" + str(api.getPort()) + "/" + forwardpath
        
        try:
            start = time.time()
            response = requests.get(url= endpoint, json= content, params= request.args, headers=request.headers)
            end = time.time()
            latency = end - start
            api.setMetric(latency)
            return jsonify(response.json())
            
        except Exception as e:
            return jsonify({"status": "error"})
    else:
        return jsonify({"status": "error"})


@app.route("/api/<path:forwardpath>", methods=['POST'])
def forwardPostRequest(forwardpath):
    """
    Forwards ``POST``request to an API server and returns the response to the client.
    """
    content = request.json
    api = pickLeastLoadedApiServer()
    if api:
        endpoint = "http://" + str(api.getIp()) + ":" + str(api.getPort()) + "/" + forwardpath

        try:
            start = time.time()
            response = requests.post(url= endpoint, json= content, headers=request.headers)
            end = time.time()
            latency = end - start
            api.setMetric(latency)
            return jsonify(response.json())

        except Exception as e:
            return jsonify({"status": "error"})

    else:
        return jsonify({"status": "error"})



########## Private methods ##################

def pickLeastLoadedApiServer():
    """ Returns the least loaded server based on metric values """
    current = None
    lowest = None
    server = None
    for key, value in apiServerDict.items():
        current = value.getMetric()
        if lowest is None:
            lowest = current
            server = key
        if current < lowest:
            lowest = current
            server = key
    return apiServerDict.get(server)


def registerAtDirectoryService(myIp, myPort, myName):
    try:
        content = {"ip": myIp, "port": myPort, "name": myName , "type": "LB"}
        endpoint = "http://" + os.environ.get("DIR_IP") + ":" + os.environ.get("DIR_PORT") + "/directory-service/register"
        response = requests.post(url= endpoint, json= content)
        resp = response.json()
        return resp

    except Exception as e:
        print("1. Error of type " + e.__class__.__name__ + " occured.")
        return False
    

if __name__ == '__main__':
    if len(sys.argv) == 3:
        host = socket.gethostbyname(socket.gethostname())
        port = int(sys.argv[1])
        name = sys.argv[2]

        registerAtDirectoryService(host, port, name)
        app.run(host=host, port=port, debug=False)
    else:
        print("Usage: python main.py <port> <name>")
        exit()

