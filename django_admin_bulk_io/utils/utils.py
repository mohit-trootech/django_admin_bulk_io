import pandas as pd
from os import makedirs
from django.conf import settings
from django.contrib import admin
from django.utils.timezone import now
from django_admin_bulk_io.utils.constants import FILE_NAME_TEMPLATE
from django.db.models import Model, QuerySet
from logging import Logger


def log_messages(errors: list, logger: Logger) -> None:
    """
    This method logs the errors.
    :param errors: list of errors
    """
    for error in errors:
        logger(error)


def get_model_fields_info(model: Model) -> tuple[list[str], list[str]]:
    """
    This method returns required fields for given model.
    :param model: model instance
    :return: tuple of required and optional fields list
    """
    required = []
    optional = []
    for field in model._meta.fields:
        if field.blank is False and field.null is False:
            required.append(field)
        else:
            optional.append(field)
    return required, optional


def get_admin_class_for_model_instance(model_instance: Model) -> admin.ModelAdmin:
    """
    Retrieves the ModelAdmin class associated with a model.
    :param: model_instance: An model_instance of a Django model.
    :return: The ModelAdmin class associated with the model, or None if not found.
    """
    for model, admin_class in admin.site._registry.items():
        if model == model_instance:
            return admin_class
    return None


def generate_csv_filename() -> str:
    """
    generate csv filename with timestamp
    :return: str
    """

    return f"bulk_io_{now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"


def generate_csv_from_queryset(queryset: QuerySet) -> str:
    """
    use pandas to generate csv from queryset
    :param queryset: QuerySet
    :param model: Model
    :return: str
    """
    df = pd.DataFrame.from_records(queryset.values())
    return df.to_csv(index=False)


def save_csv_file_in_base_dir(csv_str: str, app_label: str, model_name: str) -> None:
    """
    save csv string in base dir handle exceptions
    :param csv_str: str
    :param app_label: str
    :param model_name: str
    :return: None
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


def get_data_from_csv_file(model: Model, csv_file: str, fields: list) -> dict:
    """
    import & clean csv file data and returns dict of data
    :param model: Model
    :param csv_file: str
    :param fields: list
    :return: dict
    """

    df = pd.read_csv(csv_file)
    df.drop_duplicates(inplace=True)
    if model._meta.pk.name in df.columns:
        df.drop(columns=[model._meta.pk.name], inplace=True)
    required, optional = get_model_fields_info(model=model)
    for field in required:
        if field.is_relation:
            field_model = field.related_model
            df[field.attname] = df[field.attname].apply(
                lambda x: field_model.objects.filter(pk=x).values()[0]
            )
        if field.name in df.columns:
            df.dropna(subset=[field.name], inplace=True)
    for field in optional:
        if field.name in df.columns:
            if df[field.name].isna().any():
                df.drop(columns=[field.name], inplace=True)
    breakpoint()
    return df.to_dict(orient="records")
