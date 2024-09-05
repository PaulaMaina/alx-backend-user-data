#!/usr/bin/env python3
"""SessionDBAuth"""
from .session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Stores session IDs in database"""

    def create_session(self, user_id=None):
        """Creates and stores a new instance of UserSession"""
        session_id = super().create_session(user_id)
        if isinstance(session_id, str):
            kwargs = {
                'user_id': user_id,
                'session_id': session_id,
            }
            session = UserSession(**kwargs)
            session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """Returns the user ID by requesting UserSession session ID"""
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        curr_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        expire_time = sessions[0].created_at + time_span
        if expire_time < curr_time:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """Destroys the UserSesssion based on the session ID"""
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
