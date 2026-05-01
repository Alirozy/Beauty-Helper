from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import CustomUser


class AuthFlowTests(APITestCase):
    def setUp(self):
        self.password = "StrongPass123!"
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password=self.password,
        )
        self.login_url = reverse("token_obtain_pair")
        self.register_url = reverse("auth_register")
        self.logout_url = reverse("auth_logout")
        self.delete_account_url = reverse("delete_account")
        self.refresh_url = reverse("token_refresh")

    def authenticate(self):
        response = self.client.post(
            self.login_url,
            {"username": self.user.username, "password": self.password},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access = response.data["access"]
        refresh = response.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        return access, refresh

    def test_login_returns_tokens_and_user_payload(self):
        response = self.client.post(
            self.login_url,
            {"username": self.user.username, "password": self.password},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("user", response.data)
        self.assertEqual(response.data["user"]["username"], self.user.username)
        self.assertEqual(response.data["user"]["email"], self.user.email)

    def test_register_creates_user_successfully(self):
        payload = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "StrongPass456!",
            "password_confirm": "StrongPass456!",
            "phone_number": "5551234567",
        }
        response = self.client.post(self.register_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(username="newuser").exists())
        self.assertIn("user", response.data)
        self.assertEqual(response.data["user"]["username"], "newuser")

    def test_register_fails_when_passwords_do_not_match(self):
        payload = {
            "username": "newuser2",
            "email": "newuser2@example.com",
            "password": "StrongPass456!",
            "password_confirm": "DifferentPass456!",
            "phone_number": "5551234568",
        }
        response = self.client.post(self.register_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
        self.assertFalse(CustomUser.objects.filter(username="newuser2").exists())

    def test_register_fails_with_duplicate_email(self):
        payload = {
            "username": "anotheruser",
            "email": self.user.email,
            "password": "StrongPass456!",
            "password_confirm": "StrongPass456!",
            "phone_number": "5551234569",
        }
        response = self.client.post(self.register_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertFalse(CustomUser.objects.filter(username="anotheruser").exists())

    def test_logout_blacklists_refresh_token(self):
        _, refresh = self.authenticate()

        logout_response = self.client.post(
            self.logout_url,
            {"refresh": refresh},
            format="json",
        )
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)

        refresh_response = self.client.post(
            self.refresh_url,
            {"refresh": refresh},
            format="json",
        )
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_requires_refresh_token(self):
        self.authenticate()
        response = self.client.post(self.logout_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_account_removes_current_user_with_valid_password(self):
        self.authenticate()

        response = self.client.delete(
            self.delete_account_url,
            {"password": self.password},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(CustomUser.objects.filter(id=self.user.id).exists())

    def test_delete_account_rejects_wrong_password(self):
        self.authenticate()

        response = self.client.delete(
            self.delete_account_url,
            {"password": "WrongPassword!"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(CustomUser.objects.filter(id=self.user.id).exists())
