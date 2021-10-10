from flask import Flask, request, jsonify
from flask_cors import CORS
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

@app.route("/account/isAuthenticated")
def getAccount():
    token = request.headers.get("Authorization")
    token = token.replace("Bearer ", "")
    if not token:
        return jsonify({"error": "No token provided"}), 401
    if not verify_jwt(token):
        return jsonify({"error": "Invalid token"}), 401
    return jsonify({"message": "Success"})

@app.route("/account/signup", methods=['POST'])
def signup():
    userID = "fnsjdfmf2d9jiw"
    token = jwt.encode({"id": userID}, SECRET , algorithm="HS256")
    return jsonify({"auth": True, "id": userID, "token": token})

@app.route("/account/signin", methods=['POST'])
def signin():
    userID = "fnsjdfmf2d9jiw"
    token = jwt.encode({"id": userID}, SECRET, algorithm="HS256")
    return jsonify({"auth": True, "id": userID, "token": token})
    

@app.route("/user/search", methods=['GET'])
def search():
    return jsonify([{
        "id": "fnsjdfmf2d9jiw",
        "name": "John Lorenz Moser",
        "highscore": 1187,
    },{
        "id": "fnsjdfmf2d9jiw",
        "name": "Kristoffer Jonas Klauß",
        "highscore": 187,
    }])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)
