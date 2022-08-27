# pylint: disable=import-error
"""Contains hashing functions"""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher():
    """Hash functions"""
    @staticmethod
    def verify_password(password, hashed_password):
        """Verifies the password matches the hashed_password"""
        return pwd_context.verify(password, hashed_password)

    @staticmethod
    def hash_password(password):
        """Hashs the password"""
        return pwd_context.hash(password)
