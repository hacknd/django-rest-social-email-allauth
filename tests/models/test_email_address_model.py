try:
	from unittest import mock
except ImportError:
	import mock


from django.conf import settings

from rest_social_email_auth import models


def test_create(user_factory):
	"""
	testing creating an email address
	"""
	email = models.EmailAddress.objects.create(
		email="test@example.com",
		is_primary=True,
		user=user_factory()
	)

	assert not email.is_verified


def test_create_second_primary(email_factory):
	"""
	if the user has a primary email address and a second one is created
	with ``is_primary == True``, the initial email should be reomved as the primary email.
	"""

	old_primary = email_factory(is_primary=True)
	email_factory(is_primary=True, user=old_primary.user)

	old_primary.refresh_from_db()

	assert not old_primary.is_primary