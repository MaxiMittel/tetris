from datetime import datetime
from math import e
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from serverObject import serverObject as so
from db import *
import socket
import time
from threading import Thread
import os
import sys
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = Flask(__name__)
CORS(app)

__gameServerDict = {}
__apiServerDict = {}


@app.route("/")
def index():
    return "Success! Load balancer is running."


@app.route("/register", methods=['POST'])
def registerServer():
    """ 
    Register a GameServer or API server to the load balancer.
    """
    content = request.json 
    if registerCheck(content):

        if content["type"] == "GS":
            gso = so.makeServerObject(content["ip"],content["port"],content["name"])
            __gameServerDict[content["name"]] = gso

        elif content["type"] == "API":
            api = so.makeServerObject(content["ip"],content["port"],content["name"])
            __apiServerDict[content["name"]] = api

        else:
            return jsonify({"status": "error"})

        return jsonify({"status": "success"})

    else:
        return jsonify({"status": "error"})


@app.route("/unregister/<id>", methods=['DELETE'])
def unregisterServer(id):
    """ 
    Unregister a GameServer or API server from the load balancer.
    """
    if id in __gameServerDict.keys():
        __gameServerDict.pop(id)
        return jsonify({"status": "success"})

    elif id in __apiServerDict.keys():
        __apiServerDict.pop(id)
        return jsonify({"status": "success"})

    return jsonify({"status": "error"})


@app.route("/usage", methods=['POST'])
def heartbeat():
    """ 
    Periodically update the utilization of every server.
    """
    content = request.json
    serverName = content["name"]

    gameServer = __gameServerDict.get(serverName)
    if gameServer:
        gameServer.setMetric(content["usage"])
        gameServer.setLastContact(datetime.now())
        return jsonify({"status": "success"})

    apiServer = __apiServerDict.get(serverName)
    if apiServer:
        apiServer.setMetric(content["usage"])
        apiServer.setLastContact(datetime.now())
        return jsonify({"status": "success"})
    
    return jsonify({"status": "error"})


@app.route("/gameserver/allocate", methods=['GET'])
def allocate():
    """ 
    Request the ip of a gameserver, load balancing picks service 
    with least load/most free resources.
    """
    dropNonresponsiveServers()
    gameServer = pickLeastLoadedGameServer()
    if gameServer:
        return jsonify({
            "ip": gameServer.getIp(),
            "port": gameServer.getPort(),
            "name": gameServer.getName(),
        })
    else:
        return jsonify({"status": "error"})




######## GAME SESSIONS BELOW ##########

@app.route("/sessions/list", methods=['GET'])
def getGameSessions():
    """
    Get list of all gamesessions
    """
    return dbGetGameSessions()


@app.route("/sessions/allocate", methods=['POST'])
def createGameSession():
    """
    Allocates for a new gamesession
    """
    try:
        content = request.json
        name = content["name"]
        server = pickLeastLoadedGameServer()
        serverIp = server.getIp()
        serverPort = server.getPort()
        return dbAllocate(serverIp, serverPort, name)
    except Exception as e:
        return jsonify({"status": "error", "error": e.__class__.__name__})


@app.route("/sessions/get", methods=['GET'])
def getGameSession():
    """
    Get session by its uniqe id
    """
    id = request.args.get("id")
    return dbGetSingleGameSession(id)


@app.route("/sessions/delete", methods=['POST'])
def deleteGameSession():
    """
    Deletes a game session
    """
    try:
        content = request.json
        sessionId = content["id"]
        serverIp = content["ip"]
        serverPort = content["port"]
        response = dbGetSingleGameSession(sessionId)
        result = response.json

        if (serverIp == result["ip"] and serverPort == result["port"]):
            return dbRemoveGameSession(sessionId)
        else:
            return jsonify({"status": "success", "error": "Did not delete session"})

    except Exception as e:
        return jsonify({"status": "error", "error": e.__class__.__name__})


@app.route("/sessions/migrate", methods=['POST'])
def migrateSingleGameSession():
    """ 
    migrates a gamesession to a new game server
    """
    try:
        content = request.json
        sessionId = content["id"]
        name = content["name"]
        response = dbGetSingleGameSession(sessionId)
        result = response.json
        
        if result["status"] == "error":
            dropNonresponsiveServers()
            server = pickLeastLoadedGameServer()
            serverIp = server.getIp()
            serverPort = server.getPort()
            return dbAllocate(serverIp, serverPort, name)
        else:
            return result

    except Exception as e:
        print(e)
        return jsonify({"status": "error", "error": e.__class__.__name__})




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
            response = requests.get(url= endpoint, json= content, params= request.args, headers=request.headers)
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
            response = requests.post(url= endpoint, json= content, headers=request.headers)
            return jsonify(response.json())

        except Exception as e:
            return jsonify({"status": "error"})

    else:
        return jsonify({"status": "error"})





