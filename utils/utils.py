def get_model(app_label: str, model_name: str):
    """
    retuns models instance
    :param app_label: user's app label
    :param model_name: user's model name
    :return: model instance
    """
    from django.apps import apps

    return apps.get_model(app_label=app_label, model_name=model_name)
