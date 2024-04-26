from app.models import User, UserCredentials


def decode_token(token: str) -> User:
    """Decodes a Bearer token. Can raise IncorrectToken exception."""
    return User(username=token, password='booba')


def create_token(user: User) -> UserCredentials:
    return UserCredentials(access_token=user.username, refresh_token=user.password)


def generate_token_from_user(user: User) -> UserCredentials:
    return UserCredentials(access_token=user.username, refresh_token=user.password)
