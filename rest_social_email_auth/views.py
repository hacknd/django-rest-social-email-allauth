# DRF Packages
from rest_framework import generics

# Local Packages
from rest_social_email_auth import app_settings


# Create your views here.
class UserCreateView(generics.CreateAPIView):
	"""
	Create an account from scratch

	post:
		create an account and facilitate in providing
		a venue in login in.
	"""
	def get_serializer_class(self):
		"""
		Get the serializer class used to register new users.

		Detault:
			CreateUserSerializer
		"""
		return app_settings.USER_SERIALIZER