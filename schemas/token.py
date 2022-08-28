# pylint: disable=import-error
"""Token schema definitions"""

from pydantic import BaseModel


class TokenPayload(BaseModel):
    """Token payload"""
    exp: int
    sub: str
