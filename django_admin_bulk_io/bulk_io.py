# Bulk Export Decorator Class
from django.contrib.admin import ModelAdmin
from django.urls import path
from django_admin_bulk_io.views import bulk_import_view, bulk_export_view

class BulkIO(ModelAdmin):

    def get_urls(self, *args, **kwargs):
        info = self.opts.app_label, self.opts.model_name
        urls = super(BulkIO, self).get_urls(*args, **kwargs)
        bulk_io_urls = [
            path(
                "export/",
                bulk_export_view,
                name="%s_%s_export" % info,
            ),
            path(
                "import/",
                bulk_import_view,
                name="%s_%s_import" % info,
            ),
        ]
        print(bulk_export_view)
        return bulk_io_urls + urls
