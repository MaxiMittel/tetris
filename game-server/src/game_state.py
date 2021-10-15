class GameState:

    def __init__(self):
        self.clients = []
        self.players = []
        self.gameField = []
        self.score = 0

    def add_player(self, username, id, sid):
        self.players.append({'username': username, "sid": sid, 'id': id, "ready": False, "block": False})
        self.clients.append(sid)

    def remove_player(self, sid):
        self.clients.remove(sid)
        self.players = [player for player in self.players if player['sid'] != sid]

    def set_player_ready(self, id):
        for player in self.players:
            if player['id'] == id:
                player['ready'] = True

    def update_player(self, id, block):
        for player in self.players:
            if player['id'] == id:
                player['block'] = block

    def add_score(self, score):
        self.score += score

    def is_ready(self):
        return all([player['ready'] for player in self.players])

    def set_field(self, field):
        self.gameField = field

    def get_players(self):
        return self.players

    def get_clients(self):
        return self.clients

    def is_empty(self):
        return len(self.clients) == 0