########## Private methods below ##################

def registerCheck(content):
    """ Checks if register request is valid """
    if content is not None:
        for key in __gameServerDict:
            if (key == content['name']):
                return False
        for key in __apiServerDict:
            if (key == content['name']):
                return False
        return True
    else:
        return False

def dropNonresponsiveServers():
    """ Go through all servers and drop non"""
    now = datetime.now()
    forwardpath = "/directory-service/unregister/"
    for server in __gameServerDict.values():
        if (now - server.getLastContact()) > os.environ.get("TIMEOUT"):
            # also needs to kick out the server from the dir service list
            """ - Can be added in for testing
            endpoint = "http://" + server.getIp + ":" + server.getPort + "/" + forwardpath + server.getName

            try:
                requests.delete(url=endpoint, params=request.args)

            except Exception as e:
                print(server.getName + "could not be deleted on the directory service!")
            """
            __gameServerDict.pop(server.getName())

    for server in __apiServerDict.values:

        if (now - server.getLastContact()) > os.environ.get("TIMEOUT"):
            """
            endpoint = "http://" + server.getIp + ":" + server.getPort + "/" + forwardpath + server.getName

            try:
                requests.delete(url=endpoint, params=request.args)

            except Exception as e:
                print(server.getName + "could not be deleted on the directory service!")
            """

            __apiServerDict.pop(server.getName())


def pickLeastLoadedGameServer():
    """ Returns the least loaded server based on metric values """
    current = None
    lowest = None
    server = None
    for key, value in __gameServerDict.items():
        current = value.getMetric()
        if lowest is None:
            lowest = current
            server = key
        if current < lowest:
            lowest = current
            server = key
    return __gameServerDict.get(server)


def pickLeastLoadedApiServer():
    """ Returns the least loaded server based on metric values """
    current = None
    lowest = None
    server = None
    for key, value in __apiServerDict.items():
        current = value.getMetric()
        if lowest is None:
            lowest = current
            server = key
        if current < lowest:
            lowest = current
            server = key
    return __apiServerDict.get(server)


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
    

def updateServersTask(dirIP, dirPort):
    """
    Periodically fetch registered servers from the directory service
    """
    GSEndpoint = "http://" + dirIP + ":" + dirPort + "/directory-service/getgs"
    APIEndpoint ="http://" + dirIP + ":" + dirPort + "/directory-service/getapi"
    while True:
        try:    
            """ Fetch game servers """
            GSResponse = requests.get(url= GSEndpoint)
            gameServerList = GSResponse.json()

            for server in gameServerList["server"]:
                if server not in __gameServerDict.keys():
                    """ Add any servers that is not in this server dictionary """
                    gso = so.makeServerObject(server["ip"],server["port"],server["name"])
                    __gameServerDict[server["name"]] = gso    
                else:
                    """ Update existing server"""
                    pass

            """ Fetch api servers """
            APISResponse = requests.get(url= APIEndpoint)
            apiServerList = APISResponse.json()

            for server in apiServerList["server"]:
                """ Add any servers that is not in this server dictionary """
                if server not in __apiServerDict.keys():
                    apio = so.makeServerObject(server["ip"],server["port"],server["name"])
                    __apiServerDict[server["name"]] = apio
                else:
                    """ Update existing server"""
                    pass

            time.sleep(int(os.environ.get("PERIODIC_UPDATE"))) 
        except Exception as e:
            time.sleep(int(os.environ.get("PERIODIC_UPDATE")))
            

if __name__ == '__main__':

    if len(sys.argv) == 3:
        host = socket.gethostbyname(socket.gethostname())
        port = int(sys.argv[1])
        name = sys.argv[2]

        registerAtDirectoryService(host, port, name)
        Thread(target=updateServersTask, args=(os.environ.get("DIR_IP"), os.environ.get("DIR_PORT")), daemon=True).start()
        app.run(host=host, port=port, debug=False)
    else:
        print("Usage: python main.py <port> <name>")
        exit()

