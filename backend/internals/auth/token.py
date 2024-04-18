from backend.models import User


def decode_token(token: str) -> User:
    return User(username=token, password='booba')


def create_token(user: User) -> str:
    return 'aboba'
