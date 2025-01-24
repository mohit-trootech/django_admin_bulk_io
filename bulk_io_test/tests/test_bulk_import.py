from bulk_io_test.tests.base import TestBulkIOBase
from random import randint, choice, uniform
import pandas as pd
from io import StringIO
from utils.utils import get_model
import factory
from faker import Faker
import csv

fake = Faker()
Comment = get_model(app_label="bulk_io_test", model_name="Comment")
Post = get_model(app_label="bulk_io_test", model_name="Post")


class TestBulkImportBase(TestBulkIOBase):
    ACTION = "bulk_import"

    def handle_success_response(self, content: dict):
        self.assertEqual(200, content["status"])
        self.assertEqual("success", content["message"])

    # def import_file_data(self, filepath: str):
    #     with open(filepath, "rb") as fp:
    #         response = self.client.post(self.url, data={"file": fp})
    #         self.assertEqual(200, response.status_code)
    #         content = response.json()
    #         self.handle_success_response(content=content)

    def get_model_fields(self):
        return self.opts.fields

    def create_dynamic_csv_content(model, num_rows):

        fields = model._meta.fields
        data = []

        for _ in range(num_rows):
            row_data = {}
            for field in fields:
                # Generate fake data based on field type
                if isinstance(field, factory.django.ImageField):
                    row_data[field.name] = "path/to/image.jpg"
                elif isinstance(field, factory.django.FileField):
                    row_data[field.name] = "path/to/file.txt"
                elif isinstance(field, factory.django.BooleanField):
                    row_data[field.name] = choice([True, False])
                elif isinstance(field, factory.django.DateTimeField):
                    row_data[field.name] = (
                        fake.date_time_this_year().isoformat()
                    )  # ISO format for datetime
                elif isinstance(field, factory.django.DateField):
                    row_data[field.name] = (
                        fake.date_this_year().isoformat()
                    )  # ISO format for date
                elif isinstance(field, factory.django.ForeignKey):
                    related_model = field.related_model
                    try:
                        related_object = related_model.objects.order_by("?").first()
                        if related_object:
                            row_data[field.name] = related_object.pk
                        else:
                            row_data[field.name] = ""
                    except Exception:
                        row_data[field.name] = (
                            ""  # Handle cases where no related model instances exist
                        )
                elif isinstance(field, factory.django.ManyToManyField):
                    # Skip ManyToManyFields (handle separately if needed)
                    continue  # Or generate comma-separated values
                elif isinstance(
                    field, (factory.django.IntegerField, factory.django.BigIntegerField)
                ):  # Handle Integer Fields
                    row_data[field.name] = randint(1, 1000)
                elif isinstance(field, factory.django.FloatField):  # Handle FloatField
                    row_data[field.name] = uniform(1.0, 1000.0)

                else:  # CharField, TextField, etc.
                    row_data[field.name] = fake.word()

            data.append(row_data)
        df = pd.DataFrame(data)
        csv_buffer = StringIO()
        df.to_csv(
            csv_buffer, index=False, quoting=csv.QUOTE_ALL
        )  # Use quoting to handle commas in fields
        csv_content = csv_buffer.getvalue()
        csv_buffer.close()
        return csv_content


class TestBulkImportComment(TestBulkImportBase):

    def setUp(self):
        super().setUp()
        self.model = Comment
        self.opts = self.model._meta

    def test_bulk_import_comment(self):
        csv_content = self.create_dynamic_csv_content(self.model, num_rows=10)
        csv_file = StringIO(csv_content)
        response = self.client.post(self.url, data={"file": csv_file})
        self.assertEqual(200, response.status_code)
        content = response.json()
        self.handle_success_response(content=content)
        self.assertEqual(10, Comment.objects.count())

    def test_bulk_import_comment_with_errors(self):
        # Create CSV data with some invalid entries
        csv_content = self.create_dynamic_csv_content(self.model, num_rows=10)
        # Introduce an error, e.g., missing required field
        csv_content = csv_content.replace("test", "")
        csv_file = StringIO(csv_content)
        response = self.client.post(self.url, data={"file": csv_file})
        self.assertEqual(200, response.status_code)
        content = response.json()
        self.assertEqual(200, content["status"])
        self.assertEqual("partial_success", content["message"])
        self.assertIn("errors", content)
        # Assertions to check the error details


class TestBulkImportPost(TestBulkImportBase):
    def setUp(self):
        super().setUp()
        self.model = Post
        self.opts = self.model._meta

    def test_bulk_import_post(self):
        csv_content = self.create_dynamic_csv_content(self.model, num_rows=10)
        csv_file = StringIO(csv_content)
        response = self.client.post(self.url, data={"file": csv_file})
        self.assertEqual(200, response.status_code)
        content = response.json()
        self.handle_success_response(content=content)
        self.assertEqual(10, Post.objects.count())

    def test_bulk_import_post_with_errors(self):
        # Create CSV data with some invalid entries
        csv_content = self.create_dynamic_csv_content(self.model, num_rows=10)
        # Introduce an error, e.g., missing required field
        csv_content = csv_content.replace("test", "")
        csv_file = StringIO(csv_content)
        response = self.client.post(self.url, data={"file": csv_file})
        self.assertEqual(200, response.status_code)
        content = response.json()
        self.assertEqual(200, content["status"])
        self.assertEqual("partial_success", content["message"])
        self.assertIn("errors", content)
        # Assertions to check the error details
