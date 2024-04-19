import secrets


def check_user(username: str, password: str) -> bool:
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
