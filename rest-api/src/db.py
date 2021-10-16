from enum import unique
from flask import jsonify
from flask_pymongo import pymongo
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.json_util import dumps
from bson.objectid import ObjectId

# Connection to monogodb atlas
dbUri = "mongodb+srv://dbUser:dbUserPassword@adstetriscluster.ecfwj.mongodb.net/tetris_db?retryWrites=true&w=majority"
mongo = pymongo.MongoClient(dbUri)
db = mongo.get_database('tetris_db')
userData = pymongo.collection.Collection(db, 'user_data')


def dbSignup(newAccount, username, token):
    try:
        userData.create_index([("username", pymongo.DESCENDING) ], unique=True)

    except Exception as e:
        print(e)
        msg = "Could not create unique value"
        return jsonify({"status": "error", "error": msg, "auth": "", "username": ""})

    try:
        result  = userData.insert_one(newAccount)

        if result .acknowledged:
            return jsonify({"status": "success", "error": "", "auth": token, "username": username})
        else:
            msg = "Operation not acknowledged"
            return jsonify({"status": "error", "error": msg, "auth": "", "username": ""})

    except DuplicateKeyError:
        msg = "Duplicate key/username"
        return jsonify({"status": "error", "error": msg, "auth": "", "username": ""})

    except OperationFailure:
        msg = "Operation failure"
        return jsonify({"status": "error", "error": msg, "auth": "", "username": ""})

    except Exception as e:
        return jsonify({"status": "error", "error": e.__class__.__name__, "auth": "", "username": ""})



def dbSignin(userID, enteredPassword):
    try:
        projection = { "_id": 0, "username": 1, "password": 1, "auth": 1}
        result  = userData.find_one( {"username": userID }, projection)
        
        if result ["password"] != enteredPassword:
            return jsonify({"status": "error", "error": "Wrong password", "auth": "", "username": ""})

        else:
            return jsonify({"status": "success", "error": "", "auth": result["auth"], "username": result["username"]})

    except OperationFailure:
        msg = "Operation failure"
        return jsonify({"status": "error", "error": msg, "auth": "", "username": ""})

    except Exception as e:
        return jsonify({"status": "error", "error": e.__class__.__name__, "username": ""})  



def dbGetUser(userID):
    try:
        if(userID != False):
            projection = { "_id": 0, "username": 1, "stats": 1}
            result  = userData.find_one( {"username": userID["id"]}, projection)
            return jsonify({"status": "success", "error": "", "username": result["username"], "stats": result["stats"] })
        else:
            msg = "JWT encode error"
            return jsonify({"status": "error", "error": msg, "username": "", "stats": ""})

    except OperationFailure:
        msg = "Operation Failure"
        return jsonify({"status": "error", "error": msg, "username": "", "stats": ""})

    except Exception as e:
        return jsonify({"status": "error", "error": e.__class__.__name__, "username": "", "stats": ""})        



def dbUpdateUser(userID, newUsername, newAuth):
    if(userID != False):
        try:
            filter = {"username": userID["id"]}
            update = {"$set": {"username": newUsername, "auth": newAuth} }
            userData.update_one(filter, update)
            return jsonify({"status": "success", "error": "", "username": newUsername, "auth": newAuth})

        except OperationFailure:
            msg = "Operation failure"
            return jsonify({"status": "error", "error": msg, "username": "", "auth": ""})

        except Exception as e:
            return jsonify({"status": "error", "error": e.__class__.__name__, "username": "", "auth": ""})
    else:
        return jsonify({"status": "error", "error": "Incorrect authentication"})



def dbPostStat(userID, stat):
    if(userID != False):
        try:
            filter = {"username": userID["id"]}
            potentialHighscore = stat["score"]
            update = {"$push": {"stats": stat}, "$max": {"highscore": potentialHighscore}}
            userData.update_one(filter, update)
            return jsonify({"status": "success", "error": ""})

        except OperationFailure:
            return jsonify({"status": "error", "error": "Operation Failure"})

        except Exception as e:
            return jsonify({"status": "error", "error": e.__class__.__name__})
    else:
        return jsonify({"status": "error", "error": "Incorrect authentication"})
        
        

def dbFindUsers(userList):
    if(userList):
        try:
            projection = {"_id": 1, "username": 1, "highscore": 1}
            cursor = userData.find({ "username": { "$in": userList } }, projection )
            list_cur = list(cursor)
            json_data = dumps(list_cur)
            return jsonify({"users": json_data})

        except OperationFailure:
            return jsonify({"users": ""})

        except Exception as e:
            return jsonify({"users": ""})
    else:
        return jsonify({"users": ""})


        
def dbFindUserById(id):
    try:
        projection = {"_id": 1, "username": 1, "stats": 1}
        result = userData.find_one({"_id": ObjectId(id) }, projection)
        return jsonify({"id": str(result["_id"]), "username": result["username"], "stats": result["stats"]})

    except OperationFailure:
        return jsonify({"id": "", "username": "", "stats": ""})

    except Exception as e:
        return jsonify({"id": "", "username": "", "stats": "", "error": e.__class__.__name__})
