from http import HTTPStatus
from random import choice

import pandas as pd
from django.core.files.base import ContentFile
from django_extensions.db.models import ActivatorModel
from faker import Faker

from bulk_io_test.tests.base import TestBulkIOBase
from bulk_io_test.tests.factory import CommentFactory, UserFactory
from django_admin_bulk_io.utils.constants import BulkIOException, BulkIOMessages
from utils.utils import get_model

fake = Faker()
Comment = get_model(app_label="bulk_io_test", model_name="Comment")
Post = get_model(app_label="bulk_io_test", model_name="Post")
DEFAULT_NUM_ROWS = 10


class TestBulkValidationBase(TestBulkIOBase):
    ACTION = "bulk_validate"

    def create_csv_file_from_content(
        self, content: str, name: str = "test.csv"
    ) -> ContentFile:
        """
        Create a csv file from given content.
        :param content: str
        :param name: str = "test.csv"
        """
        return ContentFile(content=content, name=name)

    def bulk_validate_post_no_file(self):
        response = self.client.post(self.url)
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(BulkIOException.REQUEST_BODY_EMPTY, response.json()["message"])

    def bulk_validate_post_invalid_file_type(self):
        file = self.create_csv_file_from_content(
            content="invalid file content", name="test.txt"
        )
        response = self.client.post(self.url, data={"file": file})
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(
            BulkIOException.FILE_TYPE_NOT_SUPPORTED, response.json()["message"]
        )

    def invalid_csv_file(self):
        file = self.create_csv_file_from_content(content="invalid file content")
        response = self.client.post(self.url, data={"file": file})
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(BulkIOException.INVALID_CSV_FILE, response.json()["message"])

    def bulk_validate_post_empty_file(self):
        file = self.create_csv_file_from_content(content=b"", name="test.csv")
        response = self.client.post(self.url, data={"file": file})
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(BulkIOException.FILE_EMPTY, response.json()["message"])


class TestBulkValidationComment(TestBulkValidationBase):

    def setUp(self):
        self.model = Comment
        super(TestBulkValidationComment, self).setUp()

    def create_valid_csv_content(self, num_rows: int):
        """
        Create CSV content for self.model with num_rows rows.
        :param num_rows: int
        """
        df = pd.DataFrame(
            {
                "title": [fake.name() for _ in range(num_rows)],
                "description": [fake.text() for _ in range(num_rows)],
                "created": [fake.date() for _ in range(num_rows)],
                "status": [
                    choice(
                        [ActivatorModel.INACTIVE_STATUS, ActivatorModel.ACTIVE_STATUS]
                    )
                    for _ in range(num_rows)
                ],
            }
        )
        return df.to_csv(index=False)

    def create_invalid_csv_content(self, num_rows: int):
        """
        Create invalid csv content for self.model with num_rows rows. if iteration is odd, create invalid data entry by removing the title.
        :param num_rows: int
        """
        items = []
        for row in range(num_rows):
            if row % 2 == 0:
                items.append(
                    {
                        "title": fake.name(),
                        "description": fake.text(),
                        "created": fake.date(),
                        "status": choice(
                            [
                                ActivatorModel.INACTIVE_STATUS,
                                ActivatorModel.ACTIVE_STATUS,
                            ]
                        ),
                    }
                )
            else:
                items.append(
                    {
                        "title": "",
                        "description": fake.text(),
                        "created": fake.date(),
                        "status": choice([3, 4, 5, 6, 7]),
                    }
                )
        df = pd.DataFrame(items)
        return df.to_csv(index=False)

    def test_bulk_validate_no_errors(self):
        """
        Test bulk validation of models with all validated data
        """
        csv_content = self.create_valid_csv_content(num_rows=DEFAULT_NUM_ROWS)
        file = self.create_csv_file_from_content(content=csv_content)
        response = self.client.post(self.url, data={"file": file})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(
            BulkIOMessages.CSV_VALIDATED_SUCCESSFULLY % 0,
            response.json()["message"],
        )

    def test_bulk_import_with_errors(self):
        """
        Test bulk import of models with some invalid data
        """
        csv_content = self.create_invalid_csv_content(num_rows=DEFAULT_NUM_ROWS)
        file = self.create_csv_file_from_content(content=csv_content)
        response = self.client.post(self.url, data={"file": file})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(
            BulkIOMessages.CSV_VALIDATED_SUCCESSFULLY % (DEFAULT_NUM_ROWS // 2),
            response.json()["message"],
        )

    def test_bulk_validate_post_invalid_file_type(self):
        super(TestBulkValidationComment, self).bulk_validate_post_invalid_file_type()

    def test_invalid_csv_file(self):
        super(TestBulkValidationComment, self).invalid_csv_file()

    def test_bulk_import_post_empty_file(self):
        super(TestBulkValidationComment, self).bulk_validate_post_empty_file()

    def test_bulk_validate_post_no_file(self):
        super(TestBulkValidationComment, self).bulk_validate_post_no_file()


class TestBulkValidationPost(TestBulkValidationBase):
    def setUp(self):
        self.model = Post
        super(TestBulkValidationPost, self).setUp()

    def create_valid_csv_content(self, num_rows: int):
        comment = CommentFactory.create()
        users = UserFactory.create_batch(num_rows)
        df = pd.DataFrame(
            {
                "title": [fake.name() for _ in range(num_rows)],
                "description": [fake.text() for _ in range(num_rows)],
                "comment": comment.id,
                "likes": [[user.id for user in users] for _ in range(num_rows)],
            }
        )
        return df.to_csv(index=False)

    def create_invalid_csv_content(self, num_rows: int):
        comment = CommentFactory.create()
        users = UserFactory.create_batch(num_rows)
        items = []
        for row in range(num_rows):
            if row % 2 == 0:
                items.append(
                    {
                        "title": fake.name(),
                        "description": fake.text(),
                        "comment": comment.id,
                        "likes": [user.id for user in users],
                    }
                )
            else:
                items.append(
                    {
                        "title": "",
                        "description": fake.text(),
                        "comment": 9,
                        "likes": [user.id for user in users],
                    }
                )
        df = pd.DataFrame(items)
        return df.to_csv(index=False)

    def test_bulk_validate_no_errors(self):
        """
        Test bulk validation of models with all validated data
        """
        csv_content = self.create_valid_csv_content(num_rows=DEFAULT_NUM_ROWS)
        file = self.create_csv_file_from_content(content=csv_content)
        response = self.client.post(self.url, data={"file": file})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(
            BulkIOMessages.CSV_VALIDATED_SUCCESSFULLY % 0,
            response.json()["message"],
        )

    def test_bulk_import_with_errors(self):
        """
        Test bulk import of models with some invalid data
        """
        csv_content = self.create_invalid_csv_content(num_rows=DEFAULT_NUM_ROWS)
        file = self.create_csv_file_from_content(content=csv_content)
        response = self.client.post(self.url, data={"file": file})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(
            BulkIOMessages.CSV_VALIDATED_SUCCESSFULLY % (DEFAULT_NUM_ROWS // 2),
            response.json()["message"],
        )

    def test_bulk_validate_post_invalid_file_type(self):
        super(TestBulkValidationPost, self).bulk_validate_post_invalid_file_type()

    def test_invalid_csv_file(self):
        super(TestBulkValidationPost, self).invalid_csv_file()

    def test_bulk_import_post_empty_file(self):
        super(TestBulkValidationPost, self).bulk_validate_post_empty_file()

    def test_bulk_validate_post_no_file(self):
        super(TestBulkValidationPost, self).bulk_validate_post_no_file()
