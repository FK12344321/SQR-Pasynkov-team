from locust import HttpUser, tag, task
import requests
import json
from random import randint
from datetime import datetime
from requests.auth import HTTPBasicAuth

API = 'http://10.90.137.146:8000'

SINCE = 0
TILL = int(datetime.now().timestamp())
ACTIVITY_TYPES = ['sport', 'work', 'study']
ACTIVITIES_TOTAL = 100


class HelloWorldUser(HttpUser):
    def get_dates(self) -> tuple[datetime, datetime]:
        from_datetime = datetime.fromtimestamp(randint(SINCE, TILL))
        to_datetime = datetime.fromtimestamp(
            randint(from_datetime.timestamp(), TILL))
        return (from_datetime, to_datetime)

    def on_start(self):
        basic_auth = HTTPBasicAuth("user", "password")
        r = requests.get(f'{API}/auth/login', auth=basic_auth)
        self.token = r.json()['access_token']
        print(self.token)

    @tag("post_activities")
    @task
    def post_activities(self):
        start_date, end_date = self.get_dates()
        activity_type = ACTIVITY_TYPES[randint(0, len(ACTIVITY_TYPES) - 1)]
        body = {
            "activity_type": activity_type,
            "start_date": start_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "end_date": end_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }
        print(body)
        self.client.request(method="POST",
                            url="/activity",
                            data=json.dumps(body),
                            headers={"Authorization": "Bearer " + self.token})

    @tag("get_activities")
    @task
    def get_activities(self):
        page_size = 20
        page_index = randint(1, ACTIVITIES_TOTAL // page_size - 1)
        query_params = f"page_index={page_index}&page_size={page_size}"
        if randint(0, 10) % 2 == 0:
            start_date, end_date = self.get_dates()
            start_date = start_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            end_date = end_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            query_params += f"&start_date={start_date}&end_date={end_date}"
        if randint(0, 10) % 2 == 0:
            activity_type = ACTIVITY_TYPES[randint(0, len(ACTIVITY_TYPES) - 1)]
            query_params += f"&activity_type={activity_type}"
        print(f"/activity?{query_params}")
        self.client.request(method="GET",
                            url=f"/activity?{query_params}",
                            headers={"Authorization": "Bearer " + self.token})
