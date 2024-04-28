from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime  # noqa: E501
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from app.config import get_settings


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    username = Column(String, primary_key=True, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    activities = relationship('Activity', back_populates='user')


class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True)
    activity_type = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    username = Column(Integer, ForeignKey('users.username'))
    user = relationship('User', back_populates='activities')


settings = get_settings()
engine = create_engine('sqlite://' + settings.db_file_path)
Base.metadata.create_all(engine)
session_maker = sessionmaker(bind=engine)
