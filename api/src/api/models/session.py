from __future__ import annotations
from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4
from datetime import datetime


class Session(SQLModel, table=True):
    """Model for a user session."""

    session_id: UUID = Field(default=uuid4(), primary_key=True)
    user_id: UUID = Field(foreign_key="user.user_id")
    session_token: str
    is_active: bool = Field(default=True)
    started_at: datetime = Field(default=datetime.now())
    last_accessed_at: datetime = Field(default=datetime.now())
    ended_at: datetime = Field(default=None)

    def __repr__(self):
        return (
            f"<{'Active' if self.is_active else 'Inactive'}Session({self.session_id})>"
        )

    def __str__(self):
        return f"Session {self.session_id} for {self.user_id}"
