try:
	from unittest import mock
except ImportError:
	import mock

from rest_social_email_auth import models, serializers


def test_save(password_reset_token_factory):
	"""
	Saving the serializer with a valid token and password should reset
	the associated user's password.
	"""
	token = password_reset_token_factory()
	user = token.email.user

	data = {"key": token.key, "password": "new_passw0rd"}

	serializer = serializers.PasswordResetSerializer(data=data)
	assert serializer.is_valid()

	serializer.save()
	user.refresh_from_db()

	assert user.check_password(data["password"])
	assert models.PasswordResetToken.objects.count() == 0


def test_validate_key_expired(password_reset_token_factory):
	"""
	If the key provided corresponds to a token that has expired, the
	serializer should not validate
	"""
	token = password_reset_token_factory()
	data = {"key": token.key, "password": "new_passw0rd"}

	serializer = serializers.PasswordResetSerializer(data=data)


	with mock.patch(
		"rest_social_email_auth.models.PasswordResetToken.valid_tokens.filter",
		return_value=models.PasswordResetToken.objects.none(),
	) as mock_filter:
		assert not serializer.is_valid()

	assert set(serializer.errors.keys()) == {"key"}
	assert mock_filter.call_count == 1