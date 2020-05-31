# DRF Packages
from rest_framework import (
		generics,
		permissions, 
		response, 
		status
	)
from rest_framework.authtoken.serializers import AuthTokenSerializer

# Installed Packages
from knox.views import LoginView

# Django Packages
from django.contrib.auth import login

# Local Packages
from rest_social_email_auth import app_settings

# Local Variables
current_format = None


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


class UserLoginView(LoginView):
	"""
	Logging in a user that verification is required and an authorization header is created in the djangi api side
	"""
	permission_classes = (permissions.AllowAny,)

	def post(self, request, format=current_format):
		serializer = AuthTokenSerializer(
			data=request.data
		)
		serializer.is_valid(raise_exception=True)
		account = serializer.validated_data['user']
		login(request, account)
		json = super(UserLoginView, self).post(
			request,
			format=current_format
		)
		token = json.data["token"]
		return response.Response(
			json.data,
			status=status.HTTP_201_CREATED,
			headers={'Authorization': 'Token {0}'.format(token)}
		)