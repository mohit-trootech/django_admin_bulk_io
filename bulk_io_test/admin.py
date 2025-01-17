from django.contrib.admin import  register, site, ModelAdmin
from django_admin_bulk_io.admin import BulkIOModelAdmin
from utils.utils import get_model

Comment = get_model(app_label="bulk_io_test", model_name="Comment")
Post = get_model(app_label="bulk_io_test", model_name="Post")
Like = get_model(app_label="bulk_io_test", model_name="Like")


@register(Comment)
class CommentAdmin(BulkIOModelAdmin):
    list_display = ("title", "created", "status")
    list_filter = ("created", "status")
    search_fields = ("title",)
    


@register(Post)
class PostAdmin(ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)

site.register(Like)