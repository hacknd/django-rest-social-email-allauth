# DRF Packages
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Installed Packages
from rest_social_auth.serializers import UserKnoxSerializer

# Django Packages
from django.contrib.auth import get_user_model, password_validation

# Local Packages
from rest_social_email_auth import signals


class CreateUserSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(
		required=True,
		validators=[UniqueValidator(queryset=get_user_model().objects.all())]
	)
	username = serializers.CharField(
		required=True,
		max_length=13,
		validators=[UniqueValidator(queryset=get_user_model().objects.all())]
	)
	password = serializers.CharField(
		min_length=8,
		write_only=True
	)

	def create(self, validated_data):
		account = get_user_model().objects.create_user(
			username=validated_data['username'],
			email=validated_data['email'],
			password=validated_data['password']
		)

		signals.user_registered.send(
				sender=self.__class__,
				user=account
			)
		return account

	def validate_email(self, email):
		"""
		Validate the provided email address.

		Args:
			email:
				The email address to validate.

		Returns:
			The provided email address, transformed to match the RFC
			spec. Namely, the domain portion of the email must be 
			lowercase.
			# Sowy for the formality onnichan or ani-wee its for the best.
		"""
		user, domain = email.rsplit("@", 1)
		email = "@".join([user, domain.lower()])

		if self.instance and email and self.instance.email != email:
			raise serializers.ValidationError(
				__(
					"Existing emails may not be edited. Create a new one "
					"instead."
				)

			)

		return email

	def validate_password(self, password):
		"""
		Validate the provided password.


		Args:
			password (str):
				The password provided by the user.

		Returns:
			str:
				The validated password.

		Raises:
			ValidationError:
				If the provided password does not pass the
				considered password validators.
		"""

		password_validation.validate_password(password)

		return password

	class Meta(object):
		model = get_user_model()
		fields = ('id', 'username', 'email', 'password')


class AccountSerializer(serializers.ModelSerializer):
	class Meta:
		model = get_user_model()
		fields = ('id', 'last_login', 'is_superuser', 'username', 'email', 'phone_number', 'is_active')


# Social Logins serializer
class SocialSerializer(UserKnoxSerializer):
	def get_token(self, obj):
		instance, token = models.AuthToken.objects.create(obj)
		instance.save()
		return token