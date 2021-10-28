from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
from game_state import GameState
import directory
import socket
import sys
from dotenv import load_dotenv, find_dotenv
import multiprocessing
import time
import os

load_dotenv(find_dotenv())

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET')
socketio = SocketIO(app, cors_allowed_origins="*")

game = {} # {room: GameState}
clients = {} # {sid: room}

def printGames():
    for room in game:
        print("ROOM", room)
        for player in game[room].get_players():
            print(player)

"""
Client joins a room
"""
@socketio.on('join')
def join(data):
    room = data['room']
    username = data['username']
    id = data['id']
    sid = request.sid

    join_room(sid)
    clients[sid] = room

    if room not in game:
        game[room] = GameState([], [])

    game[room].add_player(username, id, sid)

    printGames()

    sendAll('onJoin', room, {"players": game[room].get_players(), "field": game[room].get_field()})

"""
Client disconnects
"""
@socketio.on('disconnect')
def on_disconnect():
    sid = request.sid

    leave_room(sid)
    room = clients[sid]
    game[room].remove_player(sid)
    clients.pop(sid, None)

    if game[room].is_empty():
        game.pop(room, None)
        return

    sendAll('onLeave', room, game[room].get_players())

"""
Client in the lobby changes to ready
"""
@socketio.on("playerReady")
def player_ready(data):
    room = data['room']
    id = data['id']

    game[room].set_player_ready(id)

    if game[room].is_ready():
        sendAll('onGameStart', room, game[room].get_players())
    else:
        sendAll('onPlayerReady', room, game[room].get_players())

"""
Update a player's position
"""
@socketio.on('playerUpdate')
def player_update(data):
    room = data['room']
    id = data['id']

    game[room].update_player(id, data["block"])

    sendAll('onPlayerUpdate', room, game[room].get_players())

"""
Update the game field
"""
@socketio.on('fieldUpdate')
def field_update(data):
    room = data['room']
    gameField = data['field']

    # Check if block in first row -> game lost
    for block in gameField[0]:
        if block != 0:
            sendAll('onGameOver', room, {"score": game[room].get_score()})
            break

    completeRows = []

    # Search for complete rows
    for row in gameField:
        isComplete = True
        for block in row:
            if block == 0:
                isComplete = False
                break

        if isComplete:
            completeRows.append(row)

    game[room].add_score(len(completeRows))

    # Remove complete rows
    for row in completeRows:
        gameField.remove(row)

    # Add new row
    for _ in range(len(completeRows)):
        gameField.insert(0, [0] * 30)

    game[room].set_field(gameField)

    sendAll('onFieldUpdate', room, gameField)

"""
Send a chat message
"""
@socketio.on("chatMessage")
def chat_message(data):
    room = data['room']
    message = data['msg']

    sendAll("onChatMessage", room, {"message": message})

"""
Migrate an game session froma another server
"""
@socketio.on('migrate')
def migrate(data):
    room = data['room']
    gameField = data['field']
    players = data['players']

    if room not in game:
        game[room] = GameState(players, gameField)

    sendAll('onMigrate', room, game[room].get_players())

@app.route("/ping")
def ping():
    return "pong", 200

"""
Send a message to all clients in a room
"""
def sendAll(action, room, message):
    for client in game[room].get_clients():
        emit(action, message, room=client)

def Server(host,port):
    socketio.run(app, host=host, port=port)

if __name__ == '__main__':

    if len(sys.argv) == 3:
        host = "0.0.0.0"
        port = int(sys.argv[1])
        name = sys.argv[2]

        server_process = multiprocessing.Process(target=Server, args=(host, port))
        server_process.start()

        # Wait 2 seconds then try until registration was successful
        time.sleep(2)
        is_Registered = directory.registerService(os.environ.get("PUBLIC_IP"), port, name, "GS")
        while not is_Registered:
            app.logger.info("Connection to directory service was unsuccessfull. Retrying in 2s.")
            time.sleep(2)
            is_Registered = directory.registerService(os.environ.get("PUBLIC_IP"), port, name, "GS")
        app.logger.info("Connection to directory service was successfull")
    else:
        print("Usage: python main.py <port> <name>")
        exit()