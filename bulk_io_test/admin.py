from django.contrib.admin import  register
from django_admin_bulk_io.bulk_io import BulkIOModelAdmin
from utils.utils import get_model

Comment = get_model(app_label="bulk_io_test", model_name="Comment")


@register(Comment)
class CommentAdmin(BulkIOModelAdmin):
    list_display = ("title", "created", "status")
    list_filter = ("created", "status")

