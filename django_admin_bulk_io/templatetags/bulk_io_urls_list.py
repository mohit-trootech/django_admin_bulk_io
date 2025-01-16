from django.template import Library
from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_admin_bulk_io.utils.constants import Exception
register = Library()

def bulk_io_reverse(app_label, model_name, path_template:str):
    """returns bulk io url reverse based on app_label & model_name directly"""

    url_name = path_template % (app_label, model_name)
    url = reverse(f"admin:{url_name}")
    return url


@register.simple_tag(name="bulk_io_urls")
def do_bulk_io_urls(*args):
    """
    This template tag renders the bulk import and export links for a given model.
    """
    app_label, model_name = args
    return BulkIOUrlsNode(app_label, model_name).render()
   


class BulkIOUrlsNode(template.Node):
    def __init__(self, app_label, model_name):
        self.app_label = app_label
        self.model_name = model_name

    def render(self, *args):
        try:
            url_import = bulk_io_reverse(self.app_label, self.model_name, "%s_%s_bulk_import")
            url_export = bulk_io_reverse(self.app_label, self.model_name, "%s_%s_bulk_export")
            return mark_safe(
            """
                <li>
                    <a href="%s" class="">Bulk Import</a>
                </li>
                <li>
                    <a href="%s" class="">Bulk Export</a>
                </li>
            """
            % (url_import, url_export)
        )
        except ValueError as ve:
            print(Exception.ERROR_URL_REVERSE.format(ve=ve))
            return mark_safe()
