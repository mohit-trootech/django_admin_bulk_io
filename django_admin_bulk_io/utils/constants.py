# Django Admin Bulk I/O Constants

FORM_CLASS_BASE = "form-control bg-light text-dark"
FILE_NAME_TEMPLATE = "{base_path}/bulk_io/{app_label}/{model_name}/"


class Keys:
    """Bulk IO - Request Keys"""

    ACTION_TOGGLE = "action-toggle"
    SELECTED_ACTIONS = "_selected_actions"
    SELECTED_IDS = "selectedIds"


class Templates:
    """Bulk IO - Templates"""

    BASE_IO = "admin/bulk_io_base.html"
    BULK_IMPORT_HTML = "admin/bulk_import.html"
    BULK_EXPORT_HTML = "admin/bulk_export.html"


class InputTypes:
    """Bulk IO - Input Types"""

    TEXT = "text"
    CSV = "csv"
    XLSX = "xlsx"
    JSON = "json"

    @classmethod
    def types_accepted(cls) -> list:
        """
        This method returns accepted input types.
        :return list: list of accepted input types
        """
        return [cls.CSV, cls.XLSX, cls.JSON]


class FormLabels:
    """Bulk IO = Form Labels"""

    SEARCH = "Search"


class FormFields:
    """Bulk IO - Form Filter Fields"""

    CHAR_FIELD = "CharField"
    TEXT_FIELD = "TextField"
    BOOLEAN_FIELD = "BooleanField"
    NULL_BOOLEAN_FIELD = "NullBooleanField"
    CHOICE_FIELD = "ChoiceField"

    @classmethod
    def fields_accepted(cls) -> list:
        """
        This method returns accepted fields for filtering.
        :return list of accepted fields
        """
        return [
            cls.CHAR_FIELD,
            cls.TEXT_FIELD,
            cls.BOOLEAN_FIELD,
            cls.NULL_BOOLEAN_FIELD,
            cls.CHOICE_FIELD,
        ]

    @classmethod
    def boolean_accepted(cls) -> list:
        """
        This method returns accepted boolean fields for filtering.
        :return: list of accepted boolean fields
        """
        return [cls.BOOLEAN_FIELD, cls.NULL_BOOLEAN_FIELD]

    @classmethod
    def char_accepted(cls) -> list:
        """

        This method returns accepted char fields for filtering.
            :return: list: list of accepted char fields
        """
        return [cls.CHAR_FIELD, cls.TEXT_FIELD]

    @classmethod
    def choice_accepted(cls) -> list:
        """
        This method returns accepted choice fields for filtering.
        :return: list of accepted choice fields
        """
        return [cls.TEXT_FIELD, cls.CHAR_FIELD]


class BulkIOMessages:
    """Bulk IO - Success Messages"""

    CSV_CREATED_SUCCESSFULLY = "CSV Created Successfully, View 'bulk_io' folder."
    CSV_IMPORTED_SUCCESSFULLY = "CSV Imported Successfully."


class BulkIOException:
    """Bulk IO - Exceptions"""

    ERROR_URL_REVERSE = "Error reversing URL: {ve}."
    REQUEST_BODY_EMPTY = "Request body is empty."
    FILE_NOT_FOUND = "File not found."
