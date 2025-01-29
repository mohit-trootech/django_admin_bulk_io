# Custom Django Admin Bulk IO Exceptions


class RequestBodyEmpty(Exception):
    pass


class FileTypeNotSupported(Exception):
    pass


class InvalidCSVFile(Exception):
    pass


class EmptyFile(Exception):
    pass
