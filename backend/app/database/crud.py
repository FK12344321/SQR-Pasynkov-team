from typing import List

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.models import ActivityCreate, Activity, ActivitiesFilter
from app.database.models import Activity as DB_Activity

Base = declarative_base()
engine = create_engine('sqlite:///pasynkov.db')
session_maker = sessionmaker(bind=engine)


def create_activity(
        activity: ActivityCreate,
        username: str,
) -> Activity:
    session = session_maker()
    db_activity = DB_Activity(
        username=username,
        activity_type=activity.activity_type,
        start_date=activity.start_date,
        end_date=activity.end_date,
    )
    session.add(db_activity)
    session.commit()
    created_activity = Activity(
        id=db_activity.id,
        activity_type=db_activity.activity_type,
        start_date=db_activity.start_date,
        end_date=db_activity.end_date,
    )
    session.close()
    return created_activity


def get_activities(
        activity_params: ActivitiesFilter,
        username: str,
) -> List[Activity]:
    session = session_maker()
    conditions = [DB_Activity.username == username]

    if activity_params.start_date:
        condition = DB_Activity.start_date > activity_params.start_date
        conditions.append(condition)
    if activity_params.end_date:
        condition = DB_Activity.end_date > activity_params.end_date
        conditions.append(condition)
    if activity_params.activity_type:
        condition = DB_Activity.activity_type == activity_params.activity_type
        conditions.append(condition)

    offset = (activity_params.page_index - 1) * activity_params.page_size
    limit = activity_params.page_size

    query = session.query(DB_Activity).filter(*conditions) \
        .order_by(DB_Activity.start_date)\
        .limit(limit).offset(offset)

    activities = []
    for fetched_activity in query.all():
        activity = Activity(
            id=fetched_activity.id,
            activity_type=fetched_activity.activity_type,
            start_date=fetched_activity.start_date,
            end_date=fetched_activity.end_date,
        )
        activities.append(activity)
    return activities
