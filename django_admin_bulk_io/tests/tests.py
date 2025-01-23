from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
import csv
from io import StringIO
from django.apps import apps


class TestAdminBulkIO(TestCase):
    client = APIClient()
    maxDiff = None

    def setUp(self):
        self.model = apps.get_model(
            app_label="django_admin_bulk_io", model_name="BulkIOExport"
        )
        self.model_import = apps.get_model(
            app_label="django_admin_bulk_io", model_name="BulkIOImport"
        )

    def create_csv_file(self, data):
        csv_file = StringIO()
        writer = csv.writer(csv_file)
        writer.writerow(data.keys())
        for row in data.values():
            writer.writerow(row.values())
        csv_file.seek(0)
        return csv_file

    def upload_csv_file(self, url, data):
        csv_file = self.create_csv_file(data)
        file = SimpleUploadedFile("test.csv", csv_file.read(), content_type="text/csv")
        response = self.client.post(url, {"file": file}, format="multipart")
        return response

    def get_url(self, app_label, model_name, action):
        return reverse(f"{app_label}_{model_name}_{action}")

    def assert_response_ok(self, response, message):
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], message)

    def assert_response_bad_request(self, response, message):
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], message)

    def assert_response_internal_server_error(self, response, message):
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data["message"], message)

    def assert_model_created(self, model, count):
        self.assertEqual(model.objects.count(), count)

    def assert_model_not_created(self, model, count):
        self.assertEqual(model.objects.count(), count)

    def assert_file_created(self, model, count):
        self.assertEqual(model.objects.count(), count)

    def assert_file_not_created(self, model, count):
        self.assertEqual(model.objects.count(), count)

    def assert_equal_data(self, data1, data2):
        self.assertEqual(len(data1), len(data2))
        for i in range(len(data1)):
            self.assertEqual(data1[i], data2[i])

    def assert_equal_file_data(self, file1, file2):
        self.assertEqual(file1.read(), file2.read())
        file1.seek(0)
        file2.seek(0)
        self.assertEqual(file1.name, file2.name)
        self.assertEqual(file1.size, file2.size)
        self.assertEqual(file1.content_type, file2.content_type)
        self.assertEqual(file1.charset, file2.charset)
        self.assertEqual(file1.content_type_extra, file2.content_type_extra)
        self.assertEqual(file1.url, file2.url)
        self.assertEqual(file1.title, file2.title)

    def assert_equal_file_data_list(self, file_list1, file_list2):
        self.assertEqual(len(file_list1), len(file_list2))
        for i in range(len(file_list1)):
            self.assert_equal_file_data(file_list1[i], file_list2[i])

    def tearDown(self):
        self.model.objects.all().delete()
        self.model_import.objects.all().delete()

    def create_data(self, count=1):
        data = []
        for i in range(count):
            data.append({"name": f"test_{i}", "age": i})
        return data

    def create_model_instance(self, data):
        return self.model.objects.create(**data)

    def create_model_import_instance(self, data):
        return self.model_import.objects.create(**data)

    def create_file(self, data):
        csv_file = self.create_csv_file(data)
        file = SimpleUploadedFile("test.csv", csv_file.read(), content_type="text/csv")
        return file

    def create_file_instance(self, file):
        return self.model.objects.create(file=file)

    def create_file_import_instance(self, file):
        return self.model_import.objects.create(file=file)

    def create_csv_data(self, count=1):
        data = {}
        for i in range(count):
            data[f"row_{i}"] = {"name": f"test_{i}", "age": i}
        return data
