import string
from fastapi.testclient import TestClient
from app.main import app
import random
from datetime import datetime
from requests.auth import HTTPBasicAuth
import json

client = TestClient(app)

USERNAME = ''.join(random.choices(string.ascii_uppercase
                                  + string.digits, k=30))
PASSWORD = ''.join(random.choices(string.ascii_uppercase
                                  + string.digits, k=30))
ACTIVITY_TYPES = ['sport', 'work', 'study']
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def get_activities():
    activities = []
    for year in range(2000, 2020):
        start_date = f"{year}-01-01T00:00:00.000000Z"
        end_date = f"{year}-01-01T00:01:00.000000Z"
        activity_type = ACTIVITY_TYPES[year % 3]
        activities.append({
           "start_date": start_date,
           "end_date": end_date,
           "activity_type": activity_type,
        })
    return activities


def compare_activity(activity, response_body):
    assert response_body['activity_type'] == activity['activity_type']
    assert datetime.strptime(response_body['start_date'],
                             "%Y-%m-%dT%H:%M:%S") == datetime.strptime(
                                 activity['start_date'],
                                 "%Y-%m-%dT%H:%M:%S.%fZ")
    assert datetime.strptime(response_body['end_date'],
                             "%Y-%m-%dT%H:%M:%S") == datetime.strptime(
                                 activity['end_date'],
                                 "%Y-%m-%dT%H:%M:%S.%fZ")
    assert 'id' in response_body


def test_integration():
    body = {
        "username": USERNAME,
        "password": PASSWORD,
    }
    response = client.post('/auth/register', data=json.dumps(body))
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

    basic_auth = HTTPBasicAuth(USERNAME, PASSWORD)
    response = client.get('/auth/login', auth=basic_auth)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    refresh_token = response.json()["refresh_token"]

    response = client.post('/activity')
    headers = {'Authorization': 'Bearer ' + refresh_token}
    response = client.get('/auth/token', headers=headers)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

    access_token = response.json()["access_token"]
    refresh_token = response.json()["refresh_token"]

    activities = get_activities()
    for activity in activities:
        headers = {'Authorization': 'Bearer ' + access_token}
        response = client.post('/activity',
                               data=json.dumps(activity), headers=headers)
        assert response.status_code == 200
        response_body = response.json()
        compare_activity(activity, response_body)

    for activity_type in ACTIVITY_TYPES:
        headers = {'Authorization': 'Bearer ' + access_token}
        query = '/activity?page_index=1&page_size=' + \
            f'300&activity_type={activity_type}'
        response = client.get(query, headers=headers)
        relevant_activities = list(filter(
            lambda activity: activity['activity_type'] ==
            activity_type, activities))

        for i, fetched_activity in enumerate(response.json()):
            compare_activity(relevant_activities[i], fetched_activity)

    for year in range(2000, 2020):
        headers = {'Authorization': 'Bearer ' + access_token}
        start_date = f"{year}-01-01T00:00:00.000000Z"
        end_date = "2020-01-01T00:01:00.000000Z"
        query = '/activity?page_index=1&page_size=300&start_date=' +\
            f'{start_date}&end_date={end_date}'
        response = client.get(query, headers=headers)
        assert len(response.json()) == 2020 - year - 1
