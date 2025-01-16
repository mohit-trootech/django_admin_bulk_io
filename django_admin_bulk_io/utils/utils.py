from django.contrib import admin


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
