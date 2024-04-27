import re
import datetime
import time
import streamlit as st
import pandas as pd
import requests
import json
import os

from requests.auth import HTTPBasicAuth


API = os.environ.get('API_PATH', "http://10.90.137.146:8000")


def authenticate(username, password):
    basic_auth = HTTPBasicAuth(username, password)
    r = requests.get(f'{API}/auth/login', auth=basic_auth)
    if r.status_code != 200:
        return False
    st.session_state['access_token'] = r.json()['access_token']
    st.session_state['refresh_token'] = r.json()['refresh_token']
    return True


def sign_up(username, password):
    body = {
        "username": username,
        "password": password,
    }
    r = requests.post(f'{API}/auth/register', data=json.dumps(body))
    if r.status_code != 200:
        return False
    st.session_state['access_token'] = r.json()['access_token']
    st.session_state['refresh_token'] = r.json()['refresh_token']
    return True


def renew_token():
    headers = {'Authorization': 'Bearer ' + st.session_state['refresh_token']}
    r = requests.get(f'{API}/auth/token', headers=headers)
    if r.status_code != 200:
        return False
    st.session_state['access_token'] = r.json()['access_token']
    st.session_state['refresh_token'] = r.json()['refresh_token']
    return True


def convert_seconds(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    return hours, minutes, remaining_seconds


def validate_time_format(input_text):
    # pattern = re.compile(r'^([0-1]?[0-9]|2[0-3]):([0-5]?[0-9]):([0-5]?[0-9])$')
    pattern = re.compile(r'^(\d+|0?[0-9]|1[0-9]|2[0-3]):([0-5]?[0-9]):([0-5]?[0-9])$')
    if pattern.match(input_text):
        return True
    else:
        return False


def post_activity(hour, minutes, seconds, activity_select):
    time_delta = datetime.timedelta(hours=hour, minutes=minutes, seconds=seconds)
    end_date = datetime.datetime.now()
    start_date = end_date - time_delta
    body = {
        "activity_type": activity_select,
        "start_date": start_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "end_date": end_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    }
    headers = {'Authorization': 'Bearer ' + st.session_state['access_token']}
    r = requests.post(f'{API}/activity', data=json.dumps(body), headers=headers)
    if r.status_code == 401:
        renew_token()
        headers = {'Authorization': 'Bearer ' + st.session_state['access_token']}
        r = requests.get(f'{API}/activity', data=json.dumps(body), headers=headers)
    return r


def get_auth_page():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    cols = st.columns(7)
    with cols[0]:
        login_button = st.button("Login")
    with cols[1]:
        sign_up_button = st.button("Sign up")
    if login_button:
        if authenticate(username, password):
            st.session_state['auth'] = True
            st.session_state['page'] = 'timer'
            st.rerun()
        else:
            st.error("Invalid username or password")
    if sign_up_button:
        if sign_up(username, password):
            st.session_state['auth'] = True
            st.session_state['page'] = 'timer'
            st.rerun()
        else:
            st.error("Error with signing up")


def get_timer_page():
    activity_select = st.text_input("Choose an activity")

    play_button = st.button("Play")
    pause_button = st.button("Pause/Reset")
    save_button = st.button("Save")
    timer_output = st.empty()

    if play_button:
        st.session_state['elapsed_time'] = -1

    if pause_button:
        if 'elapsed_time' in st.session_state:
            st.session_state['paused_time'] = st.session_state['elapsed_time']
            hour, minutes, seconds = convert_seconds(st.session_state['paused_time'])
            timer_output.write(f"{hour:02}:{minutes:02}:{seconds:02}")
            del st.session_state['elapsed_time']

    if save_button:
        if 'paused_time' in st.session_state:
            hour, minutes, seconds = convert_seconds(st.session_state['paused_time'])
            r = post_activity(hour, minutes, seconds, activity_select)
            if r.status_code == 200:
                st.success(f"Saved activity: {activity_select}, Time: {hour}:{minutes}:{seconds}")
                del st.session_state['paused_time']
            else:
                st.error("Error saving activity")

    while 'elapsed_time' in st.session_state:
        st.session_state['elapsed_time'] += 1
        hour, minutes, seconds = convert_seconds(st.session_state['elapsed_time'])
        timer_output.write(f"{hour:02}:{minutes:02}:{seconds:02}")
        time.sleep(1)


def get_form_page():
    with st.form("Activity Form"):
        activity_select = st.text_input("Choose an activity")
        time_select = st.text_input("Enter time (format: 00:00:00)")
        submit_button = st.form_submit_button("Save")
        if submit_button:
            if validate_time_format(time_select):
                hours, minutes, seconds = map(int, time_select.split(':'))
                r = activity_select(hours, minutes, seconds, activity_select)
                if r.status_code == 200:
                    st.success(f"Saved activity: {activity_select}, Time: {time_select}")
                else:
                    st.error("Error saving activity")
            else:
                st.error("Invalid time format")


def get_list():
    cols = st.columns(3)
    with cols[0]:
        activity_select = st.text_input("Choose an activity")
    with cols[1]:
        start_date = st.date_input("Start Date")
    with cols[2]:
        end_date = st.date_input("End Date")

    page_size = 5
    page_number = st.number_input("Page Number", min_value=1, value=1)

    activity_filter =\
        (f"?page_index={page_number}"
         f"&page_size={page_size}"
         f"&start_date={start_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}"
         f"&end_date={end_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}")
    if activity_select:
        activity_filter += f"&activity_type={activity_select}"
    headers = {'Authorization': 'Bearer ' + st.session_state['access_token']}
    r = requests.get(f'{API}/activity' + activity_filter, headers=headers)
    if r.status_code == 401:
        renew_token()
        headers = {'Authorization': 'Bearer ' + st.session_state['access_token']}
        r = requests.get(f'{API}/activity' + activity_filter, headers=headers)
    if r.status_code != 200:
        return
    array = r.json()
    df = pd.DataFrame(array, columns=["activity_type", "start_date", "end_date"])
    st.dataframe(df, hide_index=True, use_container_width=True)


def main():
    st.title("InnoTrackify")

    if 'auth' not in st.session_state or st.session_state['auth'] is False:
        get_auth_page()
    else:
        page = st.sidebar.radio("Pages", ['Use timer', 'Add activity', 'Show activities'], key='sidebar')
        st.session_state['page'] = page
        if st.session_state['page'] == 'Use timer':
            get_timer_page()
        elif st.session_state['page'] == 'Add activity':
            get_form_page()
        elif st.session_state['page'] == 'Show activities':
            get_list()


if __name__ == "__main__":
    main()
