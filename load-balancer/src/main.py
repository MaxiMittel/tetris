import json
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from serverObject import serverObject as so
from db import *

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
    if __registerCheck(content):

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


@app.route("/unregister", methods=['DELETE'])
def unregisterServer():
    """ 
    Unregister a GameServer or API server from the load balancer.
    """
    pass


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
        return jsonify({"status": "success"})

    apiServer = __apiServerDict.get(serverName)
    if apiServer:
        apiServer.setMetric(content["usage"])
        return jsonify({"status": "success"})
    
    return jsonify({"status": "error"})


@app.route("/gameserver/allocate", methods=['GET'])
def allocate():
    """ 
    Request the ip of a gameserver, load balancing picks service 
    with least load/most free resources.
    """
    gameServer = __pickLeastLoadedGameServer()
    if gameServer:
        return jsonify({
            "ip": gameServer.getIp(),
            "port": gameServer.getPort(),
            "name": gameServer.getName(),
        })
    else:
        return jsonify({"status": "error"})


@app.route("/gameserver/newsession", methods=['POST'])
def createGameSession():
    """
    Creates a new game session on reqeusted game server
    """
    content = request.json
    if content:
        serverIp = content["ip"]
        return dbAddGameSession(serverIp)
    else:
        msg = "Incorrect data"
        return jsonify({"status": "error", "error": msg, "ip": "", "id": ""})


@app.route("/gameserver/deletesession", methods=['DELETE'])
def deleteGameSession():
    content = request.json
    if content:
        serverId = content["id"]
        return dbRemoveGameSession(serverId)
    else:
        msg = "Incorrect data"
        return jsonify({"status": "error", "error": msg, "ip": "", "id": ""})


@app.route("/migrate", methods=['POST'])
def migrateSingleGameSession():
    """ 
    migrates a gamesession to a new game server
    """
    content = request.json
    gameSessionId = content["id"]
    result = dbCheckForGameSession(gameSessionId)

    if result != False:
        return result

    else:
        server = __pickLeastLoadedGameServer

        if(server):
            serverIp = server.getIp()
            dbUpdateGameSessionHost(gameSessionId, serverIp)

        else:
            msg = "No active Game server available"
            return jsonify({"status": "error", "error": msg, "ip": ""})
        


@app.route("/api/<path:forwardpath>", methods=['GET'])
def forwardGetRequest(forwardpath):
    """
    Forwards ``GET``request to an API server and returns the response to the client.
    """
    content = request.json
    api = __pickLeastLoadedApiServer()
    if api:
        endpoint = "http://" + api.getIp() + ":" + api.getPort() + "/" + forwardpath

        try:
            response = requests.get(url= endpoint, json= content, params= request.args)
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
    api = __pickLeastLoadedApiServer()
    if api:
        endpoint = "http://" + api.getIp() + ":" + api.getPort() + "/" + forwardpath

        try:
            response = requests.post(url= endpoint, json= content)
            return jsonify(response.json())

        except Exception as e:
            return jsonify({"status": "error"})

    else:
        return jsonify({"status": "error"})


########## "Private" methods below ##################

def __registerCheck(content):
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


def __pickLeastLoadedGameServer():
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


def __pickLeastLoadedApiServer():
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, debug=False)

