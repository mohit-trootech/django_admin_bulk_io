from ast import literal_eval
from logging import Logger
from os import makedirs

import pandas as pd
from django.conf import settings
from django.contrib import admin
from django.db.models import Model
from django.utils.timezone import now

from django_admin_bulk_io.utils.constants import FILE_NAME_TEMPLATE


def log_messages(errors: list, logger: Logger) -> None:
    """
    This method logs the errors.
    :param errors: list of errors
    """
    for error in errors:
        logger(error)


def get_model_fields_info(model: Model) -> tuple[list[str], list[str]]:
    """
    This method returns required & optional fields for given model.
    :param model: model instance
    :return: tuple of required and optional fields list
    """
    required = set()
    optional = set()
    for field in model._meta.get_fields():
        try:
            if field.field.blank is False and field.field.null is False:
                required.add(field.field)
            else:
                optional.add(field.field)
        except AttributeError:
            if field.blank is False and field.null is False:
                required.add(field)
            else:
                optional.add(field)
    if model._meta.many_to_many:
        for field in model._meta.many_to_many:
            if field.blank is False and field.null is False:
                required.add(field)
            else:
                optional.add(field)
    return list(required), list(optional)


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


def generate_csv_from_serialized_data(data: dict) -> str:
    """
    use pandas to generate csv from queryset
    :param data: dict
    :return: str
    """
    df = pd.DataFrame.from_records(data=data)
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
        if field.name in df.columns:
            if field.many_to_many:
                df[field.name] = df[field.name].apply(lambda x: literal_eval(x))
            df.dropna(subset=[field.name], inplace=True)
    for field in optional:
        if field.name in df.columns:
            if field.many_to_many:
                df[field.name] = df[field.name].apply(lambda x: literal_eval(x))
            if df[field.name].isna().any():
                df.drop(columns=[field.name], inplace=True)
    return df.to_dict(orient="records")
