# Django Packages
from django.test import TestCase
from django.contrib.auth import get_user_model

# Local Packages
from rest_social_email_auth.models import User

# Universal Packages and other variables
Account = User


class AccountManagerTests(TestCase):
    def test_create_account_test(self):
        account = Account.objects.create_user(
            username="Ben", email="normal@user.com", password="foo"
        )
        account.save()
        self.assertEqual(account.email, "normal@user.com")
        self.assertTrue(account.is_active)
        self.assertFalse(account.is_staff)
        self.assertFalse(account.is_superuser)

        with self.assertRaises(TypeError):
            Account.objects.create_user()
        with self.assertRaises(TypeError):
            Account.objects.create_user(email="")
        with self.assertRaises(ValueError):
            Account.objects.create_user(username="", email="", password="foo")

    def test_create_superuser(self):
        admin_account = Account.objects.create_superuser(
            username="super", password="foo", email=""
        )
        self.assertEqual(admin_account.username, "super")
        self.assertTrue(admin_account.is_active)
        self.assertTrue(admin_account.is_staff)
        self.assertTrue(admin_account.is_superuser)

        self.assertEqual(len(admin_account.email), 0)
        with self.assertRaises(ValueError):
            Account.objects.create_superuser(
                username="super", email="", password="foo", is_superuser=False
            )
