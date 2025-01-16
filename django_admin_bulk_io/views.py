# Django Admin Bulk I/O Views
from django.apps import apps
from django.db.models import Q
from django.db.models import Model
from django.db.models import QuerySet
from django.views.generic import ListView
from django_admin_bulk_io.forms import DynamicExportForm
from django_admin_bulk_io.utils.constants import Templates


def get_model_fields(model: Model) -> list:
    """
    This method returns list of fields for given model.
    """
    fields = []
    for field in model._meta.get_fields():
        if not field.is_relation and field.name != "id":
            fields.append(field)
    return fields


def get_model(app_label: str, model_name: str) -> Model:
    """
    This method returns model class for given app label and model name.
    """
    return apps.get_model(app_label=app_label, model_name=model_name)


class BulkIOBaseView(ListView):
    template_name = Templates.BASE_IO

    def get_queryset(self) -> QuerySet:
        query = Q()
        if self.request.GET:
            for key, value in self.request.GET.items():
                query = query & Q(**{key: value})
        return self.model.objects.filter(query)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["opts"] = self.model._meta
        context["model_name"] = self.model_name
        context["app_label"] = self.app_label
        context["action"] = self.action
        context["model"] = self.model
        context["model_fields"] = self.model_fields
        return context

    def dispatch(self, request, *args, **kwargs):
        try:
            self.app_label, self.model_name, self.action = [
                i for i in self.request.path.split("/") if i not in ["", "admin"]
            ]
            self.model = get_model(app_label=self.app_label, model_name=self.model_name)
            self.model_fields = self.model._meta.get_fields()
            return super().dispatch(request, *args, **kwargs)
        except Exception as err:
            return self.handle_exception(request, err)

    def handle_exception(self, request, exception):
        return self.render_to_response(context={"error": str(exception)})


class BulkImportView(BulkIOBaseView):
    template_name = Templates.BULK_IMPORT_HTML


bulk_import_view = BulkImportView.as_view()


class BulkExportView(BulkIOBaseView):
    template_name = Templates.BULK_EXPORT_HTML
    form_class = DynamicExportForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.form_class:
            context["form"] = self.form_class(model=self.model)
        return context


bulk_export_view = BulkExportView.as_view()
