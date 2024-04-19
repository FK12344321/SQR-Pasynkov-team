from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    username = Column(String)

    activities = relationship('Activity', back_populates='user')


class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True)
    activity_type = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    username = Column(Integer, ForeignKey('users.username'))
    user = relationship('User', back_populates='activities')


engine = create_engine('sqlite:///pasynkov.db')
Base.metadata.create_all(engine)
