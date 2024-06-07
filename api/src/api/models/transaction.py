from __future__ import annotations
from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum, auto



class Transaction(SQLModel, table=True):
    """Model for a user transaction."""
    transaction_id: UUID = Field(default=uuid4(), primary_key=True)
    user_id: UUID = Field(foreign_key="user.user_id")
    session_id: UUID = Field(foreign_key="session.session_id")
    transaction_type: str = Field(sa_column_name="transaction_type")
    transaction_amount: float = Field(sa_column_name="transaction_amount")
    transaction_start_at: datetime = Field(sa_column_name="transaction_start_at", default=datetime.now())
    transaction_end_at: datetime = Field(sa_column_name="transaction_end_at", default=None)

    def __repr__(self):
        return f"<Transaction({self.transaction_id})>"

    def __str__(self):
        return f"Transaction {self.transaction_id} for {self.user_id}"