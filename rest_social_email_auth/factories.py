"""
Factories for generating test data


These factories generate models with dummy data for testing purposes.
"""

from django.contrib.auth import get_user_model


import factory

from rest_social_email_auth import models


class UserFactory(factory.django.DjangoModelFactory):
	"""
	Factory for generating Django user instances.
	"""

	password = "password"
	username = factory.sequence(lambda n: "user{n}".format(n=n))
	email = factory.sequence(lambda n: "test{n}@example.com".format(n=n))
	phone_number = factory.sequence(lambda n: "+25471594357{n}".format(n=n))

	class Meta(object):
		model = get_user_model()

	@classmethod
	def _create(cls, model_class, *args, **kwargs):
		"""
		Create a new user instance

		Args:
			model_class:
				The type of model to create an instance of.
			args:
				Positional arguements to create the instance with.
			kwargs:
				Keyword arguements to create the instance with.

		Returns:
			A new user instance of the type specified by
			``model_class``.
		"""

		manager = cls._get_manager(model_class)
		user = manager.create_user(*args, **kwargs)
		user.save()
		return user