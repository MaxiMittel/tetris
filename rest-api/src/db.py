from flask import jsonify
from flask_pymongo import pymongo
from pymongo.errors import DuplicateKeyError, OperationFailure

dbUri = "mongodb+srv://dbUser:dbUserPassword@adstetriscluster.ecfwj.mongodb.net/tetris_db?retryWrites=true&w=majority"
mongo = pymongo.MongoClient(dbUri)
db = mongo.get_database('tetris_db')
userData = pymongo.collection.Collection(db, 'user_data')


def dbSignup(newAccount, token):
    try:
        ret = userData.insert_one(newAccount)

        if ret.acknowledged:
            return jsonify({"status": "success", "error": "", "auth": token, "username": ret.inserted_id})
        else:
            msg = "Operation not acknowledged"
            return jsonify({"status": "error", "error": msg, "auth": "", "username": ""})

    except DuplicateKeyError:
        msg = "Duplicate key/username"
        return jsonify({"status": "error", "error": msg, "auth": "", "username": ""})
    except OperationFailure:
        msg = "Operation failure"
        return jsonify({"status": "error", "error": msg, "auth": "", "username": ""})


def dbSignin(userID,enteredPassword):
    try:
        # TODO Projection cause exception ???
        #projection = { "_id": 1, "password": 1, "mail": 0, "auth": 1, "stats": 0}
        user = userData.find_one( {'_id': userID})#, projection)
        
        if user["password"] != enteredPassword:
            return jsonify({"status": "error", "error": "Wrong password", "auth": "", "username": ""})

        else:
            return jsonify({"status": "success", "error": "", "auth": user["auth"], "username": user["_id"]})

    except DuplicateKeyError:
        msg = "Duplicate key/username"
        return jsonify({"status": "error", "error": msg, "auth": "", "username": ""})
    except OperationFailure:
        msg = "Operation failure"
        return jsonify({"status": "error", "error": msg, "auth": "", "username": ""})