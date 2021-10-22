from flask import jsonify
from flask_pymongo import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from dotenv import load_dotenv, find_dotenv
import json
import os

load_dotenv(find_dotenv())

# Connection to game_session collection
dbUri = "mongodb+srv://{}:{}@adstetriscluster.ecfwj.mongodb.net/tetris_db?retryWrites=true&w=majority".format(os.environ.get("DB_USER"), os.environ.get("DB_PASSWORD"))
GSC = pymongo.collection.Collection(pymongo.MongoClient(dbUri).get_database('tetris_db'), 'game_session')

def dbGetGameSessions():
    try:
        result = list(GSC.find())
        return jsonify({"status": "success", "sessions": json.loads(dumps(result))})
    except Exception as e:
        return jsonify({"status": "error"})


def dbAllocate(serverIp, serverPort, name):
    try:
        result = GSC.insert_one({"ip": serverIp, "port": serverPort, "name": name})
        
        if result.acknowledged:
            gameSessionId = result.inserted_id
            return jsonify({"status": "success", "id": str(gameSessionId)})
        else:
            msg = "Operation not acknowledged"
            return jsonify({"status": "error", "error": msg})

    except Exception as e:
        return jsonify({"status": "error", "error": e.__class__.__name__})



def dbRemoveGameSession(id):
    try:
        result = GSC.delete_one({"_id": ObjectId(id)})
        
        if result.deleted_count == 1:
            return jsonify({"status": "success"})
        else:
            msg = "No Game session with this ID was found"
            return jsonify({"status": "error", "error": msg})

    except Exception as e:
        return jsonify({"status": "error", "error": e.__class__.__name__})



def dbGetSingleGameSession(gameSessionId):
    """
    Returns ip for gamesession if the game session is in the db
    """
    try:
        result  = GSC.find_one( {"_id": ObjectId(gameSessionId) })
        if result:
            return jsonify({"status": "success", "ip": result["ip"], "port": result["port"]})
        else:
            return False

    except Exception as e:
        return jsonify({"status": "error"})  


   