import uuid

class SessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self):
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {}
        return session_id

    def get_session(self, session_id):
        return self.sessions.get(session_id, {})

session_manager = SessionManager()
