import jwt
import pytest
from unittest.mock import patch
from app.models import User
from app.internals.auth.token import generate_token_from_user
from app.internals.auth.token import decode_token


def test_generate_token_from_user():
    # Make sure to include the password when creating the User instance
    test_user = User(username="test_user", password="secure_password")
    # Proceed with generating a token and asserting as needed
    token_result = generate_token_from_user(test_user)
    assert token_result.access_token is not None


@pytest.mark.unit
def test_decode_token():
    # Prepare a sample payload that reflects a valid decoded JWT structure
    sample_payload = {'username': 'test_user'}
    valid_token = jwt.encode(sample_payload, 'secret', algorithm='HS256')

    with patch('jwt.decode') as mock_decode, \
            patch('jwt.get_unverified_header') as mock_get_header, \
            patch('app.internals.auth.token.get_user_by_username') as\
            mock_get_user:
        # Mock the jwt.decode to return the sample payload
        mock_decode.return_value = sample_payload
        # Mock the jwt.get_unverified_header to not raise an exception
        mock_get_header.return_value = {'alg': 'HS256'}
        # Mock the user retrieval to return a user object
        mock_get_user.return_value = User(
            username="test_user", password="secure_password")

        # Invoke the function to be tested
        user = decode_token(valid_token)

        # Verify the expected results
        assert user.username == 'test_user'
        mock_decode.assert_called_once_with(
            valid_token, key='this_is_secret_token', algorithms=['HS256'])
        mock_get_header.assert_called_once_with(valid_token)


def test_exception():
    with pytest.raises(Exception):
        decode_token("asdagccc")
