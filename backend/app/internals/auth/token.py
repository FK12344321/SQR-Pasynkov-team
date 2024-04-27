import jwt

from app.models import User, UserCredentials, IncorrectToken
from app.database.users import get_user_by_username
from app.config import get_settings


def decode_token(token: str) -> User:
    """Decodes a Bearer token. Can raise IncorrectToken exception."""
    settings = get_settings()
    try:
        header_data = jwt.get_unverified_header(token)
        payload_data = jwt.decode(token,
                                  key=settings.auth_token_secret,
                                  algorithms=[header_data['alg'], ])
        return get_user_by_username(payload_data['username'])
    except Exception as error:
        print("Can't decode token, error:", error)
        raise IncorrectToken('Bearer')


def generate_token_from_user(user: User) -> UserCredentials:
    settings = get_settings()
    payload_data = {
        'username': user.username,
    }

    token = jwt.encode(
        payload=payload_data,
        key=settings.auth_token_secret,
        algorithm=settings.auth_token_alg,
    )

    return UserCredentials(access_token=token, refresh_token=token)
