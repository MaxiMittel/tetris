from flask import Flask, request, jsonify
from flask_cors import CORS
from serverObject import ServerObject as so
from serverObject import serverObjectJSONEncoder as sOJE
from threading import Thread
import requests
import time
import sys

app = Flask(__name__)
CORS(app)
app.json_encoder = sOJE

__gameServerDict = {}
__apiServerDict = {}
__lbServerDict = {}


@app.route("/directory-service")
def index():
    return "Success! Directory Service is running."


@app.route("/directory-service/register", methods=['POST'])
def registerServer():
    """
    Register a GameServer/ApiServer/LbServer to the Directory Service.
    """
    content = request.json
    if __empty_check(content):

        if content["type"] == "GS":
            gso = so.makeServerObject(content["ip"], content["port"], content["name"])
            __gameServerDict[content["name"]] = gso

        elif content["type"] == "LB":
            lbso = so.makeServerObject(content["ip"], content["port"], content["name"])
            __lbServerDict[content["name"]] = lbso

        elif content["type"] == "API":
            apiso = so.makeServerObject(content["ip"], content["port"], content["name"])
            __apiServerDict[content["name"]] = apiso
            notifyLoadbalancer()

        else:
            return jsonify({"status": "error"})

        return jsonify({"status": "success"})

    else:
        return jsonify({"status": "error"})


@app.route("/directory-service/unregister/<id>", methods=['DELETE'])
def unregisterServer(id):
    """
    Unregister a GameServer/ApiServer/LbServer from the Directory Service.
    """
    if id in __gameServerDict.keys():
        __gameServerDict.pop(id)
        return jsonify({"status": "success"})

    elif id in __lbServerDict.keys():
        __lbServerDict.pop(id)
        return jsonify({"status": "success"})

    elif id in __apiServerDict.keys():
        __apiServerDict.pop(id)
        notifyLoadbalancer()
        return jsonify({"status": "success"})

    return jsonify({"status": "error"})


@app.route("/directory-service/getgs", methods=['GET'])
def getGameServer():
    """
    Request all currently registered game servers.

    Returns:
    A list with all registered services
    """
    servers = list(__gameServerDict.values())
    return jsonify(server=servers)


@app.route("/directory-service/getapi", methods=['GET'])
def getApiServer():
    """
    Request all currently registered api servers.

    Returns:
    A list with all registered api services
    """
    servers = list(__apiServerDict.values())
    return jsonify(server=servers)


@app.route("/directory-service/getlb", methods=['GET'])
def getLoadBalancer():
    """
    Request all currently registered load balancers

    Returns:
    A list with all registered load balancers
    """
    servers = list(__lbServerDict.values())
    return jsonify(server=servers)


### Private methods below ###

def __empty_check(content):
    """ Checks if register request is valid """
    if content is not None:
        return True
    else:
        return False


def notifyLoadbalancer():
    """
    When the entries in the api dictionary changes, these changes are posted to the load balancer
    """
    for server in __lbServerDict.values():
        forwardpath = "loadbalancer/notify"
        endpoint = "http://" + str(server.getIp()) + ":" + str(server.getPort()) + "/" + forwardpath

        servers = []
        for s in __apiServerDict.values():
            servers.append({"name": s.getName(), "ip": s.getIp(), "port": s.getPort()})

        try:
            response = requests.post(url=endpoint, json={"servers": servers}, headers=request.headers)
        except Exception as e:
            print(e)
            print("API Server list update at the Loadbalancer was unsuccessful ")


def remove_unresponsive(server_dict):
    """
    Remove unresponsive servers.
    """
    update_lb = False
    for server in list(server_dict.values()):
        response = requests.get("http://{}:{}/ping".format(server.getIp(), server.getPort()))
        if response.status_code != 200:
            update_lb = True
            server_dict.pop(server.getName(), None)

    if update_lb:
        notifyLoadbalancer()


def heartbeat_thread():
    """
    Heartbeat thread.
    """
    while True:
        #Check if game servers are alive
        remove_unresponsive(__gameServerDict)
        #Check if api servers are alive
        remove_unresponsive(__apiServerDict)
        #Check if lb servers are alive
        remove_unresponsive(__lbServerDict)

        time.sleep(1)


if __name__ == '__main__':

    if len(sys.argv) == 2:
        Thread(target=heartbeat_thread, daemon=True).start()
        app.run(host='0.0.0.0', port=int(sys.argv[1]))
    else:
        print("Usage: python3 main.py <port>")