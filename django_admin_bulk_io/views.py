# Django Admin Bulk IO Views
from django.views.generic import ListView
from django.apps import apps
from django_admin_bulk_io.forms import DynamicExportForm
from django_admin_bulk_io.utils import get_admin_class_for_model_instance

def get_model(app_label: str, model_name: str):
    """
    retuns models instance
    :param app_label: user's app label
    :param model_name: user's model name
    :return: model instance
    """

    return apps.get_model(app_label=app_label, model_name=model_name)


class BulkIOBaseView(ListView):
    template_name = "admin/bulk_io_base.html"

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model_name
        context['app_label'] = self.app_label
        context['action'] = self.action
        context['model'] = self.model
        context['model_fields'] = self.model_fields
        return context

    def dispatch(self, request, *args, **kwargs):
        try:
            self.app_label, self.model_name, self.action = [ i for i in  self.request.path.split("/") if i not in ["","admin"]]
            self.model = get_model(app_label=self.app_label, model_name=self.model_name)
            self.model_fields = self.model._meta.get_fields()
            return super().dispatch(request, *args, **kwargs)
        except Exception as err:
            return self.handle_exception(request, err)

    def handle_exception(self, request, exception):
        return self.render_to_response(context={"error": str(exception)})


class BulkImportView(ListView):
    template_name = "admin/bulk_import.html"


bulk_import_view = BulkImportView.as_view()


class BulkExportView(BulkIOBaseView):
    template_name = "admin/bulk_export.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        admin_class = get_admin_class_for_model_instance(self.model)
        return context

bulk_export_view = BulkExportView.as_view()
