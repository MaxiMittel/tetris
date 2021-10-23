from flask import jsonify
from flask_pymongo import pymongo
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.json_util import dumps
from bson.objectid import ObjectId
import jwt
import hashlib
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

SECRET = os.environ.get("SECRET")

"""
Checks if a JWT token is valid
"""
def verify_jwt(token):
    try:
        return jwt.decode(token, SECRET, algorithms=['HS256'])
    except jwt.exceptions.InvalidSignatureError:
        return False
    except jwt.exceptions.DecodeError:
        return False

"""
Retrieves the data from a JWT token
"""
def decode_jwt(token):
    return jwt.decode(token, SECRET, algorithms=['HS256'])

"""
Encode the supplied data to a JWT token
"""
def encode_jwt(data):
    return jwt.encode(data, SECRET, algorithm="HS256")

# Connection to monogodb atlas
dbUri = "mongodb+srv://{}:{}@adstetriscluster.ecfwj.mongodb.net/tetris_db?retryWrites=true&w=majority".format(os.environ.get("DB_USER"), os.environ.get("DB_PASSWORD"))
mongo = pymongo.MongoClient(dbUri)
db = mongo.get_database('tetris_db')
userData = pymongo.collection.Collection(db, 'user_data')


def dbSignup(newAccount, username):
    try:
        userData.create_index([("username", pymongo.DESCENDING) ], unique=True)

    except Exception as e:
        msg = "Could not create unique value"
        return jsonify({"status": "error", "error": msg}), 500

    try:
        result  = userData.insert_one(newAccount)
        
        if result.acknowledged:
            token = encode_jwt({"id": str(result.inserted_id)})
            return jsonify({"status": "success", "auth": token, "username": username})
        else:
            msg = "Operation not acknowledged"
            return jsonify({"status": "error", "error": msg}), 500

    except DuplicateKeyError:
        msg = "Duplicate key/username"
        return jsonify({"status": "error", "error": msg}), 400

    except OperationFailure:
        msg = "Operation failure"
        return jsonify({"status": "error", "error": msg}), 500

    except Exception as e:
        return jsonify({"status": "error", "error": e.__class__.__name__}), 500



def dbSignin(username, enteredPassword):
    try:
        projection = { "_id": 1, "username": 1, "password": 1}
        result = userData.find_one({"username": username}, projection)
        if(result):
            if result["password"] != enteredPassword:
                return jsonify({"status": "error", "error": "Wrong password"}), 403
            else:
                token = encode_jwt({"id": str(result["_id"])})
                return jsonify({"status": "success", "error": "", "auth": token, "username": result["username"]})
        else:
           return jsonify({"status": "error", "error": "User not found"}), 404

    except OperationFailure:
        msg = "Operation failure"
        return jsonify({"status": "error", "error": msg}), 500

    except Exception as e:
        return jsonify({"status": "error", "error": e.__class__.__name__}), 500



def dbGetUser(userID):
    try:
        if(userID != False):
            projection = {"_id": 1, "username": 1, "stats": 1}
            result  = userData.find_one( {"_id": ObjectId(userID["id"])}, projection)
            return jsonify({"status": "success", "error": "", "username": result["username"], "stats": result["stats"] })
        else:
            msg = "JWT encode error"
            return jsonify({"status": "error", "error": msg}), 400

    except OperationFailure:
        msg = "Operation Failure"
        return jsonify({"status": "error", "error": msg}), 500

    except Exception as e:
        return jsonify({"status": "error", "error": e.__class__.__name__}), 500        



def dbUpdateUser(userID, newUsername):
    if(userID != False):
        try:
            filter = {"_id": ObjectId(userID["id"])}
            update = {"$set": {"username": newUsername} }
            result = userData.update_one(filter, update)

            if (result.modified_count > 0):
                newAuth = encode_jwt({"id": userID["id"]})
                return jsonify({"status": "success", "username": newUsername, "auth": newAuth})
            else:
                msg = "Failed to post update"
                return jsonify({"status": "error", "error": msg}), 400

        except OperationFailure:
            msg = "Operation failure"
            return jsonify({"status": "error", "error": msg}), 500

        except Exception as e:
            return jsonify({"status": "error", "error": e.__class__.__name__}), 500
    else:
        return jsonify({"status": "error", "error": "Incorrect authentication"}), 403



def dbPostStat(userID, stat):
    if(userID != False):
        try:
            filter = {"_id": ObjectId(userID["id"])}
            potentialHighscore = stat["score"]
            update = {"$push": {"stats": stat}, "$max": {"highscore": potentialHighscore}}
            result = userData.update_one(filter, update)

            if (result.modified_count > 0):
                return jsonify({"status": "success"})
            else:
                msg = "Failed to post update"
                return jsonify({"status": "error", "error": msg}), 400

        except OperationFailure:
            return jsonify({"status": "error", "error": "Operation Failure"}), 500

        except Exception as e:
            return jsonify({"status": "error", "error": e.__class__.__name__}), 500
    else:
        return jsonify({"status": "error", "error": "Incorrect authentication"}), 403
        
        

def dbFindUsers(search):
    """
     # TODO returns in wierd format?
    """
    if(search):
        try:
            projection = {"_id": 1, "username": 1, "highscore": 1}
            cursor = userData.find({ "username": { "$regex": search } }, projection)

            users = []
            for doc in cursor:
                users.append({"id": str(doc["_id"]), "username": doc["username"], "highscore": doc["highscore"]})

            return jsonify({"users": users})

        except OperationFailure:
            return jsonify({"users": []})

        except Exception as e:
            return jsonify({"users": []})
    else:
        return jsonify({"users": []})


        
def dbFindUserById(userID):
    try:
        projection = {"_id": 1, "username": 1, "stats": 1, "highscore": 1}
        result = userData.find_one({"_id": ObjectId(userID) }, projection)
        if result:
            return jsonify({"id": str(result["_id"]), "username": result["username"], "stats": result["stats"], "highscore": result["highscore"]})
        else:
            return jsonify({"error": "User not found"}), 404 
    except OperationFailure:
        return jsonify({"error": "User not found"}), 500

    except Exception as e:
        return jsonify({"error": e.__class__.__name__}), 500

def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()