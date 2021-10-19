from flask import jsonify
from flask_pymongo import pymongo
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.json_util import dumps
from bson.objectid import ObjectId

# Connection to game_session collection
dbUri = "mongodb+srv://dbUser:dbUserPassword@adstetriscluster.ecfwj.mongodb.net/tetris_db?retryWrites=true&w=majority"
GSC = pymongo.collection.Collection(pymongo.MongoClient(dbUri).get_database('tetris_db'), 'game_session')


def dbAddGameSession(serverIp):
    try:
        result = GSC.insert_one({"ip": serverIp})
        
        if result.acknowledged:
            gameSessionId = result.inserted_id
            return jsonify({"status": "success", "error": "", "ip": serverIp, "id": str(gameSessionId)})
        else:
            msg = "Operation not acknowledged"
            return jsonify({"status": "error", "error": msg, "ip": "", "id": ""})

    except OperationFailure:
        msg = "Operation failure"
        return jsonify({"status": "error", "error": msg, "ip": "", "id": ""})

    except Exception as e:
        return jsonify({"status": "error", "error": e.__class__.__name__, "ip": "", "id": ""})



def dbRemoveGameSession(gameSessionId):
    try:
        result = GSC.delete_one({"_id": ObjectId(gameSessionId)})
        
        if result.deleted_count == 1:
            return jsonify({"status": "success", "error": ""})
        else:
            msg = "No Game session with this ID was found"
            return jsonify({"status": "error", "error": msg})

    except OperationFailure:
        msg = "Operation failure"
        return jsonify({"status": "error", "error": msg})

    except Exception as e:
        return jsonify({"status": "error", "error": e.__class__.__name__})



def dbCheckForGameSession(gameSessionId):
    """
    Returns ip for gamesession if the game session is in the db
    """
    try:
        result  = GSC.find_one( {"_id": ObjectId(gameSessionId) })
        
        if result:
            return jsonify({"status": "success", "error": "", "ip": result["ip"], "id": ""})

        else:
            return False

    except OperationFailure:
        msg = "Operation failure"
        return jsonify({"status": "error", "error": msg, "ip": "", "id": ""})

    except Exception as e:
        return jsonify({"status": "error", "error": e.__class__.__name__, "ip": "", "id": ""})  



def dbUpdateGameSessionHost(gameSessionId, serverIp):
    """
    Updates ip of a gamesession, migrating it to a new server
    """
    try:
        filter = {"_id": ObjectId(gameSessionId)}
        update = {"$set": {"ip": serverIp} }
        GSC.update_one(filter, update)
        return jsonify({"status": "success", "error": "", "ip": serverIp, "id": str(gameSessionId)})

    except OperationFailure:
        msg = "Operation failure"
        return jsonify({"status": "error", "error": msg, "ip": "", "id": ""})

    except Exception as e:
        return jsonify({"status": "error", "error": e.__class__.__name__, "ip": "", "id": ""})

   