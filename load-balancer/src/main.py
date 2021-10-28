from math import e
from flask import Flask, request
import requests
from flask_cors import CORS
from server_object import serverObject as so
import socket
import time
import sys
from dotenv import load_dotenv, find_dotenv
import multiprocessing
import directory
import json
import os


load_dotenv(find_dotenv())

app = Flask(__name__)
CORS(app)

apiServerDict = {}

@app.route("/")
def index():
    return "Success! Load balancer is running."

@app.route("/ping")
def ping():
    return "pong", 200

@app.route("/loadbalancer/notify", methods=['POST'])
def updateServers():
    content = request.json
    servers = content["servers"]

    #If a server is in apiServerDict but not in update, remove it:
    for oldServer in list(apiServerDict.values()):
        if(not list(filter(lambda server: server['name'] == oldServer.getName(), servers))):
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

    return json.dumps({"status": "success"}, ensure_ascii=False)



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

            # Write to log file
            with open("request_log.csv", 'a+') as f:
                f.write(str(latency) + "," + str(api.getName()) + "," + str(request.method) + "," + str(request.path) + "\n")

            return json.dumps(response.json(), ensure_ascii=False), response.status_code
            
        except Exception as e:
            app.logger.error(e)
            return json.dumps({"status": "error"}, ensure_ascii=False), 500
    else:
        return json.dumps({"status": "error"}, ensure_ascii=False), 500


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

            # Write to log file
            with open("request_log.csv", 'a+') as f:
                f.write(str(latency) + "," + str(api.getName()) + "," + str(request.method) + "," + str(request.path) + "\n")
                
            return json.dumps(response.json(), ensure_ascii=False), response.status_code

        except Exception as e:
            app.logger.error(e)
            return json.dumps({"status": "error"}, ensure_ascii=False), 500

    else:
        return json.dumps({"status": "error"}, ensure_ascii=False), 500



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

    
def Server(host, port):
   app.run(host=host, port=port,)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        host = "0.0.0.0"
        port = int(sys.argv[1])
        name = sys.argv[2]

        server_process = multiprocessing.Process(target=Server, args=(host, port))
        server_process.start()

        # Wait 2 seconds then try until registration was successful
        time.sleep(2)
        is_Registered = directory.registerService(os.environ.get("PUBLIC_IP"), port, name, "LB")
        while not is_Registered:
            app.logger.info("Connection to directory service was unsuccessfull. Retrying in 2s.")
            time.sleep(2)
            is_Registered = directory.registerService(os.environ.get("PUBLIC_IP"), port, name, "LB")

        app.logger.info("Connection to directory service was successfull")
        
    else:
        print("Usage: python main.py <port> <name>")
        exit()

