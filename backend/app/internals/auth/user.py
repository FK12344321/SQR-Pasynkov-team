import secrets

from app.models import User


def check_user(username: str, password: str) -> bool:
    """
    Checks if the given username and password are correct.
    User with the given username must exist and password should be correct.
    :return: bool value indicating if the given user is correct.
    """
    current_username_bytes = username.encode("utf8")
    correct_username_bytes = b"aboba"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = password.encode("utf8")
    correct_password_bytes = b"booba"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    return is_correct_username and is_correct_password


def is_exist(username: str) -> bool:
    return username == 'aboba'


def create_user(user: User) -> User:
    return user
