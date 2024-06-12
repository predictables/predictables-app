from __future__ import annotations
from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4
from datetime import datetime


class User(SQLModel, table=True):
    """Model for a user."""

    user_id: UUID = Field(default=uuid4(), primary_key=True)
    username: str
    password: str
    display_name: str
    email: str
    is_registered: bool
    registered_at: datetime
    last_login_at: datetime

    def __repr__(self):
        return f"<{'Registered' if self.is_registered else 'Unregistered'}User({self.display_name})>"

    def __str__(self):
        return f"{self.display_name} ({self.username})"
