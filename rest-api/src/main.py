from threading import Thread
from flask import Flask, request
from flask_cors import CORS
from flask_script import Manager, Server
from db import *
from metric import *
import sys
import time
import requests
import jwt

SECRET = "CHANGE_SECRET"
def verify_jwt(token):
    try:
        return jwt.decode(token, SECRET, algorithms=['HS256'])
    except jwt.exceptions.InvalidSignatureError:
        return False
    except jwt.exceptions.DecodeError:
        return False

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
        token = jwt.encode({"id": username}, SECRET , algorithm="HS256")
        newAccount = {"username": username, "password": password, "mail": mail, "auth": token, "highscore": 0, "stats": [ ] }
        return dbSignup(newAccount, username, token)
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
        userID = content["username"]
        enteredPassword = content["password"]
        return dbSignin(userID, enteredPassword)
    else:
        msg = "No arguements passed"
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


@app.route("/account/update", methods=['POST'])
def update():
    """ 
    Updates the current users username.
    """
    content = request.json
    if (content):
        auth = content["auth"]
        userID = verify_jwt(auth)
        newUsername = content["username"]
        newAuth = jwt.encode({"id": newUsername}, SECRET , algorithm="HS256")
        return dbUpdateUser(userID, newUsername, newAuth)
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
        userList = content["query"]
        return dbFindUsers(userList)
    else:
        msg = "No arguements passed"
        return jsonify({"status": "error", "error": msg})


@app.route("/user/getbyid", methods=['GET'])
def getUserById():
    """
    Get user informations by their id.
    """
    content = request.json
    id = content["id"]
    return dbFindUserById(str(id))


"""
@app.route("/account/isAuthenticated")
def getAccount():
    token = request.headers.get("Authorization")
    token = token.replace("Bearer ", "")
    if not token:
        return jsonify({"error": "No token provided"}), 401
    if not verify_jwt(token):
        return jsonify({"error": "Invalid token"}), 401
    return jsonify({"message": "Success"})


@app.route("/account/getAuthenticatedUser")
def getAuthenticatedUser():
    return jsonify({
        "username": "John452",
        "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Est nam ipsa consequatur laborum explicabo.",
        "games": [
            {"score": 1000, "bpm": 4.56, "date": 1631647493076},
            {"score": 1005, "bpm": 4.89, "date": 1631647493076},
            {"score": 980, "bpm": 4.6, "date": 1631647493076},
            {"score": 1100, "bpm": 3.2, "date": 1631647493076},
            {"score": 1090, "bpm": 4.23, "date": 1631647493076},
            {"score": 1150, "bpm": 4.54, "date": 1631647493076},
            {"score": 1200, "bpm": 5.1, "date": 1631647493076}
        ]
    })
"""

def registerAtLoadBalancer(myIp, myPort, myName):
    regmsg = {"ip": myIp, "port": myPort, "name": myName, "type": "API"}
    endpoint = loadbalancerAddressAndPort + "/register"
    try:
        requests.post(url= endpoint, json= regmsg)
        print("Registered to load balancer")
        return True
    except:
        return False


def heartbeatTask(myIp, myName, isRegistered):
    """
    Send server metric to loadbalancer at even interval
    """
    while True:
        if isRegistered:
            try:
                endpoint = loadbalancerAddressAndPort + "/usage"
                metric = calculateMetric(myIp, myName)
                requests.post(url= endpoint, json= metric)
                
            except Exception as e:
                print("exception?")
        else:
            time.sleep(1)
        time.sleep(10)


 # TODO hardcoded for now, whatever ip/port of loadbalancer
loadbalancerAddressAndPort = "http://192.168.1.204:7777"

if __name__ == '__main__':
    try:
        myIp = sys.argv[1]
        myPort = sys.argv[2]
        myName = sys.argv[3]
    except:
        print("Usage guide: <arg1: ip> <arg2: port> <arg3: server name>")
        sys.exit()

    isRegistered = registerAtLoadBalancer(myIp, myPort, myName)
    Thread(target=heartbeatTask, args=(myIp, myName, isRegistered), daemon=True).start()
    app.run(host=myIp, port=myPort, debug=False)

