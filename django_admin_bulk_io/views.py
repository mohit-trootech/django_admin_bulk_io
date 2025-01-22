# Django Admin Bulk I/O Views
from django.apps import apps
from http import HTTPStatus
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
    LogMessages,
    AcceptedTypes,
)
from django.views import View
from django_admin_bulk_io.utils.utils import (
    get_admin_class_for_model_instance,
    generate_csv_from_queryset,
    get_data_from_csv_file,
    generate_csv_filename,
)
from django.core.files.base import ContentFile
from logging import Logger
from django.conf import settings
from django_admin_bulk_io.serializer import BulkIODynamicSerializer


logger = Logger(__name__) if settings.LOGGING else None


def get_model(app_label: str, model_name: str) -> Model:
    """
    This method returns model class for given app label and model name.
    """
    return apps.get_model(app_label=app_label, model_name=model_name)


BulkIOExport = get_model(app_label="django_admin_bulk_io", model_name="BulkIOExport")
BulkIOImport = get_model(app_label="django_admin_bulk_io", model_name="BulkIOImport")


@method_decorator(csrf_exempt, name="dispatch")
class BulkIOBaseView(View):
    template_name = Templates.BASE_IO

    def dispatch(self, request, *args, **kwargs):
        self.app_label, self.model_name, self.action = [
            path for path in self.request.path.split("/") if path not in ["", "admin"]
        ]
        self.model = get_model(app_label=self.app_label, model_name=self.model_name)
        self.admin_class = get_admin_class_for_model_instance(model_instance=self.model)
        self.fields = self.admin_class.get_fields(request=self.request)
        return super().dispatch(request, *args, **kwargs)


class BulkImportView(BulkIOBaseView):
    template_name = Templates.BULK_IMPORT_HTML
    serializer_class = BulkIODynamicSerializer

    def get_serializer(self):
        self.serializer_class.Meta.model = self.model
        return self.serializer_class

    def post(self, request, *args, **kwargs):
        log_message = LogMessages.LOGGER_NOT_CONFIGURED
        try:
            if not request.FILES:
                if logger:
                    log_message = LogMessages.NO_FILES_TO_IMPORT
                    logger.warning(log_message)
                return JsonResponse(
                    {"message": BulkIOException.FILE_NOT_FOUND},
                    status=HTTPStatus.BAD_REQUEST,
                )
            file = request.FILES["file"]
            if file.content_type not in AcceptedTypes.get_accepted_types_list():
                if logger:
                    log_message = LogMessages.FILE_TYPE_NOT_SUPPORTED
                    logger.warning(log_message)
                return JsonResponse(
                    {"message": BulkIOException.FILE_TYPE_NOT_SUPPORTED},
                    status=HTTPStatus.BAD_REQUEST,
                )
            data = get_data_from_csv_file(
                model=self.model, csv_file=file, fields=self.fields
            )
            serializer_class = self.get_serializer()
            serializer = serializer_class(data=data, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse(
                {"message": BulkIOMessages.CSV_IMPORTED_SUCCESSFULLY},
                status=HTTPStatus.OK,
            )
        except Exception as err:
            if logger:
                log_message = str(err)
                logger.error(log_message)
            return JsonResponse(
                {"message": log_message}, status=HTTPStatus.INTERNAL_SERVER_ERROR
            )


bulk_import_view = BulkImportView.as_view()


class BulkExportView(BulkIOBaseView):

    def get_queryset(self):
        return self.model.objects.all()

    def get_queryset_with_ids(self, queryset: QuerySet, ids: list) -> QuerySet:
        return queryset.filter(pk__in=ids)

    def post(self, request, *args, **kwargs):
        log_message = LogMessages.LOGGER_NOT_CONFIGURED
        try:
            payload = request.POST.get(Keys.SELECTED_IDS)
            if not payload:
                if logger:
                    log_message = LogMessages.REQUEST_PAYLOAD_EMPTY
                    logger.warning(BulkIOException.REQUEST_BODY_EMPTY % log_message)
                return JsonResponse(
                    {"message": BulkIOException.REQUEST_BODY_EMPTY % log_message},
                    status=HTTPStatus.BAD_REQUEST,
                )
            ids = payload.split(",")
            filtered_queryset = self.get_queryset_with_ids(
                queryset=self.get_queryset(), ids=ids
            )
            csv_str = generate_csv_from_queryset(filtered_queryset, self.model)
            title = generate_csv_filename()
            file = BulkIOExport.objects.create(
                file=ContentFile(content=csv_str, name=title)
            )
            return JsonResponse(
                {
                    "message": BulkIOMessages.CSV_CREATED_SUCCESSFULLY,
                    "file": {"url": file.url, "title": file.title},
                },
                status=HTTPStatus.OK,
            )
        except Exception as err:
            if logger:
                log_message = BulkIOException.UNKNOWN_EXCEPTION_OCCURED % str(err)
                logger.error(log_message)
            return JsonResponse(
                {"message": log_message}, status=HTTPStatus.INTERNAL_SERVER_ERROR
            )


bulk_export_view = BulkExportView.as_view()
