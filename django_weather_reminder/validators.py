from django.core.exceptions import ValidationError


def validate_frequency(value: int):
    values_set = {1, 3, 6, 12, 24}

    if value not in values_set:
        raise ValidationError(
            f'Value must be in the given values set - {values_set}'
        )
