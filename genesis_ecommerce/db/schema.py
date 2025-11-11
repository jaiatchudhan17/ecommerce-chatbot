from datetime import datetime

from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class Users(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime
    updated_at: datetime


class Orders(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    items: list[str] = Field(sa_column=Column(JSON))
    status: str
    created_at: datetime
    updated_at: datetime


class Tickets(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id")
    issue_description: str
    status: str
    created_at: datetime
    updated_at: datetime
