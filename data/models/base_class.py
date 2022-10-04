# pylint: disable=import-error
"""Base class for database model classes"""

from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """Base class, db classes will inherit from this class"""
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(self, cls) -> str:
        return cls.__name__.lower()
