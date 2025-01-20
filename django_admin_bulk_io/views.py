# Django Admin Bulk I/O Views
from django.apps import apps
from http import HTTPStatus
from django.db.models import Q
from django.db.models import Model
from django.http import JsonResponse
from django.db.models import QuerySet
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django_admin_bulk_io.utils.constants import (
    Templates,
    BulkIOException,
    BulkIOMessages,
    Keys,
)
from django.views import View
from django_admin_bulk_io.utils.utils import (
    get_admin_class_for_model_instance,
    generate_csv_from_queryset,
    import_csv_file,
)
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.messages import error, info


def get_model(app_label: str, model_name: str) -> Model:
    """
    This method returns model class for given app label and model name.
    """
    return apps.get_model(app_label=app_label, model_name=model_name)


@method_decorator(csrf_exempt, name="dispatch")
class BulkIOBaseView(View):
    template_name = Templates.BASE_IO

    # def get_queryset(self) -> QuerySet:
    #     search_fields = self.admin_class.get_search_fields(self.request)
    #     query = Q()
    #     if search_fields:
    #         search_term = self.request.GET.get("q")
    #         if search_term:
    #             for field in search_fields:
    #                 query &= Q(**{field + "__icontains": search_term})
    #     if self.request.GET:
    #         form = DynamicExportForm(model=self.model, data=self.request.GET)
    #         if form.is_valid():
    #             for field in form.cleaned_data:
    #                 if form.cleaned_data[field]:
    #                     query &= Q(**{field + "__exact": form.cleaned_data[field]})
    #     return self.model.objects.filter(query)

    # def get_context_data(self, **kwargs) -> dict:
    #     context = super().get_context_data(**kwargs)
    #     context["opts"] = self.model._meta
    #     context["model_name"] = self.model_name
    #     context["app_label"] = self.app_label
    #     context["action"] = self.action
    #     context["model"] = self.model
    #     context["model_fields"] = self.fields
    #     return context

    def dispatch(self, request, *args, **kwargs):
        self.app_label, self.model_name, self.action = [
            path for path in self.request.path.split("/") if path not in ["", "admin"]
        ]
        self.model = get_model(app_label=self.app_label, model_name=self.model_name)
        self.admin_class = get_admin_class_for_model_instance(instance=self.model)
        self.fields = self.admin_class.get_fields(request=self.request)
        return super().dispatch(request, *args, **kwargs)


class BulkImportView(BulkIOBaseView):
    template_name = Templates.BULK_IMPORT_HTML

    def post(self, request, *args, **kwargs):
        try:
            csv_file = request.FILES["file"]
            if not csv_file:
                raise BulkIOException.FILE_NOT_FOUND
            self.model.objects.bulk_create(
                import_csv_file(model=self.model, csv_file=csv_file, fields=self.fields)
            )
            info(request, BulkIOMessages.CSV_IMPORTED_SUCCESSFULLY)
            return redirect(
                reverse("admin:%s_%s_bulk_import" % (self.app_label, self.model_name))
            )
        except Exception as e:
            error(request, str(e))
            return redirect(
                reverse("admin:%s_%s_bulk_import" % (self.app_label, self.model_name))
            )


bulk_import_view = BulkImportView.as_view()


class BulkExportView(BulkIOBaseView):

    def get_queryset(self):
        return self.model.objects.all()

    def get_query_params(self):
        return dict(self.request.GET)

    def get_search_fields(self):
        return self.admin_class.get_search_fields(self.request)

    def get_filtered_queryset(self, queryset, query_params):
        search = query_params.pop("q")
        query = Q()
        search_fields = self.get_search_fields()
        if search_fields and search:
            for field in search_fields:
                query &= Q(**{field + "__icontains": search})
        if query_params:
            for field in query_params:
                query &= Q(**{field: query_params[field][0]})
        return queryset.filter(query)

    def get_queryset_with_ids(self, queryset: QuerySet, ids: list) -> QuerySet:
        return queryset.filter(pk__in=ids)

    def post(self, request, *args, **kwargs):
        if not request.POST.get(Keys.SELECTED_IDS):
            return JsonResponse(
                {"message": BulkIOException.REQUEST_BODY_EMPTY},
                status=HTTPStatus.BAD_REQUEST,
            )
        ids = request.POST.get(Keys.SELECTED_IDS).split(",")
        filtered_queryset = self.get_queryset_with_ids(
            queryset=self.get_queryset(), ids=ids
        )
        csv_str = generate_csv_from_queryset(filtered_queryset)
        return JsonResponse(
            {"message": BulkIOMessages.CSV_CREATED_SUCCESSFULLY},
            status=HTTPStatus.OK,
        )


bulk_export_view = BulkExportView.as_view()
