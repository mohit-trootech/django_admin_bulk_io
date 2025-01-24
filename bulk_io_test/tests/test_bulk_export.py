from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from bulk_io_test.tests.factory import PostFactory, CommentFactory, UserFactory
from django.contrib.auth.models import User
from utils.utils import get_model
from random import randint
from django.db.models import Model
from json import loads
from django_admin_bulk_io.utils.constants import BulkIOMessages, BulkIOException
from django.conf import settings
import pandas as pd
from django.core.files.base import ContentFile


Post = get_model(app_label="bulk_io_test", model_name="Post")
Comment = get_model(app_label="bulk_io_test", model_name="Comment")
URL = "admin:%s_%s_%s"


class TestBulkExportBase(TestCase):
    client = APIClient()
    BASE_DIR = str(settings.BASE_DIR)

    def setUp(self):
        self.user = self.create_superuser()
        self.client.force_login(self.user)

    def create_superuser(self):
        return User.objects.create_superuser(username="testuser", password="password")

    def bulk_io_url(self, info: tuple, action: str):
        return reverse(URL % (*info, action))


class TextCommentExport(TestBulkExportBase):
    ACTION = "bulk_export"

    def setUp(self):
        super().setUp()
        self.model = Comment
        self.opts = self.model._meta
        self.url = self.bulk_io_url(
            info=(self.opts.app_label, self.opts.model_name), action=self.ACTION
        )

    def handle_success_file_response(self, content: dict):
        """Get File from url and create csv Object and checks if it is equals to queryset"""
        self.assertEqual(BulkIOMessages.CSV_CREATED_SUCCESSFULLY, content["message"])
        self.assertIn("file", content)
        self.assertIn("url", content["file"])
        self.assertIn("title", content["file"])

    def create_comments(self):
        return CommentFactory.create_batch(size=10)

    def export_file_data(self, url: str):
        with open(url, "r") as fp:
            df = pd.read_csv(ContentFile(content=fp.read()))
        return df.to_dict(orient="records")

    def test_comment_select_across(self):
        comments = self.create_comments()
        response = self.client.post(self.url, data={"select_across": 1})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        content = loads(response.content)
        self.handle_success_file_response(content=content)
        data = self.export_file_data(url=self.BASE_DIR + content["file"]["url"])
        self.assertEqual(len(comments), len(data))

    def test_comment_select_some(self):
        comments = self.create_comments()
        ids = [comment.id for comment in comments[: randint(1, 9)]]
        response = self.client.post(
            self.url, data={"_selected_action": ",".join(map(str, ids))}
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        content = loads(response.content)
        self.handle_success_file_response(content=content)
        data = self.export_file_data(url=self.BASE_DIR + content["file"]["url"])
        self.assertEqual(len(ids), len(data))

    def test_comment_select_none(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        content = loads(response.content)
        self.assertEqual(BulkIOException.REQUEST_PAYLOAD_EMPTY, content["message"])

    def test_comment_select_invalid(self):
        response = self.client.post(self.url, data={"_selected_action": ""})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        content = loads(response.content)
        self.assertEqual(BulkIOException.INVALID_REQUEST_BODY, content["message"])
