from django.test import TestCase
from rest_framework.test import APIClient
from bulk_io_test.tests.factory import CommentFactory, PostFactory, UserFactory
from utils.utils import get_model

Comment = get_model(app_label="bulk_io_test", model_name="Comment")
Post = get_model(app_label="bulk_io_test", model_name="Post")


class TestModels(TestCase):
    def test_comment_model(self):
        comment = CommentFactory()
        self.assertTrue(isinstance(comment, Comment))

    def test_post_model(self):
        post = PostFactory()
        self.assertTrue(isinstance(post, Post))

    def test_user_model(self):
        user = UserFactory()
        self.assertTrue(isinstance(user, object))

    def test_post_likes_user_m2m(self):
        likes = UserFactory.create_batch(size=3)
        post = PostFactory(likes=likes)
        self.assertEqual(post.likes.count(), 3)
