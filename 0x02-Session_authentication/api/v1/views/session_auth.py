#!/usr/bin/env python3
"""Session Authentication view"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from typing import Tuple
import os


@app_views.route(
        '/auth_session/login',
        methods=['POST'],
        strict_slashes=False)
def login() -> Tuple[str, int]:
    """Session login method for the user"""
    no_user_res = {"error": "no user found for this email"}
    email = request.form.get('email')
    pwd = request.form.get('password')
    if email is None or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400
    if pwd is None or len(pwd.strip()) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify(no_user_res), 404
    if len(users) <= 0:
        return jsonify(no_user_res), 404

    if users[0].is_valid_password(pwd):
        from api.v1.app import auth
        sess_id = auth.create_session(getattr(users[0], 'id'))
        cookie = jsonify(users[0].to_json())
        cookie.set_cookie(os.getenv('SESSION_NAME'), sess_id)
        return cookie
    return jsonify({"error": "wrong password"}), 401


@app_views.route(
        '/auth_session/logout',
        methods=['DELETE'],
        strict_slashes=False)
def logout() -> Tuple[str, int]:
    """Deletes the user session"""
    from api.v1.app import auth
    sess_destroyed = auth.destroy_session(request)
    if not sess_destroyed:
        abort(404)
    return jsonify({})
