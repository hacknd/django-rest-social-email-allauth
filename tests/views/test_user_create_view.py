try:
    from unittest import mock
except ImportError:
    import mock

import pytest

from rest_framework import status

from rest_social_email_auth import app_settings, views, models


registration_view = views.UserCreateView.as_view()


def test_get_serializer_class():
    """
	The view should use the serializer defined in the app's settings.
	"""
    view = views.UserCreateView()
    expected = app_settings.USER_SERIALIZER

    assert view.get_serializer_class() == expected


@pytest.mark.django_db
def test_register(api_rf):
    """
	Sending a POST request with valid data to the view should register a
	new user.
	"""
    data = {
        "username": "user",
        "email": "test@example.com",
        "password": "password1231232",
    }

    serializer = app_settings.USER_SERIALIZER(data=data)
    assert serializer.is_valid()

    request = api_rf.post("/", data)
    response = registration_view(request)

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_account_with_short_password(api_rf):
    """
		Ensure user is not created for password length less that 8
		:return:
		"""
    data = {"username": "foobar", "password": "foo", "email": "foobarbaz@example.com"}

    request = api_rf.post("/", data)
    response = registration_view(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert models.User.objects.count() == 0


@pytest.mark.django_db
def test_create_account_with_no_password(api_rf):
    data = {"username": "foobar", "email": "foobar@example.com", "password": ""}
    request = api_rf.post("/", data)
    response = registration_view(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert models.User.objects.count() == 0


@pytest.mark.django_db
def test_create_account_with_long_username(api_rf):
    foo = "foo" * 17
    data = {"username": foo, "email": "foobarbaz@example.com", "password": "foobarbaz"}

    request = api_rf.post("/", data)
    response = registration_view(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert models.User.objects.count() == 0


@pytest.mark.django_db
def test_create_account_with_no_username(api_rf):
    data = {"username": "", "email": "foobarbaz@example.com", "password": " foobar"}

    request = api_rf.post("/", data)
    response = registration_view(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert models.User.objects.count() == 0


@pytest.mark.django_db
def test_create_account_with_pre_existing_email(api_rf, user_factory):
    user = user_factory()
    data = {"username": "testuser2", "email": user.email, "password": "testuser"}

    request = api_rf.post("/", data)
    response = registration_view(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert models.User.objects.count() == 1


@pytest.mark.django_db
def test_create_account_with_invalid_email(api_rf):
    data = {"username": "foobarbaz", "email": "testing", "password": "foobarbaz"}

    request = api_rf.post("/", data)
    response = registration_view(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert models.User.objects.count() == 0


@pytest.mark.django_db
def test_user_with_no_email(api_rf):
    data = {"username": "foobar", "email": "", "password": "foobarbaz"}

    request = api_rf.post("/", data)
    response = registration_view(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert models.User.objects.count() == 0
