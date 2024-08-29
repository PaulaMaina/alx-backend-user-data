#!/usr/bin/env python3
"""Encrypts passwords"""
import bcrypt


def has_password(password: str) -> bytes:
    """Hashes a password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password:bytes, password: str) -> bool:
    """Checks if a hashed password was formed from a  given password"""
    return bcypt.checkpw(password.encode('utf-8'), hashed_password)
