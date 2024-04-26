from typing import List
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.models import User
from app.database.models import User as DB_User, Activity
from app.database.crud import session_maker


def get_user_by_username(username: str) -> User:
    session = session_maker()
    db_user = session.query(DB_User).filter_by(username=username).first()
    session.close()
    if db_user is None:
        raise ValueError("User not found")
    return User(
        username=db_user.username,
        password=db_user.password,
    )


def create_user(user: User) -> User:
    session = session_maker()
    new_user = DB_User(
        username=user.username,
        password=user.password,
    )
    session.add(new_user)
    session.commit()

    return get_user_by_username(user.username)


def update_user(user: User) -> User:
    session = session_maker()
    db_user = session.query(DB_User).filter_by(username=user.username).first()

    db_user.password = user.password
    db_user.updated_at = datetime.utcnow()
    session.commit()

    return get_user_by_username(user.username)
