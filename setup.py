# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

setup(
	# Naming Area
	name="django-rest-social-email-allauth",

	# Version Area
	version='0.1.0',

	# Description Area
	description="This is an authentication module template with social (Oauth2) Authentication, knox-rest and email account verification with password reset framework.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	license="MIT",
	url="https://github.com/hacknd/django-rest-social-email-auth",
	author="HackND",
	author_email="benkaranja43@gmail.com",

	classifiers=[
		"Development Status :: 3 - Alpha",
		# Supported versions of Django
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        # Supported versions of Python
        "Programming Language :: Python",
  	],

	# Include the actual source code
	include_package_data=True,
	packages=find_packages(),
	# Dependencies
	install_requires=[
		"Django >= 3.0",
		"djangorestframework >= 3.0",
		"django-email-utils < 1.0",
		"django-rest-knox > 4.0",
		"social-auth-app-django<=3.1.0",
		"rest-social-auth>=2.1.0"
	],
)