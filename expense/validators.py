from django.core.exceptions import ValidationError


def validate_max_file_size(value, max_size):
    filesize = value.size
    if filesize > max_size:
        raise ValidationError(
            "The maximum file size that can be uploaded is 5 MB."
        )
