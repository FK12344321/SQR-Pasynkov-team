from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from backend.app.models import ActivityCreate
from backend.app.database.models import User, Activity

Base = declarative_base()
engine = create_engine('sqlite:///pasynkov.db')
session_maker = sessionmaker(bind=engine)


def create_activity(activity: ActivityCreate, username: str):
    session = session_maker()
    db_user = session.query(User).filter_by(username=username).first()
    if db_user is None:
        session.close()
        raise ValueError("No such user")
    db_activity = Activity(start_date=activity.start_date,
                           end_date=activity.end_date,
                           activity_type=activity.activity_type)
    session.add(db_activity)
    session.commit()
    session.close()
    return db_activity
