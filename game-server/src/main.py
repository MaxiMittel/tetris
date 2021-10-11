from flask import Flask, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'CHANGE_SECRET!'
socketio = SocketIO(app, cors_allowed_origins="*")

database = {} # {'room_name': {'players': [{'sid': string, 'username': string, 'id': string}], 'game': {'field': []}}}

@socketio.on('join')
def join(data):
    room_name = data['room']
    username = data['username']
    id = data['id']
    sid = request.sid

    join_room(room_name)

    if room_name not in database:
        database[room_name] = {'players': [], 'game': {'field': []}}
    else:
        # TODO: check if player is already in room
        database[room_name]['players'].append({'sid': sid, 'username': username, 'id': id})

    emit('onJoin', {"players": database[room_name]['players']}, room=room_name)
        

@socketio.on('leave')
def leave(data):
    room_name = data['room']
    sid = request.sid

    leave_room(room_name)

    if room_name in database:
        database[room_name]['players'] = [player for player in database[room_name]['players'] if player['sid'] != sid]

    emit('onLeave', {"players": database[room_name]['players']}, room=room_name)

@socketio.on('playerUpdate')
def player_update(data):
    room_name = data['room']
    id = data['id']
    block = data['block']

    emit('onPlayerUpdate', {"id": id, "player": block}, room=room_name)

@socketio.on('fieldUpdate')
def field_update(data):
    room_name = data['room']
    field = data['field']

    #TODO: check if row is complete

    emit('onFieldUpdate', {"field": field}, room=room_name)


if __name__ == '__main__':
    socketio.run(app, debug=True)


