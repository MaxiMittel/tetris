from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'CHANGE_SECRET!'
socketio = SocketIO(app, cors_allowed_origins="*")

clients = []
players = []
gameField = []

@socketio.on('join')
def join(data):
    username = data['username']
    id = data['id']

    join_room(request.sid)

    clients.append(request.sid)
    players.append({'username': username, "sid": request.sid, 'id': id, "ready": False, "block": False})

    sendAll('onJoin', players)

@socketio.on('leave')
def on_leave():
    sid = request.sid
    print("leave")

    leave_room(sid)

    for i in range(len(players)):
        if players[i]['sid'] == sid:
            del players[i]
            break

    for i in range(len(clients)):
        if clients[i] == sid:
            del clients[i]
            break

    sendAll('onLeave', players)

@socketio.on('disconnect')
def on_disconnect():
    sid = request.sid
    print("disconnect")

    leave_room(sid)

    for i in range(len(players)):
        if players[i]['sid'] == sid:
            del players[i]
            break

    for i in range(len(clients)):
        if clients[i] == sid:
            del clients[i]
            break

    sendAll('onLeave', players)

@socketio.on("playerReady")
def player_ready(data):
    id = data['id']

    for player in players:
        if player['id'] == id:
            player['ready'] = True

    all_ready = all([player['ready'] for player in players])

    print(players)

    if all_ready:
        sendAll('onGameStart', players)
    else:
        sendAll('onPlayerReady', players)

@socketio.on('playerUpdate')
def player_update(data):
    id = data['id']

    for player in players:
        if player['id'] == id:
            player['block'] = data['block']

    sendAll('onPlayerUpdate', players)

@socketio.on('fieldUpdate')
def field_update(data):
    gameField = data['field']

    #TODO: check if row is complete

    sendAll('onFieldUpdate', gameField)

@socketio.on("chatMessage")
def chat_message(data):
    message = data['msg']

    sendAll("onChatMessage", {"message": message})

def sendAll(action, message):
    for client in clients:
        emit(action, message, room=client)

if __name__ == '__main__':
    socketio.run(app, debug=True)