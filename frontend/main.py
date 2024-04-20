# from typing import re
import re
import datetime
import time
import streamlit as st

activities = ["Running", "Cycling", "Swimming"]


def authenticate(username, password):
    if username == "1" and password == "2":
        return True
    else:
        return False


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


def main():
    st.title("InnoTrackify")

    if 'auth' not in st.session_state or st.session_state['auth'] is False:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login")
        if login_button:
            if authenticate(username, password):
                st.session_state['auth'] = True
                st.session_state['page'] = 'timer'
            else:
                st.error("Invalid username or password")

    else:
        page = st.sidebar.radio("Pages", ['Use timer', 'Add activity', 'Show activities'], key='sidebar')
        st.session_state['page'] = page

        if st.session_state['page'] == 'Use timer':
            activity_select = st.selectbox("Choose an activity", activities)

            timer_output = st.empty()
            play_button = st.button("Play")
            pause_button = st.button("Pause/Reset")

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
        elif st.session_state['page'] == 'Add activity':
            with st.form("Activity Form"):
                activity_select = st.selectbox("Choose an activity", activities, index=0)
                time_select = st.text_input("Enter time (format: 00:00:00)")
                submit_button = st.form_submit_button("Save")
                if submit_button:
                    if validate_time_format(time_select):
                        st.success(f"Saved activity: {activity_select}, Time: {time_select}")
                    else:
                        st.error("Invalid time format")
        elif st.session_state['page'] == 'Show activities':
            st.header('huy')


if __name__ == "__main__":
    main()
