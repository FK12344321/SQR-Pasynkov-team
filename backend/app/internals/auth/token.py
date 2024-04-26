import base64

from app.models import User, UserCredentials, IncorrectToken
from app.database.users import get_user_by_username


def decode_token(token: str) -> User:
    """Decodes a Bearer token. Can raise IncorrectToken exception."""
    try:
        token_data = base64.b64decode(token.encode('utf-8')).decode('utf-8')
        username, reversed_username = token_data.split(sep=' ', maxsplit=1)
        if username != reversed_username[::-1]:
            raise IncorrectToken('Bearer')
        return get_user_by_username(username)
    except Exception:
        raise IncorrectToken('Bearer')


def generate_token_from_user(user: User) -> UserCredentials:
    token = f"{user.username} {user.username[::-1]}"
    token_bytes = token.encode('utf-8')
    base64_token = base64.b64encode(token_bytes).decode('utf-8')
    return UserCredentials(access_token=base64_token, refresh_token=base64_token)
