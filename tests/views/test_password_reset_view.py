try:
	from unittest import mock
except ImportError:
	import mock

from rest_framework import status
from rest_framework.reverse import reverse


url = reverse("rest-social-email-auth:password-reset")


@mock.patch(
	"rest_social_email_auth.serializers.PasswordResetSerializer.save"
)
def test_request_reset(mock_save, api_client, password_reset_token_factory):
	"""
	Sending a POST request with valid data to the view should reset the
	user's password.
	"""
	token = password_reset_token_factory()
	data = {"key": token.key, "password": "new_passw0rd"}

	response = api_client.post(url, data)

	assert response.status_code == status.HTTP_201_CREATED
	assert mock_save.call_count == 1