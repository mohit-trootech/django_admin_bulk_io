from django.urls import reverse
from django.conf import settings
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

URL = "admin:%s_%s_%s"


class TestBulkIOBase(TestCase):
    client = APIClient()
    BASE_DIR = str(settings.BASE_DIR)

    def setUp(self):
        self.user = self.create_superuser()
        self.client.force_login(self.user)

    def create_superuser(self):
        return get_user_model().objects.create_superuser(
            username="testuser", password="password"
        )

    def bulk_io_url(self, info: tuple, action: str):
        return reverse(URL % (*info, action))
