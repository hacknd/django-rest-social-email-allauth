# Django Packages
from django.test import TestCase
from django.contrib.auth import get_user_model

# Local Packages
from client_auth.models import Account

# Universal Packages

class AccountManagerTests(TestCase):
    def test_create_account_test(self):
        account = Account.objects.create_user(
            username="Ben",
            email="normal@user.com",
            password="foo"
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
            username="super",
            password="foo",
            email=""
        )
        admin_member = Member.objects.get(user=admin_account)
        self.assertEqual(admin_account.username, "super")
        self.assertTrue(admin_account.is_active)
        self.assertTrue(admin_account.is_staff)
        self.assertTrue(admin_account.is_superuser)
        self.assertTrue(admin_member.is_admin)
        self.assertEqual(admin_account.username, admin_member.username)
        self.assertEqual(admin_account.phone_number, admin_member.phone_number)

        self.assertEqual(len(admin_account.email), 0)
        with self.assertRaises(ValueError):
            Account.objects.create_superuser(
                username="super",
                email="",
                password="foo",
                is_superuser=False
            )