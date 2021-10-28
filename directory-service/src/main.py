from flask import Flask, request
from flask_cors import CORS
from server_object import ServerObject as so
from server_object import serverObjectJSONEncoder as sOJE
from threading import Thread
import requests
import time
import sys
import json

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

        key = "{}:{}".format( content["ip"], content["port"])

        if content["type"] == "GS":
            gso = so.makeServerObject(content["ip"], content["port"], content["name"])
            __gameServerDict[key] = gso

        elif content["type"] == "LB":
            lbso = so.makeServerObject(content["ip"], content["port"], content["name"])
            __lbServerDict[key] = lbso
            notifyLoadbalancer()

        elif content["type"] == "API":
            apiso = so.makeServerObject(content["ip"], content["port"], content["name"])
            __apiServerDict[key] = apiso
            notifyLoadbalancer()

        else:
            return json.dumps({"status": "error"}, ensure_ascii=False), 500

        return json.dumps({"status": "success"}, ensure_ascii=False), 200

    else:
        return json.dumps({"status": "error"}, ensure_ascii=False), 500


@app.route("/directory-service/getgs", methods=['GET'])
def getGameServer():
    """
    Request all currently registered game servers.

    Returns:
    A list with all registered services
    """
    servers = []
    for s in list(__gameServerDict.values()):
        servers.append({"name": s.getName(), "ip": s.getIp(), "port": s.getPort()})

    return json.dumps({"server": servers}, ensure_ascii=False), 200


@app.route("/directory-service/getapi", methods=['GET'])
def getApiServer():
    """
    Request all currently registered api servers.

    Returns:
    A list with all registered api services
    """
    servers = []
    for s in list(__apiServerDict.values()):
        servers.append({"name": s.getName(), "ip": s.getIp(), "port": s.getPort()})
        
    return json.dumps({"server": servers}, ensure_ascii=False), 200


@app.route("/directory-service/getlb", methods=['GET'])
def getLoadBalancer():
    """
    Request all currently registered load balancers

    Returns:
    A list with all registered load balancers
    """
    servers = []
    for s in list(__lbServerDict.values()):
        servers.append({"name": s.getName(), "ip": s.getIp(), "port": s.getPort()})

    return json.dumps({"server": servers}, ensure_ascii=False), 200


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
    for server in list(__lbServerDict.values()):
        forwardpath = "loadbalancer/notify"
        endpoint = "http://" + str(server.getIp()) + ":" + str(server.getPort()) + "/" + forwardpath

        servers = []
        for s in list(__apiServerDict.values()):
            servers.append({"name": s.getName(), "ip": s.getIp(), "port": s.getPort()})

        try:
            requests.post(url=endpoint, json={"servers": servers})
        except Exception as e:
            app.logger.error(e)


def remove_unresponsive(server_dict):
    """
    Remove unresponsive servers.
    """
    update_lb = False
    for server in list(server_dict.values()):
        try:
            response = requests.get("http://{}:{}/ping".format(server.getIp(), server.getPort()))
            if response.status_code != 200:
                update_lb = True
                key = "{}:{}".format(server.getIp(), server.getPort())
                server_dict.pop(key, None)
        except Exception as e:
            app.logger.error(e)
            update_lb = True
            key = "{}:{}".format(server.getIp(), server.getPort())
            server_dict.pop(key, None)

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