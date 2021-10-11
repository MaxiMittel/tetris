from flask import Flask, request, jsonify
from flask_cors import CORS
from gameServerObject import gameServerObject as gs

app = Flask(__name__)
CORS(app)


#Dictionary -> key: server name, value: gameServerObject 
__gameServerDict = {}


@app.route("/")
def index():
    return "Success! Load balancer is running."



@app.route("/register", methods=['POST'])
def registerServer():
    """ 
    Register a GameServer or API server to the load balancer.

    """
    content = request.json 
    if (__registerCheck(content)):
        gso = gs.makeGameServerObject(content["ip"],content["port"],content["name"],content["type"])
        __gameServerDict[content["name"]] = gso
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

    else:
        return jsonify({"status": "error"})



@app.route("/gameserver/allocate", methods=['GET'])
def allocate():
    """ 
    Request the ip of a gameserver, load balancing picks service 
    with least load/most free resources.

    Returns: 
    The server with the best/lowest metric value in json-format

    """
    server = __pickLeastLoadedServer()
    if server:
        return jsonify({
            "ip": server.getIp(),
            "port": server.getPort(),
            "name": server.getName,
        })
    else:
        return None
    


@app.route("/api/<path>", methods=['GET'])
def forwardGetRequest():
    """
    Forwards ``GET``request to an API server and returns the response to the client.

    """
    pass



@app.route("/api/<path>", methods=['POST'])
def forwardPostRequest():
    """
    Forwards ``POST``request to an API server and returns the response to the client.

    """
    pass



def __registerCheck(content):
    """ Checks if register request is valid """
    if content is not None:
        for key in __gameServerDict:
            if (key == content['name']):
                return False
        return True
    else:
        return False


def __pickLeastLoadedServer():
    """ Returns the least loaded server based on metric values """
    current = None
    lowest = None
    for gameServer in __gameServerDict:
        current = gameServer.getMetric()
        if(current < lowest or lowest is None):
            lowest = current
    return lowest


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)