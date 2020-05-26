try:
    from unittest import mock
except ImportError:
    import mock

import pytest

from rest_framework import status

from rest_social_email_auth import app_settings, views


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