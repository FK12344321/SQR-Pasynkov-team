# tests/unit/test_user.py
import pytest
from app.models import User  # Ensure this import is correct
from app.internals.auth.user import check_user
import bcrypt
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session
from app.database.users import get_user_by_username
from app.internals.auth.user import create_user as user_create_user


@pytest.fixture
def mock_session():
    # Mock the Session maker and query
    session = MagicMock(spec=Session)
    with patch('app.database.crud.session_maker', return_value=session):
        yield session


def test_get_user_by_username_not_found(mock_session):
    # Setup
    mock_session.query.return_value.filter_by\
        .return_value.first.return_value = None

    # Execute & Assert
    with pytest.raises(ValueError):
        get_user_by_username("unknown_user")


def test_check_user():
    hashed_password = bcrypt.hashpw(
        "hashed_password".encode('utf-8'), bcrypt.gensalt())
    with patch('app.internals.auth.user.get_user_by_username') as\
         mock_get_user:
        # Ensure password is correctly formatted as a bcrypt hash
        mock_get_user.return_value = User(
            username="test", password=hashed_password.decode('utf-8'))
        assert check_user("test", "hashed_password") is True


def test_user_create_user(mock_session):
    with patch('app.internals.auth.user.create_db_user') as mock:
        usr = User(username="123123", password="123123")
        mock.return_value = usr
        ret_usr = user_create_user(usr)
        assert ret_usr is usr
