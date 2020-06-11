# Django Packages
from django.urls import path
from django.conf.urls import url

# Local Packages
from rest_social_email_auth import views

app_name = "rest-social-email-auth"


urlpatterns = [
	path(
		'register/',
		views.UserCreateView.as_view(),
		name='user-create'
	),
	path(
		'login/',
		views.UserLoginView.as_view(),
		name='user-login'
	),
	path(
		'logout/',
		views.UserLogoutView.as_view(),
		name='user-logout'
	),
	path(
		'logout-all/',
		views.UserLogoutAllView.as_view(),
		name='user-logout-all'
	),
	path(
		'login/social/<provider>/',
		views.UserSocialLoginView.as_view(),
		name='user-social-login'
	),
	path(
		'emails/',
		views.EmailListView.as_view(),
		name="email-list"
	),
	url(
		r"^emails/(?P<pk>[0-9]+)/$",
		views.EmailDetailView.as_view(),
		name="email-detail",
	),
]