# Django Packages
from django.utils.translation import gettext_lazy as __
from django.contrib.sites.models import Site
from django.shortcuts import redirect

# Installed Packages
from rest_framework import exceptions, status, reverse
from social_core.backends.utils import get_backend
from decouple import config
import urllib

# Local Packages
from django.conf import settings
from rest_social_email_auth.generics import CustomException


def OAuthRedirectAuthorizationBackend(backend, code):
    """
	Authorization Information for the backends to the redirect feature
	:param backend:
	:param code:
	:return:
		data in json including:
			- code
			- redirect_uri
			- provider ( backend )
	"""
    if code is None:
        try:
            backend_class = get_backend(settings.AUTHENTICATION_BACKENDS, backend)
            authorization_url = backend_class.AUTHORIZATION_URL
            url_parameters = {
                "redirect_uri": ("http://{}{}").format(
                    Site.objects.get_current().domain,
                    reverse.reverse(
                        "rest-social-email-auth:user-social-login", args=(backend,)
                    ),
                ),
                "response_type": backend_class.RESPONSE_TYPE,
                "scope": [
                    scope for scope in backend_class.DEFAULT_SCOPE if scope != "openid"
                ][0],
                "client_id": config(
                    "SOCIAL_AUTH_" + backend.upper().replace("-", "_") + "_KEY"
                ),
            }

            final_url = authorization_url + "?" + urllib.parse.urlencode(url_parameters)

        except:
            raise CustomException(
                code=status.HTTP_501_NOT_IMPLEMENTED, detail=__("Missing Backend")
            )

        return redirect(final_url)

    data = {
        "code": code,
        "redirect_uri": ("http://{}{}").format(
            Site.objects.get_current().domain,
            reverse.reverse(
                "rest-social-email-auth:user-social-login", args=(backend,)
            ),
        ),
        "provider": backend,
    }

    return data
