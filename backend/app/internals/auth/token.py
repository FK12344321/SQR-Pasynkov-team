import jwt

from app.models import User, UserCredentials, IncorrectToken
from app.database.users import get_user_by_username


def decode_token(token: str) -> User:
    """Decodes a Bearer token. Can raise IncorrectToken exception."""
    header_data = jwt.get_unverified_header(token)
    payload_data = jwt.decode(token, key='my_super_secret', algorithms=[header_data['alg', ]])
    return get_user_by_username(payload_data['username'])


def generate_token_from_user(user: User) -> UserCredentials:
    payload_data = {
        "username": user.username,
    }

    token = jwt.encode(
        payload=payload_data,
        key='my_super_secret',
        algorithm='HS256',
    )

    return UserCredentials(access_token=token, refresh_token=token)
