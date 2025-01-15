# Bulk IO - Django Based Dynamic Model Form with Filter Fields Based on ModelAdmin filter_queryset attribute

from django import forms
from django.forms.models import ModelForm
from django_admin_bulk_io.utils import get_admin_class_for_model_instance


class DynamicExportForm(ModelForm):
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model
        self.admin_class = get_admin_class_for_model_instance(self.model)
        if self.admin_class is None:
            raise ValueError("Admin class not found for model %s" % model)
        model_admin = self.admin_class()
        self.Meta.model = self.model

        for field in model_admin.model._meta.fields:
            self.fields[field.name] = forms.BooleanField(
                required=False, label=field.verbose_name
            ) 

    class Meta:
        model = None
