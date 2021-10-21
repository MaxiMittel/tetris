from flask import Flask, request
from flask_cors import CORS
from flask_script import Manager, Server
from db import *
import socket
import sys
sys.path.append('../../')
from util.serverHelper import *

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "Success! Service is running."


@app.route("/account/signup", methods=['POST'])
def signup():
    """
    Sign up a new user.
    """
    content = request.json
    if (content):
        username = content["username"]
        password = content["password"]
        mail = content["mail"]
        newAccount = {"username": username, "password": password, "mail": mail, "highscore": 0, "stats": [] }
        return dbSignup(newAccount, username)
    else:
        msg = "No arguements passed"
        return jsonify({"status": "error", "error": msg, "auth": "", "username": ""})


@app.route("/account/signin", methods=['POST'])
def signin():
    """
    Sign in an existing user
    """
    content = request.json
    if (content):
        username = content["username"]
        enteredPassword = content["password"]
        return dbSignin(username, enteredPassword)
    else:
        msg = "No arguements(json) passed"
        return jsonify({"status": "error", "error": msg, "auth": "", "username": ""})


@app.route("/user/get", methods=['GET'])
def getUser():
    """
    Returns the account informations of the logged in user.
    """
    content = request.json
    if (content):
        userID = verify_jwt(content["auth"])
        return dbGetUser(userID)
    else:
        msg = "No arguements passed"
        return jsonify({"status": "error", "error": msg, "username": "", "stats": ""})


@app.route("/user/getbyid", methods=['GET'])
def getUserById():
    """
    Get user informations by their id.
    usage example: /user/getbyid?id=616f1a742c1a8f9f3f6588a6
    """
    id = request.args.get("id")
    return dbFindUserById(id)


@app.route("/account/update", methods=['POST'])
def update():
    """ 
    Updates the current users username.
    """
    content = request.json
    if (content):
        userID = verify_jwt(content["auth"])
        newUsername = content["username"]
        return dbUpdateUser(userID, newUsername)
    else:
        msg = "No arguements passed"
        return jsonify({"status": "error", "error": msg, "username": "", "auth": ""})


@app.route("/account/poststat", methods=['POST'])
def postStat():
    """
    Post the result of one game
    """
    content = request.json
    if (content):
        auth = content["auth"]
        userID = verify_jwt(auth)
        stat = content["gamescore"]
        return dbPostStat(userID, stat)
    else:
        msg = "No arguements passed"
        return jsonify({"status": "error", "error": msg})


@app.route("/user/search", methods=['GET'])
def search():
    """
    Search for other users.
    """
    content = request.json
    if (content):
        search = content["query"]
        return dbFindUsers(search)
    else:
        msg = "No arguements passed"
        return jsonify({"status": "error", "error": msg})


@app.route("/account/isAuthenticated")
def getAccount():
    token = request.headers.get("Authorization")
    token = token.replace("Bearer ", "")
    if not token:
        return jsonify({"error": "No token provided"}), 401
    if not verify_jwt(token):
        return jsonify({"error": "Invalid token"}), 401
    return jsonify({"message": "Success"})


if __name__ == '__main__':
    try:
        myName = sys.argv[1]
    except:
        print("Usage guide: <arg1: server name>")
        sys.exit()

    myIp = socket.gethostbyname(socket.gethostname())
    myPort = "9090"

    registerService(myIp, myPort, myName, "API")
    app.run(host="0.0.0.0", port=myPort, debug=False)

