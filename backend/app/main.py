from fastapi import FastAPI, HTTPException
from models import Session, Activity, User
from schemas import ActivityCreate

app = FastAPI()


@app.post("/users/{user_id}/activities/", response_model=ActivityCreate)
def create_activity(user_id: int, activity: ActivityCreate):
    session = Session()
    db_user = session.query(User).filter_by(id=user_id).first()
    if db_user is None:
        session.close()
        raise HTTPException(status_code=404, detail="User not found")
    db_activity = Activity(**activity.dict(), user=db_user)
    session.add(db_activity)
    session.commit()
    session.close()
    return db_activity


@app.get("/health")
def health_check():
    return "OK"
