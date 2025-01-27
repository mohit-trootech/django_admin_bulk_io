# Django Admin Bulk I/O Constants

FORM_CLASS_BASE = "form-control bg-light text-dark"
FILE_NAME_TEMPLATE = "{base_path}/bulk_io/{app_label}/{model_name}/"


class AcceptedTypes:
    """Bulk IO - File Accepted Content Types"""

    CSV = "text/csv"
    JSON = "application/json"

    @classmethod
    def get_accepted_types_list(cls) -> list:
        return [cls.CSV]


class Keys:
    """Bulk IO - Request Keys"""

    ACTION_TOGGLE = "action-toggle"
    SELECTED_ACTION = "_selected_action"
    SELECT_ALL = "select_across"


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

    CSV_CREATED_SUCCESSFULLY = "CSV Generated Successfully,"
    CSV_IMPORTED_SUCCESSFULLY = "%s New records created."
    CSV_IMPORTED_WITH_EXCEPTIONS = "%s New records created with exceptions. %s"


class BulkIOException:
    """Bulk IO - Exceptions"""

    ERROR_URL_REVERSE = "Error reversing URL: {ve}."
    REQUEST_BODY_EMPTY = "Request body is empty."
    FILE_NOT_FOUND = "File not found."
    UNKNOWN_EXCEPTION_OCCURED = "Error, Please view log file for details."
    FILE_TYPE_NOT_SUPPORTED = "File type not supported."
    INVALID_CSV_FILE = "Invalid CSV file."
    INVALID_JSON_FILE = "Invalid JSON file."
    REQUEST_PAYLOAD_EMPTY = "No data to export."
    INVALID_REQUEST_BODY = "Invalid request body."
    FILE_EMPTY = "File is empty."


class LogMessages:
    """Bulk IO - Log Messages"""

    VIEW_LOG_FOR_DETAILS = "Please view log file for details."
    LOGGER_NOT_CONFIGURED = "Please configure logger for more details."
    REQUEST_PAYLOAD_EMPTY = "No data to export."
    NO_FILES_TO_IMPORT = "No files to import."
    FILE_TYPE_NOT_SUPPORTED = "File type not supported."
    UNKNOWN_EXCEPTION_OCCURED = "Error, %s"
