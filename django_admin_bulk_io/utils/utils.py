from ast import literal_eval
from logging import Logger
from os import makedirs

import pandas as pd
from django.conf import settings
from django.db.models import Model
from django.utils.timezone import now

from django_admin_bulk_io.utils.constants import FILE_NAME_TEMPLATE


def log_messages(error: str, logger: Logger) -> None:
    """
    This method logs the errors.
    :param errors: list of errors
    """
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


def save_csv_file_in_base_dir(csv_str: str, info: tuple) -> None:
    """
    save csv string in base dir handle exceptions
    :param csv_str: str
    :param app_label: str
    :param model_name: str
    :return: None
    """
    filename = generate_csv_filename()
    file_path = FILE_NAME_TEMPLATE % (settings.BASE_DIR, *info)
    try:
        makedirs(file_path)
    except FileExistsError:
        pass
    full_path = f"{file_path}{filename}"

    def create_file():
        with open(full_path, "w") as f:
            f.write(csv_str)

    create_file()


def validate_data_from_csv_file(model: Model, csv_str: str) -> dict:
    """
    import & clean csv file data for optional field and returns dict of data

    :param model: Model
    :param csv_file: str
    :return: dict
    """
    df = pd.read_csv(csv_str)
    df.drop_duplicates(inplace=True)
    if model._meta.pk.name in df.columns:
        df.drop(columns=[model._meta.pk.name], inplace=True)
    _, optional = get_model_fields_info(model=model)  # noqa
    for field in optional:
        if field.name in df.columns:
            if df[field.name].isna().any():
                df.drop(columns=[field.name], inplace=True)
    return df.to_dict(orient="records")


def get_data_from_csv_file(model: Model, csv_str: str) -> dict:
    """
    import & clean csv file data and returns dict of data
    :param model: Model
    :param csv_file: str
    :param fields: list
    :return: dict
    """
    # TODO: Remove all Columns which are not in Field List.
    df = pd.read_csv(csv_str)
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
