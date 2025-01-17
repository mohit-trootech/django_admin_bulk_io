# Django Admin Bulk I/O Forms

from django import forms
from django.forms.models import ModelForm
from django_admin_bulk_io.utils.utils import get_admin_class_for_model_instance
from django_admin_bulk_io.utils.constants import (
    FormFields,
    InputTypes,
    FORM_CLASS_BASE,
)

class DynamicExportForm(ModelForm):
 

    def __init__(self, model, *args, **kwargs):
        if model:
            self._meta.model = model
        super(DynamicExportForm, self).__init__(*args, **kwargs)
        self.admin_class = get_admin_class_for_model_instance(self._meta.model)
        if self.admin_class:
            for field in self.admin_class.list_filter:
                field = self._meta.model._meta.get_field(field)
                if field.get_internal_type() in FormFields.char_accepted():
                    field_type = forms.CharField
                    input_type_class = forms.TextInput
                elif field.choices:
                    field_type = forms.ChoiceField
                    input_type_class = forms.Select
                elif field.get_internal_type() in FormFields.boolean_accepted():
                    field_type = forms.BooleanField
                    input_type_class = forms.CheckboxInput
                else:
                    continue
                if field.choices:
                    self.fields[field.name] = field_type(
                        choices=field.choices,
                        widget=input_type_class(
                            attrs={
                                "type": InputTypes.TEXT,
                                "class": FORM_CLASS_BASE,
                                "placeholder": field.verbose_name,
                            }
                        ),
                    )
                else:
                    self.fields[field.name] = field_type(
                        required=False,
                        widget=input_type_class(
                            attrs={
                                "type": InputTypes.TEXT,
                                "class": FORM_CLASS_BASE,
                                "placeholder": field.verbose_name,
                            }
                        ),
                    )

    class Meta:
        model = None
        fields = []
