#!/usr/bin/env python3
"""Session Authentication module"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """Implements session authentication for the current user"""
    user_id_by_session_id = {}
    def create_session(self, user_id: str = None) -> str:
        """Creates a session id for a user id"""
        if not (user_id and isinstance(user_id, str)):
            return None
        else:
            session_id = str(uuid.uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a user is based on a session id"""
        if not(session_id and isinstance(session_id, str)):
            return None
        return self.user_id_by_session_id.get(session_id)

