from typing import List

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.models import ActivityCreate, Activity, ActivitiesRequest
from app.database.models import User, Activity

Base = declarative_base()
engine = create_engine('sqlite:///pasynkov.db')
session_maker = sessionmaker(bind=engine)


def create_activity(activity: ActivityCreate, username: str) -> Activity:
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
    created_activity = Activity(activity_type=db_activity.activity_type,
                                start_date=db_activity.start_date,
                                end_date=db_activity.end_date,
                                id=db_activity.id)
    session.close()
    return created_activity


def get_activities(activity_params: ActivitiesRequest, username: str) -> List[Activity]:
    session = session_maker()
    db_user = session.query(User).filter_by(username=username).first()
    if db_user is None:
        session.close()
        raise ValueError("No such user")

    conditions = []

    if activity_params.start_date:
        condition = Activity.start_date > activity_params.start_date
        conditions.append(condition)
    if activity_params.end_date:
        condition = Activity.end_date > activity_params.end_date
        conditions.append(condition)
    if activity_params.activity_type:
        condition = Activity.activity_type == activity_params.activity_type
        conditions.append(condition)

    offset = (activity_params.page_index - 1) * activity_params.page_size
    limit = activity_params.page_size

    query = session.query(Activity).filter(*conditions) \
        .order_by(Activity.start_date)\
        .limit(limit).offset(offset)

    activities = []

    for fetched_activity in query.all():
        activity = Activity(activity_type=fetched_activity.activity_type,
                            start_date=fetched_activity.start_date,
                            end_date=fetched_activity.end_date,
                            id=fetched_activity.id)
        activities.append(activity)
    return activities
