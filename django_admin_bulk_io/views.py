from django.apps import apps
from django.db.models import Model
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
    generate_csv_from_serialized_data,
    get_data_from_csv_file,
    generate_csv_filename,
    log_messages,
)
from django.core.files.base import ContentFile
from logging import getLogger
from django_admin_bulk_io.serializer import BulkIODynamicSerializer
from django_admin_bulk_io.utils.bulkio_threading import MultiProcessPool
from django_admin_bulk_io.utils.response import JsonResponseRenderer

logger = getLogger(__name__)


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
    renderer = JsonResponseRenderer
    serializer_class = BulkIODynamicSerializer

    def get_serializer(self):
        self.serializer_class.Meta.model = self.model
        return self.serializer_class

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

    def post(self, request, *args, **kwargs):
        try:
            if not request.FILES:
                log_messages(
                    errors=[LogMessages.NO_FILES_TO_IMPORT], logger=logger.warning
                )
                return self.renderer.render_bad_request(
                    data={"message": BulkIOException.FILE_NOT_FOUND}
                )
            file = request.FILES["file"]
            if file.content_type not in AcceptedTypes.get_accepted_types_list():
                log_messages(
                    errors=[LogMessages.FILE_TYPE_NOT_SUPPORTED], logger=logger.warning
                )
                return self.renderer.render_bad_request(
                    data={"message": BulkIOException.FILE_TYPE_NOT_SUPPORTED}
                )
            data = get_data_from_csv_file(
                model=self.model, csv_file=file, fields=self.fields
            )
            if not data:
                return self.renderer.render_bad_request(
                    data={"message": BulkIOException.INVALID_CSV_FILE}
                )
            data.append({})
            serializer = self.get_serializer()
            errors = []
            for item in data:
                s = serializer(data=item)
                if s.is_valid():
                    s.save()
                    logger.info(f"Successfully saved the instance {s.data}")
                else:
                    errors.append(s.errors)
                    log_messages(s.errors, logger=logger.warning)
            BulkIOImport.objects.create(file=file)
            message = BulkIOMessages.CSV_IMPORTED_SUCCESSFULLY % (
                len(data) - len(errors),
            )
            if errors:
                log_message = LogMessages.LOGGER_NOT_CONFIGURED
                if logger:
                    log_message = LogMessages.VIEW_LOG_FOR_DETAILS
                message = BulkIOMessages.CSV_IMPORTED_WITH_EXCEPTIONS % (
                    len(data) - len(errors),
                    log_message,
                )
            return self.renderer.render_ok(data={"message": message})
        except Exception as err:
            log_messages(
                errors=[LogMessages.UNKNOWN_EXCEPTION_OCCURED % str(err)],
                logger=logger.error,
            )
            return self.renderer.render_internal_server_error(
                data={"message": BulkIOException.UNKNOWN_EXCEPTION_OCCURED},
            )


bulk_import_view = BulkImportView.as_view()


class BulkExportView(BulkIOBaseView):

    def get_queryset(self):
        return self.model.objects.all()

    def get_queryset_with_ids(self, queryset: QuerySet, ids: list) -> QuerySet:
        return queryset.filter(pk__in=ids)

    def post(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            if Keys.SELECT_ALL not in request.POST:
                payload = request.POST.get(Keys.SELECTED_ACTION).split(",")
                if not payload:
                    return self.renderer.render_bad_request(
                        data={"message": BulkIOException.REQUEST_BODY_EMPTY},
                    )
                queryset = self.get_queryset_with_ids(queryset=queryset, ids=payload)
            data = self.get_serializer()(queryset, many=True).data
            csv_str = generate_csv_from_serialized_data(data=data)
            title = generate_csv_filename()
            file = BulkIOExport.objects.create(
                file=ContentFile(content=csv_str, name=title)
            )
            return self.renderer.render_ok(
                data={
                    "message": BulkIOMessages.CSV_CREATED_SUCCESSFULLY,
                    "file": {"url": file.url, "title": file.title},
                },
            )
        except Exception as err:
            log_messages(
                errors=[LogMessages.UNKNOWN_EXCEPTION_OCCURED % str(err)],
                logger=logger.error,
            )
            return self.renderer.render_internal_server_error(
                data={"message": BulkIOException.UNKNOWN_EXCEPTION_OCCURED},
            )


bulk_export_view = BulkExportView.as_view()
