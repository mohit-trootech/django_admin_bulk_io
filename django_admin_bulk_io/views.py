# Django Admin Bulk IO Views
from django.views.generic import ListView, TemplateView
from django.contrib.admin import helpers

def get_model(app_label: str, model_name: str):
    """
    retuns models instance
    :param app_label: user's app label
    :param model_name: user's model name
    :return: model instance
    """
    from django.apps import apps

    return apps.get_model(app_label=app_label, model_name=model_name)


class BulkIOBaseView(TemplateView):
    def get_queryset(self):
        breakpoint()
        self.model = get_model(
            self.kwargs['app_label'], self.kwargs['model_name']
        )  
        return super().get_queryset()
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        breakpoint()
        context["adminform"] = helpers.AdminForm(
            self.model,
            self.get_form(self.request),
            self.request.POST or None,
            {},
            self.get_fields(self.request),
            self.get_readonly_fields(self.request),
            model_admin=self,
        )
        return context


class BulkImportView(ListView):
    template_name = "admin/bulk_import.html"

bulk_import_view = BulkImportView.as_view()


class BulkExportView(BulkIOBaseView):
    template_name = "admin/bulk_export.html"


bulk_export_view = BulkExportView.as_view()
