from flask import Flask, request, jsonify
from flask_cors import CORS
from serverObject import ServerObject as so
from serverObject import serverObjectJSONEncoder as sOJE

app = Flask(__name__)
CORS(app)
app.json_encoder = sOJE

__gameServerDict = {}


@app.route("/directory-service")
def index():
    return "Success! Directory Service is running."


@app.route("/directory-service/register", methods=['POST'])
def registerServer():
    """
    Register a GameServer to the Directory Service.
    """
    content = request.json
    if __empty_check(content):

        if content["type"] == "GS":
            gso = so.makeServerObject(content["ip"], content["port"], content["name"])
            __gameServerDict[content["name"]] = gso

        else:
            return jsonify({"status": "error"})

        return jsonify({"status": "success"})

    else:
        return jsonify({"status": "error"})


# DONE

@app.route("/directory-service/unregister/<id>", methods=['DELETE'])
def unregisterServer(id):
    """
    Unregister a GameServer from the Directory Service.
    """
    if id in __gameServerDict.keys():
        __gameServerDict.pop(id)
        return jsonify({"status": "success"})

    return jsonify({"status": "error"})


# DONE
@app.route("/directory-service/getServer", methods=['GET'])
def get_server():
    """
    Request all currently registered game servers.

    Returns:
    A list with all registered services
    """
    print(__gameServerDict)
    servers = list(__gameServerDict.values())
    return jsonify(server=servers)


### Private methods below ###

def __empty_check(content):
    """ Checks if register request is valid """
    if content is not None:
        return True
    else:
        return False


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, debug=False)
