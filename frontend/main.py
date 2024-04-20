import datetime
import time
import streamlit as st


def authenticate(username, password):
    if username == "user" and password == "password":
        return True
    else:
        return False


def convert_seconds(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    return hours, minutes, remaining_seconds


def main():
    st.title("InnoTrackify")

    if 'auth' not in st.session_state or st.session_state['auth'] is False:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login")
        if login_button:
            if authenticate(username, password):
                st.session_state['auth'] = True
            else:
                st.error("Invalid username or password")

    else:
        timer_output = st.empty()
        play_button = st.button("Play")
        pause_button = st.button("Pause/Stop")

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


if __name__ == "__main__":
    main()
