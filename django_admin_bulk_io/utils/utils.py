import pandas as pd
from os import makedirs
from django.conf import settings
from django.contrib import admin
from django.utils.timezone import now
from django_admin_bulk_io.utils.constants import FILE_NAME_TEMPLATE


def get_admin_class_for_model_instance(instance):
    """
    Retrieves the ModelAdmin class associated with a model instance.

    Args:
        instance: An instance of a Django model.

    Returns:
        The ModelAdmin class associated with the model, or None if not found.
    """
    for model, admin_class in admin.site._registry.items():
        if model == instance:
            return admin_class
    return None


def generate_csv_filename() -> str:
    """
    generate csv filename
    :return: str
    """

    return f"bulk_io_{now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"


def generate_csv_from_queryset(queryset) -> str:
    """
    use pandas to generate csv from queryset
    """
    df = pd.DataFrame.from_records(queryset.values())
    return df.to_csv(index=False)


def save_csv_file_in_base_dir(csv_str: str, app_label, model_name) -> None:
    """
    save csv string in base dir handle exceptions
    """
    filename = generate_csv_filename()
    file_path = FILE_NAME_TEMPLATE.format(
        base_path=settings.BASE_DIR,
        app_label=app_label,
        model_name=model_name,
    )
    try:
        makedirs(file_path)
    except FileExistsError:
        pass

    def create_file():
        with open(file_path + filename, "w") as f:
            f.write(csv_str)

    create_file()


def import_csv_file(model, csv_file, fields):
    """Import CSV File"""
    df = pd.read_csv(csv_file)
    df = df[fields]
    objs = []
    for _, row in df.iterrows():
        obj = model(**row.to_dict())
        objs.append(obj)
    return objs
