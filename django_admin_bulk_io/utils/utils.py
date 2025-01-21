import pandas as pd
from os import makedirs
from django.conf import settings
from django.contrib import admin
from django.utils.timezone import now
from django_admin_bulk_io.utils.constants import FILE_NAME_TEMPLATE
from django_admin_bulk_io.serializer import BulkIODynamicSerializer
from django.db.models import Model


def get_dynamic_serializer(my_model: Model):

    class DynamicModelSerializer(BulkIODynamicSerializer):

        class Meta(BulkIODynamicSerializer.Meta):
            model = my_model

    return DynamicModelSerializer


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
    full_path = f"{file_path}{filename}"

    def create_file():
        with open(full_path, "w") as f:
            f.write(csv_str)

    create_file()
    return full_path, filename


def import_csv_file(model, csv_file, fields):
    """Import CSV File"""
    try:
        df = pd.read_csv(csv_file)
        nan_fields = df.columns[df.isna().any()].tolist()
        print(nan_fields)
        df.drop(columns=list(nan_fields), inplace=True)
        if "id" in df.columns:
            df.drop(columns=["id"], inplace=True)
        serializer_class = get_dynamic_serializer(my_model=model)
        serializer = serializer_class(data=df.to_dict(orient="records"), many=True)
        if serializer.is_valid():
            return serializer.save()
        else:
            raise Exception(serializer.errors)
    except Exception as e:
        raise e
