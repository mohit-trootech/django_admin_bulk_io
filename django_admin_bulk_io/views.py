# Django Admin Bulk I/O Views
from django.apps import apps
from http import HTTPStatus
from django.db.models import Q
from django.db.models import Model
from django.http import JsonResponse
from django.db.models import QuerySet
from django.views.generic import View, ListView
from django_admin_bulk_io.forms import DynamicExportForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django_admin_bulk_io.utils.constants import (
    Templates,
    BulkIOException,
    BulkIOMessages,
)
from django_admin_bulk_io.utils.utils import (
    get_admin_class_for_model_instance,
    save_csv_file_in_base_dir,
    generate_csv_from_queryset,
)


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


@method_decorator(csrf_exempt, name="dispatch")
class BulkIOBaseView(ListView):
    template_name = Templates.BASE_IO

    def get_queryset(self) -> QuerySet:
        self.admin_class = get_admin_class_for_model_instance(instance=self.model)
        search_fields = self.admin_class.get_search_fields(self.request)
        query = Q()
        if search_fields:
            search_term = self.request.GET.get("q")
            if search_term:
                for field in search_fields:
                    query &= Q(**{field + "__icontains": search_term})
        if self.request.GET:
            form = DynamicExportForm(model=self.model, data=self.request.GET)
            if form.is_valid():
                for field in form.cleaned_data:
                    if form.cleaned_data[field]:
                        query &= Q(**{field + "__exact": form.cleaned_data[field]})
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
        self.app_label, self.model_name, self.action = [
            path for path in self.request.path.split("/") if path not in ["", "admin"]
        ]
        self.model = get_model(app_label=self.app_label, model_name=self.model_name)
        self.model_fields = get_model_fields(model=self.model)
        return super().dispatch(request, *args, **kwargs)


class BulkImportView(BulkIOBaseView):
    template_name = Templates.BULK_IMPORT_HTML


bulk_import_view = BulkImportView.as_view()


class BulkExportView(BulkIOBaseView, View):
    template_name = Templates.BULK_EXPORT_HTML
    form_class = DynamicExportForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.form_class:
            context["form"] = self.form_class(model=self.model)
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get("select-all"):
            queryset = self.get_queryset()
        else:
            instances = request.POST.getlist("instance")
            if not instances:
                return JsonResponse(
                {"message": BulkIOException.REQUEST_BODY_EMPTY}, status=HTTPStatus.BAD_REQUEST
            )
            queryset = self.get_queryset().filter(id__in=instances)
        csv_str = generate_csv_from_queryset(queryset)
        save_csv_file_in_base_dir(csv_str, self.app_label, self.model_name)
        return JsonResponse(
            {"message": BulkIOMessages.CSV_CREATED_SUCCESSFULLY},
            status=HTTPStatus.OK,
        )


bulk_export_view = BulkExportView.as_view()
