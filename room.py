class Room:
    def __init__(self, id):
        self.id = id
        self.users = set()
        self.sessions = {}
        self.game = None
        self.chat = []

    def session_connect(self, username, sess_id):
        if (username not in self.users):
            self.users.add(username)
        
        assert(sess_id not in self.sessions)
        self.sessions[sess_id] = username


    def session_disconnect(self, sess_id):
        assert(sess_id in self.sessions)
        username = self.sessions[sess_id]
        del self.sessions[sess_id]
        return username

