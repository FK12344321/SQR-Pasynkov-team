from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from backend.app.models import ActivityCreate

Base = declarative_base()
engine = create_engine('sqlite:///pasynkov.db')
session_maker = sessionmaker(bind=engine)

def create_activity(activity: ActivityCreate):
    session = session_maker()
    db_user = session.query(User).filter_by(id=user_id).first()
    if db_user is None:
        session.close()
        raise HTTPException(status_code=404, detail="User not found")
    db_activity = Activity(**activity.dict(), user=db_user)
    session.add(db_activity)
    session.commit()
    session.close()
    return db_activity