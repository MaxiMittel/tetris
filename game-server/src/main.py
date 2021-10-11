from flask import Flask, jsonify
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'CHANGE_SECRET!'
socketio = SocketIO(app)

# database or in memory storage room + players

@socketio.on('join')
def join(data):
    # data = {"room": "roomCode", "username": "Player0", "id": "f8hsdunjsdf"}
    # Save player to room
    send(jsonify({
        "action": "onJoin",
        "players": [
            {
                "username": "Player1",
                "id": "f8hsdunjsdf"
            }]}), broadcast=True)

@socketio.on('leave')
def leave(data):
    # data = {"room": "roomCode", "username": "Player0", "id": "f8hsdunjsdf"}
    # Save player to room
    send(jsonify({
        "action": "onLeave",
        "players": [
            {
                "username": "Player0",
                "id": "f8hsdunjsdf"
            },
            {
                "username": "Player1",
                "id": "f8hsdunjsdf"
            }]}), broadcast=True)

if __name__ == '__main__':
    socketio.run(app)


