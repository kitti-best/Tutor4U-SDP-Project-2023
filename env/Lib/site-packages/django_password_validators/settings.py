from django.conf import settings
from django.utils.module_loading import import_string


def get_password_hasher():
    history_hasher = getattr(
        settings,
        'DPV_DEFAULT_HISTORY_HASHER',
        'django_password_validators.password_history.hashers.HistoryHasher'
    )
    return import_string(history_hasher)
