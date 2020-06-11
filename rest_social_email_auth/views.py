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
from knox import (
		settings,
		models,
		auth,
		views
)
from rest_social_auth.views import SocialKnoxUserAuthView

# Django Packages
from django.contrib.auth import (
		login,
		signals
)

# Local Packages
from rest_social_email_auth import (
		app_settings,
		utils,
		serializers,
		generics as custom_generics
)

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

class UserSocialLoginView(SocialKnoxUserAuthView):
	"""
	Logging in a user that social verification is required and an authorization header is created in the django api side
	"""
	serializer_class = serializers.SocialSerializer

	def get(self, request, provider, code=None, format=current_format):
		try:
			code = request.GET['code']
			data = utils.OAuthRedirectAuthorizationBackend(provider, code)
		except KeyError:
			return utils.OAuthRedirectAuthorizationBackend(provider, code)
		request.data.update(data)
		return self.post(request, format)

	def post(self, request, format=current_format, *args, **kwargs):
		json = super(AccountSocialLoginView, self).post(
			request,
			format=current_format
		)
		token = models.AuthToken.objects.get(
			token_key=json.data['token'][:settings.CONSTANTS.TOKEN_KEY_LENGTH]
		)
		data = {"token": json.data['token'], "expiry": token.expiry, "user": json.data}
		login(request, token.user, backend='client.backends.AuthBackend')
		return response.Response(
			data,
			status=status.HTTP_201_CREATED,
			headers={'Authorization': 'Token {0}'.format(json.data['token'])}
		)

class UserLogoutView(views.APIView):
	"""
	Logging out a single device
	closing a single session
	"""
	authentication_classes = (auth.TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	def post(self, request, *args, **kwargs):
		request._auth.delete()
		signals.user_logged_out.send(
			sender=request.user.__class__,
			request=request,
			user=request.user,
			*args,
			**kwargs
		)
		return response.Response(None, status.HTTP_204_NO_CONTENT, *args, **kwargs)

	def get(self, request, *args, **kwargs):
		return HttpResponseRedirect('/api/v1/', *args, **kwargs)


class UserLogoutAllView(views.APIView):
	"""
	Log the user out of all sessions
	I.E delete all auth tokens for the user
	"""
	authentication_classes = (auth.TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	def post(self, request, *args, **kwargs):
		request.user.auth_token_set.all().delete()
		signals.user_logged_out.send(
			sender=request.user.__class__,
			request=request,
			user=request.user
		)
		return response.Response(
			None,
			status=status.HTTP_204_NO_CONTENT,
			*args,
			**kwargs
		)

	def get(self, request, *args, **kwargs):
		return HttpResponseRedirect('/api/v1/', *args, **kwargs)


class EmailDetailView(generics.RetrieveUpdateDestroyAPIView):
	"""
	delete:
    	Delete a specific email address.

    get:
    	Retrieve the details of a particular email address.
    
    patch:
    	Partially update an email address.
    	
    	Only a verified email address may be marked as the user's primary
    	email.
   
    put:
    	Update an email address.
    	
    	Only a verified email address may be marked as the user's primary
   		email.
	"""
	permission_classes = (permissions.IsAuthenticated, )
	serializer_class = serializers.EmailSerializer

	def get_queryset(self):
		"""
		Get the email addresses belonging to the requesting user.

		Returns:
			A queryset containing only the email addresses owned by the 
			requesting user.
		"""
		return self.request.user.email_addresses.all()


class EmailListView(generics.ListCreateAPIView):
	"""
	get:
	List the email address associated with the requesting user's
	account.

	post:
	Add a new email address to the requesting user's account.
	"""

	permission_classes = (permissions.IsAuthenticated, )
	serializer_class = serializers.EmailSerializer

	def get_queryset(self):
		"""
		Get the email addresses belonging to the requesting user.


		Returns:
			A queryset containg only the email addresses owned by the requesting user.
		"""
		return self.request.user.email_addresses.all()

	def perform_create(self, serializer):
		"""
		Create a new email address to the requesting user.

		Args:
			serializer:
				An instance of the view's serializer class containing
				the data submitted in the request.


		Returns:
			The newly created email address.
		"""
		return serializer.save(user=self.request.user)


class EmailVerificationView(custom_generics.SerializerSaveView):
	"""
	Verify s user's email address.
	"""

	serializer_class = serializers.EmailVerificationSerializer


class ResendVerificationView(custom_generics.SerializerSaveView):
	"""
	Resend an email verification to a specific address.
	"""

	serializer_class = serializers.ResendVerificationSerializer