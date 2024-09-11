#!/usr/bin/env python3
"""Authentication"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash password"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
