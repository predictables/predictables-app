from __future__ import annotations
from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4
from datetime import datetime

class User(SQLModel, table=True):
    """Model for a user."""
    user_id: UUID = Field(default=uuid4(), primary_key=True)
    username: str = Field(sa_column_name="username")
    password: str = Field(sa_column_name="hashed_password")
    display_name: str  = Field(sa_column_name="display_name")
    email: str = Field(sa_column_name="email")
    is_registered: bool = Field(sa_column_name="is_registered", default=False)
    registered_at: datetime = Field(sa_column_name="registered_at", default=None)
    last_login_at: datetime = Field(sa_column_name="last_login_at", default=None)

    def __repr__(self):
        return f"<{'Registered' if self.is_registered else 'Unregistered'}User({self.display_name})>"

    def __str__(self):
        return f"{self.display_name} ({self.username})"



