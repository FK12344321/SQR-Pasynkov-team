from main import authenticate, sign_up, renew_token, validate_time_format, post_activity
import sys
import os
import pytest
import json
from unittest.mock import patch

# Adjust Python path to ensure local modules can be imported
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../')))


@pytest.fixture(autouse=True)
def setup_session_state():
    with patch('streamlit.session_state', new_callable=dict) as mock_session:
        mock_session.update(
            {'access_token': 'fake_access_token', 'refresh_token': 'fake_refresh_token'})
        yield


@pytest.fixture
def mock_requests(mocker):
    mocker.patch('requests.get')
    mock_post = mocker.patch('requests.post')
    return mock_post


@pytest.fixture
def mock_requests_get(mocker):
    mock_get = mocker.patch('requests.get')
    return mock_get

# Authentication Tests


def test_authenticate_success(mock_requests_get):
    mock_requests_get.return_value.status_code = 200
    assert authenticate('valid_user', 'valid_pass') is True


def test_authenticate_failure(mock_requests_get):
    mock_requests_get.return_value.status_code = 401
    assert authenticate('invalid_user', 'invalid_pass') is False

# Sign Up Tests


def test_sign_up_success(mock_requests):
    mock_requests.return_value.status_code = 200
    mock_requests.return_value.json.return_value = {
        'access_token': 'new_token', 'refresh_token': 'new_refresh_token'}
    assert sign_up('new_user', 'new_pass') is True


def test_sign_up_failure(mock_requests):
    mock_requests.return_value.status_code = 400
    assert sign_up('existing_user', 'pass') is False

# Token Renewal Tests


def test_renew_token_success(mock_requests_get):
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = {
        'access_token': 'renewed_token', 'refresh_token': 'renewed_refresh_token'}
    assert renew_token() is True


def test_renew_token_failure(mock_requests):
    mock_requests.return_value.status_code = 401
    assert renew_token() is False

# Time Format Validation Tests


@pytest.mark.parametrize("time_input, expected", [
    ("23:59:59", True),
    ("00:00:00", True),
    ("24:00:00", True),
    ("12:60:00", False),
    ("12:00:60", False)
])
def test_validate_time_format(time_input, expected):
    assert validate_time_format(time_input) == expected

# Activity Posting Tests


def test_post_activity_success(mock_requests):
    mock_requests.return_value.status_code = 200
    assert post_activity(2, 30, 45, 'Running').status_code is 200


def test_post_activity_invalid_time(mock_requests):
    mock_requests.return_value.status_code = 402
    assert post_activity(25, 61, 61, 'Swimming').status_code is not 200
