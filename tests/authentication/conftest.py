"""
Fixtures for testing authentication backends.
"""

import pytest

from rest_social_email_auth import authentication


@pytest.fixture(scope="session")
def auth_backend():
    """
    Return an instance of the base authentication backend.
    """
    return authentication.AuthBackend()


@pytest.fixture(scope="session")
def verified_email_auth_backend():
    """
    Return an instance of the authentication backend that only accepts
    verified emails.
    """
    return authentication.VerifiedEmailBackend()