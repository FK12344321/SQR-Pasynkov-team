# from typing import re
import re
import datetime
import time
import streamlit as st
import pandas as pd

activities = ["Running", "Cycling", "Swimming"]


def authenticate(username, password):
    if username == "1" and password == "2":
        return True
    else:
        return False


def sign_up(username, password):
    return True


def convert_seconds(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    return hours, minutes, remaining_seconds


def validate_time_format(input_text):
    pattern = re.compile(r'^([0-1]?[0-9]|2[0-3]):([0-5]?[0-9]):([0-5]?[0-9])$')
    if pattern.match(input_text):
        return True
    else:
        return False


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
            st.success('Sign up successful')


def get_timer_page():
    activity_select = st.selectbox("Choose an activity", activities)

    cols = st.columns(5)
    with cols[0]:
        play_button = st.button("Play")
    with cols[1]:
        pause_button = st.button("Pause/Reset")
    timer_output = st.empty()

    if play_button:
        st.session_state['elapsed_time'] = -1

    if pause_button:
        if 'elapsed_time' in st.session_state:
            st.session_state['paused_time'] = st.session_state['elapsed_time']
            hour, minutes, seconds = convert_seconds(st.session_state['paused_time'])
            timer_output.write(f"{hour:02}:{minutes:02}:{seconds:02}")
            del st.session_state['elapsed_time']

    while 'elapsed_time' in st.session_state:
        st.session_state['elapsed_time'] += 1
        hour, minutes, seconds = convert_seconds(st.session_state['elapsed_time'])
        timer_output.write(f"{hour:02}:{minutes:02}:{seconds:02}")
        time.sleep(1)


def get_form_page():
    with st.form("Activity Form"):
        activity_select = st.selectbox("Choose an activity", activities, index=0)
        time_select = st.text_input("Enter time (format: 00:00:00)")
        submit_button = st.form_submit_button("Save")
        if submit_button:
            if validate_time_format(time_select):
                st.success(f"Saved activity: {activity_select}, Time: {time_select}")
            else:
                st.error("Invalid time format")


def get_list():
    cols = st.columns(3)
    with cols[0]:
        extended_activities = ["All"]
        for activity in activities:
            extended_activities.append(activity)
        activity_select = st.selectbox("Choose an activity", extended_activities)
    with cols[1]:
        start_date = st.date_input("Start Date")
    with cols[2]:
        end_date = st.date_input("End Date")

    array = [{"activity_type": activities[0], "start_date": datetime.datetime.now(), "end_date": datetime.datetime.now(), "id": 1},
             {"activity_type": activities[1], "start_date": datetime.datetime.now(), "end_date": datetime.datetime.now(), "id": 2},
             {"activity_type": activities[2], "start_date": datetime.datetime.now(), "end_date": datetime.datetime.now(), "id": 3},
             {"activity_type": activities[1], "start_date": datetime.datetime.now(), "end_date": datetime.datetime.now(), "id": 4},
             {"activity_type": activities[0], "start_date": datetime.datetime.now(), "end_date": datetime.datetime.now(), "id": 5},
             {"activity_type": activities[2], "start_date": datetime.datetime.now(), "end_date": datetime.datetime.now(), "id": 6},
             {"activity_type": activities[0], "start_date": datetime.datetime.now(), "end_date": datetime.datetime.now(), "id": 7}]

    if end_date < start_date:
        st.error("Incorrect date filter")
    else:
        df = pd.DataFrame(array, columns=["activity_type", "start_date", "end_date"])

        if activity_select == "All":
            filtered_df = df
        else:
            filtered_df = df[df['activity_type'] == activity_select]

        filtered_df['start_date'] = pd.to_datetime(filtered_df['start_date']).dt.date
        filtered_df['end_date'] = pd.to_datetime(filtered_df['end_date']).dt.date

        if start_date and end_date:
            filtered_df = filtered_df[(filtered_df['start_date'] >= start_date) & (filtered_df['end_date'] <= end_date)]

        # Pagination
        record_size = 5
        page_number = st.number_input("Page Number", min_value=1, value=1, max_value=(len(filtered_df) // record_size + 1))
        start_index = (page_number - 1) * record_size
        end_index = page_number * record_size
        paginated_df = filtered_df.iloc[start_index:end_index]

        st.dataframe(paginated_df, hide_index=True, use_container_width=True)


def main():
    st.title("InnoTrackify")

    # if 'auth' not in st.session_state or st.session_state['auth'] is False:
    #     get_auth_page()
    # else:
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
