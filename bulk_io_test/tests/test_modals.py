from django.test import TestCase
from utils.utils import get_model
from django.contrib.auth import get_user_model
from bulk_io_test.tests.factory import CommentFactory, PostFactory, UserFactory

Comment = get_model(app_label="bulk_io_test", model_name="Comment")
Post = get_model(app_label="bulk_io_test", model_name="Post")
User = get_user_model()


class BaseTestModal(TestCase):
    model = None

    def validate_model(self, qs: list):
        self.assertTrue(isinstance(qs, self.model))

    def validate_many_to_many(self, qs: list, count: int):
        self.assertEqual(qs.count(), count)


class TestCommentModal(BaseTestModal):

    def setUp(self):
        super().setUp()
        self.model = Comment

    def test_comment_model(self):
        super(TestCommentModal, self).validate_model(qs=CommentFactory())


class TestUserModal(BaseTestModal):

    def setUp(self):
        super().setUp()
        self.model = User

    def test_user_model(self):
        super(TestUserModal, self).validate_model(qs=UserFactory())


class TestPostModal(BaseTestModal):

    def setUp(self):
        super().setUp()
        self.model = Post

    def test_post_model(self):
        super(TestPostModal, self).validate_model(qs=PostFactory())

    def test_post_likes_user_m2m(self):
        likes = UserFactory.create_batch(size=3)
        post = PostFactory(likes=likes)
        super(TestPostModal, self).validate_many_to_many(
            qs=post.likes, count=(len(likes))
        )
