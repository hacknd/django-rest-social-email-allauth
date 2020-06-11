try:
	from unittest import mock
except ImportError:
	import mock

from rest_social_email_auth import serializers


def test_create(user_factory):
	"""
	Test creating a new email address from the serializer.

	Creating a new email address should also send a confirmation email
	for the provided address. If the user does not have a primary email, 
	the created one should be marked as the primary.
	"""
	user = user_factory()
	data = {"email": "test@example.com"}

	serializer = serializers.EmailSerializer(data=data)
	assert serializer.is_valid()

	email = serializer.save(user=user)

	assert email.email == data["email"]
	assert email.is_primary


@mock.patch(
	"rest_social_email_auth.models.EmailAddress.send_duplicate_notification",
	autospec=True,
	)
def test_create_duplicate(mock_duplicate_notification, email_factory, user_factory):
	"""
	Attempting to add an email address that already exists should send a notification
	to the existing email.
	"""
	email = email_factory()
	user = user_factory()

	data = {"email": email.email}

	serializer = serializers.EmailSerializer(data=data)
	assert serializer.is_valid(), serializer.errors

	serializer.save(user=user)

	assert mock_duplicate_notification.call_count == 1
	assert mock_duplicate_notification.call_args[0] == (email,)



def test_create_non_primary(
	email_factory, user_factory
	):
	"""
	If the user already has a primary email address, the created email
	should not be marked as the user's primary.
	"""
	user = user_factory()
	email_factory(is_primary=True, user=user)

	data = {"email": "test@example.com"}

	serializer = serializers.EmailSerializer(data=data)
	assert serializer.is_valid()


	email = serializer.save(user=user)

	assert email.email == data["email"]
	assert not email.is_primary


def test_update_is_primary_false(email_factory):
	"""
	Updating 'is_primary' to false should not call set_primary.
	"""
	email = email_factory(is_primary=True, is_verified=True)
	data = {"is_primary": False}


	serializer = serializers.EmailSerializer(email, data=data, partial=True)
	assert serializer.is_valid()
	with mock.patch.object(
		email, "set_primary", autospec=True
	) as mock_set_primary:
		email = serializer.save()


	assert mock_set_primary.call_count == 0


def test_validate_changed_email(email_factory):
	"""
	If a bound serializer attempts to change the email address of its
	instance it should not be valid
	"""
	email = email_factory(email="old@example.com")
	data = {"email": "new@example.com"}

	serializer = serializers.EmailSerializer(email, data=data)

	assert not serializer.is_valid()
	assert set(serializer.errors.keys()) == {"email"}

def test_validate_create_primary():
	"""
	Attempting to create a primary email address should not be valid. It
	should only be valid to mark a verified email address as the primary
	unless this is the user's first email.
	"""
	data = {"email": "test@example.com", "is_primary": True}
	serializer = serializers.EmailSerializer(data=data)

	assert not serializer.is_valid()
	assert set(serializer.errors.keys()) == {"is_primary"}

def test_validate_email_lowercase_domain():
	"""
	The registration serializer should not change an email address with a lowercase domain.
	"""
	email = "Test@example.com"
	serializer = serializers.EmailSerializer()

	assert serializer.validate_email(email) == email

def test_validate_email_mixed_case_domain():
	"""
	If the domain portion of the email is mixed case. it should be
	converted to lowercase.
	"""
	email = "Test@ExaMple.com"
	expected = "Test@example.com"
	serializer = serializers.EmailSerializer()

	assert serializer.validate_email(email) == expected

def test_validate_make_unverified_primary(email_factory):
	"""
	attempting to mark an existing but unverified email address 
	as the primary should be valid.
	"""
	email = email_factory(is_primary=False, is_verified=False)
	data = {"is_primary": True}

	serializer = serializers.EmailSerializer(email, data=data, partial=True)

	assert not serializer.is_valid()
	assert set(serializer.errors.keys()) == {"is_primary"}