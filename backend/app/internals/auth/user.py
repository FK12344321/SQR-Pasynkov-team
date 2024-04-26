import bcrypt

from app.models import User
from app.database.users import get_user_by_username, create_user as create_db_user


def check_user(username: str, password: str) -> bool:
    """
    Checks if the given username and password are correct.
    User with the given username must exist and password should be correct.
    :return: bool value indicating if the given user is correct.
    """
    print(f'check_user: username: {username}, password: {password}')
    try:
        user = get_user_by_username(username)
    except ValueError:
        return False

    hashed_password = user.password.encode('utf-8')
    hashed_x2 = bcrypt.hashpw(password.encode('utf-8'), hashed_password)
    is_correct_password = hashed_x2 == hashed_password
    print(f'check_user: is_correct_password: {is_correct_password}\n\tx1: {hashed_password}\n\tx2: {hashed_x2}')
    return is_correct_password


def is_exist(username: str) -> bool:
    try:
        user = get_user_by_username(username)
        return user is not None
    except ValueError:
        return False


def create_user(user: User) -> User:
    user.password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    return create_db_user(user)


def get_user(username: str) -> User:
    return get_user_by_username(username)
