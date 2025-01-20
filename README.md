# Django Admin Bulk I/O

This package allows you to perform bulk import and export operations within the Django admin interface.  It provides a user-friendly way to handle large datasets without the limitations of the standard Django admin's changelist.

## Features

* **Bulk Import:**  Import data from various formats (CSV, JSON, etc.) into your Django models.  Handles data validation and error reporting.
* **Bulk Export:** Export data from your Django models to various formats (CSV, JSON, etc.).  Supports custom field selection and data transformation.
* **User-Friendly Interface:**  Integrates seamlessly with the Django admin, providing a familiar and intuitive experience.
* **Flexible and Extensible:**  Easily customizable to fit your specific needs and data structures.

## Installation

```bash
pip install django-admin-bulk-io
```

## Usage

1. **Add `bulk_io` to your `INSTALLED_APPS`:**

```python
INSTALLED_APPS = [
    # ... other apps ...
    'django_admin_bulk_io',
]
```

2. **Register your models:**  No additional registration is needed; the package automatically integrates with your existing Django models.

3. **Use the bulk import/export functionality within the Django admin interface.**  You'll find new buttons in the changelist view for each model.

## Configuration

The package offers several configuration options to customize its behavior.  Refer to the [settings documentation](settings.md) for details.

## Contributing

Contributions are welcome!  Please see the [contributing guidelines](CONTRIBUTING.md) for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
