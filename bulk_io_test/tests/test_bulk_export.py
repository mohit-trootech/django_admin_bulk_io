import pandas as pd
from json import loads
from random import randint
from rest_framework import status
from utils.utils import get_model
from django.core.files.base import ContentFile
from bulk_io_test.tests.base import TestBulkIOBase
from bulk_io_test.tests.factory import PostFactory, CommentFactory, UserFactory
from django_admin_bulk_io.utils.constants import BulkIOMessages, BulkIOException


Post = get_model(app_label="bulk_io_test", model_name="Post")
Comment = get_model(app_label="bulk_io_test", model_name="Comment")


class TestBulkExportBase(TestBulkIOBase):
    ACTION = "bulk_export"

    def handle_success_file_response(self, content: dict):
        """Get File from url and create csv Object and checks if it is equals to queryset"""
        self.assertEqual(BulkIOMessages.CSV_CREATED_SUCCESSFULLY, content["message"])
        self.assertIn("file", content)
        self.assertIn("url", content["file"])
        self.assertIn("title", content["file"])

    def export_file_data(self, url: str):
        with open(url, "r") as fp:
            df = pd.read_csv(ContentFile(content=fp.read()))
        return df.to_dict(orient="records")

    def select_across(self, qs: list):
        response = self.client.post(self.url, data={"select_across": 1})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        content = loads(response.content)
        self.handle_success_file_response(content=content)
        data = self.export_file_data(url=self.BASE_DIR + content["file"]["url"])
        self.assertEqual(len(qs), len(data))

    def select_some(self, qs: list):
        ids = [comment.id for comment in qs[: randint(1, 9)]]
        response = self.client.post(
            self.url, data={"_selected_action": ",".join(map(str, ids))}
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        content = loads(response.content)
        self.handle_success_file_response(content=content)
        data = self.export_file_data(url=self.BASE_DIR + content["file"]["url"])
        self.assertEqual(len(ids), len(data))

    def select_none(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        content = loads(response.content)
        self.assertEqual(BulkIOException.REQUEST_PAYLOAD_EMPTY, content["message"])

    def select_invalid(self):
        response = self.client.post(self.url, data={"_selected_action": ""})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        content = loads(response.content)
        self.assertEqual(BulkIOException.INVALID_REQUEST_BODY, content["message"])


class CommentSetUp(TestBulkExportBase):

    def setUp(self):
        super().setUp()
        self.model = Comment
        self.opts = self.model._meta
        self.url = self.bulk_io_url(
            info=(self.opts.app_label, self.opts.model_name), action=self.ACTION
        )


class PostSetUp(TestBulkExportBase):

    def setUp(self):
        super(PostSetUp, self).setUp()
        self.model = Post
        self.opts = self.model._meta
        self.url = self.bulk_io_url(
            info=(self.opts.app_label, self.opts.model_name), action=self.ACTION
        )


class CommentBulkExportTest(CommentSetUp):

    def create_comments(self):
        return CommentFactory.create_batch(size=10)

    def test_post_select_across(self):
        super(CommentBulkExportTest, self).select_across(qs=self.create_comments())

    def test_post_select_some(self):
        super(CommentBulkExportTest, self).select_some(qs=self.create_comments())

    def test_comment_select_none(self):
        super(CommentBulkExportTest, self).select_none()

    def test_comment_select_invalid(self):
        super(CommentBulkExportTest, self).select_invalid()


class PostBulkExportTest(PostSetUp):

    def create_posts(self):
        likes = UserFactory.create_batch(size=10)
        return PostFactory.create_batch(size=10, likes=likes[: randint(1, 9)])

    def test_post_select_across(self):
        super(PostBulkExportTest, self).select_across(qs=self.create_posts())

    def test_post_select_some(self):
        super(PostBulkExportTest, self).select_some(qs=self.create_posts())

    def test_post_select_none(self):
        super(PostBulkExportTest, self).select_none()

    def test_post_select_invalid(self):
        super(PostBulkExportTest, self).select_invalid()
