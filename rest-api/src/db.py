from flask import jsonify
from flask_pymongo import pymongo
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.json_util import dumps
from bson.objectid import ObjectId
import jwt

SECRET = "CHANGE_SECRET"
def verify_jwt(token):
    try:
        return jwt.decode(token, SECRET, algorithms=['HS256'])
    except jwt.exceptions.InvalidSignatureError:
        return False
    except jwt.exceptions.DecodeError:
        return False

# Connection to monogodb atlas
dbUri = "mongodb+srv://dbUser:dbUserPassword@adstetriscluster.ecfwj.mongodb.net/tetris_db?retryWrites=true&w=majority"
mongo = pymongo.MongoClient(dbUri)
db = mongo.get_database('tetris_db')
userData = pymongo.collection.Collection(db, 'user_data')


def dbSignup(newAccount, username):
    try:
        userData.create_index([("username", pymongo.DESCENDING) ], unique=True)

    except Exception as e:
        msg = "Could not create unique value"
        return jsonify({"status": "error", "error": msg, "auth": "", "username": ""})

    try:
        result  = userData.insert_one(newAccount)
        
        if result.acknowledged:
            token = jwt.encode({"id": str(result.inserted_id)}, SECRET , algorithm="HS256")
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



def dbSignin(username, enteredPassword):
    try:
        projection = { "_id": 1, "username": 1, "password": 1}
        result = userData.find_one({"username": username}, projection)
        if(result):
            if result["password"] != enteredPassword:
                return jsonify({"status": "error", "error": "Wrong password", "username": ""})

            else:
                token = jwt.encode({"id": str(result["_id"])}, SECRET , algorithm="HS256")
                return jsonify({"status": "success", "error": "", "auth": token, "username": result["username"]})
        else:
           return jsonify({"status": "error", "error": "User not found", "username": ""}) 

    except OperationFailure:
        msg = "Operation failure"
        return jsonify({"status": "error", "error": msg, "auth": "", "username": ""})

    except Exception as e:
        return jsonify({"status": "error", "error": e.__class__.__name__, "username": ""})  



def dbGetUser(userID):
    try:
        if(userID != False):
            projection = {"_id": 1, "username": 1, "stats": 1}
            result  = userData.find_one( {"_id": ObjectId(userID["id"])}, projection)
            return jsonify({"status": "success", "error": "", "username": result["username"], "stats": result["stats"] })
        else:
            msg = "JWT encode error"
            return jsonify({"status": "error", "error": msg, "username": "", "stats": ""})

    except OperationFailure:
        msg = "Operation Failure"
        return jsonify({"status": "error", "error": msg, "username": "", "stats": ""})

    except Exception as e:
        return jsonify({"status": "error", "error": e.__class__.__name__, "username": "", "stats": ""})        



def dbUpdateUser(userID, newUsername):
    if(userID != False):
        try:
            filter = {"_id": ObjectId(userID["id"])}
            update = {"$set": {"username": newUsername} }
            result = userData.update_one(filter, update)

            if (result.modified_count > 0):
                newAuth = jwt.encode({"id": userID["id"]}, SECRET , algorithm="HS256")
                return jsonify({"status": "success", "error": "", "username": newUsername, "auth": newAuth})
            else:
                msg = "Failed to post update"
                return jsonify({"status": "error", "error": msg, "username": "", "auth": ""})

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
            filter = {"_id": ObjectId(userID["id"])}
            potentialHighscore = stat["score"]
            update = {"$push": {"stats": stat}, "$max": {"highscore": potentialHighscore}}
            result = userData.update_one(filter, update)

            if (result.modified_count > 0):
                return jsonify({"status": "success", "error": ""})
            else:
                msg = "Failed to post update"
                return jsonify({"status": "error", "error": msg, "username": "", "auth": ""})

        except OperationFailure:
            return jsonify({"status": "error", "error": "Operation Failure"})

        except Exception as e:
            return jsonify({"status": "error", "error": e.__class__.__name__})
    else:
        return jsonify({"status": "error", "error": "Incorrect authentication"})
        
        

def dbFindUsers(search):
    """
     # TODO returns in wierd format?
    """
    if(search):
        try:
            projection = {"_id": 1, "username": 1, "highscore": 1}
            cursor = userData.find({ "username": { "$regex": search } }, projection)
            list_cur = list(cursor)
            json_data = dumps(list_cur, indent = 2)
            return jsonify({"users": json_data})

        except OperationFailure:
            return jsonify({"users": ""})

        except Exception as e:
            return jsonify({"users": ""})
    else:
        return jsonify({"users": ""})


        
def dbFindUserById(userID):
    try:
        projection = {"_id": 1, "username": 1, "stats": 1}
        result = userData.find_one({"_id": ObjectId(userID) }, projection)
        if result:
            return jsonify({"id": str(result["_id"]), "username": result["username"], "stats": result["stats"]})
        else:
            return jsonify({"id": "", "username": "", "stats": ""}) 
    except OperationFailure:
        return jsonify({"id": "", "username": "", "stats": ""})

    except Exception as e:
        return jsonify({"id": "", "username": "", "stats": "", "error": e.__class__.__name__})
