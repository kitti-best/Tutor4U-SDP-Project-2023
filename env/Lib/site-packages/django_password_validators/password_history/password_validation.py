from __future__ import unicode_literals
import warnings

from django.core.exceptions import ValidationError

try:
    from django.utils.translation import gettext as _, ngettext
except ImportError:
    from django.utils.translation import ugettext as _, ngettext
from django_password_validators.settings import get_password_hasher
from django_password_validators.password_history.models import (
    PasswordHistory,
    UserPasswordHistoryConfig,
)


class UniquePasswordsValidator(object):
    """
    Validate whether the password was once used by the user.

    The password is only checked for an existing user.
    """

    def __init__(self, last_passwords=0):
        """

        :param last_passwords:
            * lookup_range > 0 - We check only the XXX latest passwords
            * lookup_range <= 0 - Check all passwords that have been used so far
        """
        self.last_passwords = int(last_passwords)

    def _user_ok(self, user):
        if not user:
            return

        user_pk = getattr(user, 'pk', None)
        if user_pk is None:
            warnings.warn(
                'An unsaved user model!s %r'
                % user
            )
            return

        if isinstance(user_pk, property):
            warnings.warn(
                'Not initialized user model! %r'
                % user
            )
            return

        return True

    def delete_old_passwords(self, user):
        if self.last_passwords > 0:
            # Delete old passwords that are outside the lookup_range
            password_ids = list(
                PasswordHistory.objects. \
                    filter(user_config__user=user). \
                    order_by('-date')[self.last_passwords:]. \
                    values_list('pk', flat=True)
            )
            if password_ids:
                PasswordHistory.objects.filter(pk__in=password_ids).delete()

    def validate(self, password, user=None):

        if not self._user_ok(user):
            return

        # We make sure there are no old passwords in the database.
        self.delete_old_passwords(user)

        for user_config in UserPasswordHistoryConfig.objects.filter(user=user):
            password_hash = user_config.make_password_hash(password)
            try:
                PasswordHistory.objects.get(
                    user_config=user_config,
                    password=password_hash
                )
                raise ValidationError(
                    _("You can not use a password that is already used in this application."),
                    code='password_used'
                )
            except PasswordHistory.DoesNotExist:
                pass

    def password_changed(self, password, user=None):

        if not self._user_ok(user):
            return

        user_config = UserPasswordHistoryConfig.objects.filter(
            user=user,
            iterations=get_password_hasher().iterations
        ).first()

        if not user_config:
            user_config = UserPasswordHistoryConfig()
            user_config.user = user
            user_config.save()

        password_hash = user_config.make_password_hash(password)

        # We are looking hash password in the database
        old_password, old_password__created = PasswordHistory.objects.get_or_create(
            user_config=user_config,
            password=password_hash
        )

        # We make sure there are no old passwords in the database.
        self.delete_old_passwords(user)

    def get_help_text(self):
        if self.last_passwords > 0:
            return ngettext(
                'Your new password can not be identical to any of the %(old_pass)d previously entered passwords.',
                'Your new password can not be identical to any of the %(old_pass)d previously entered passwords.',
                self.last_passwords
            ) % {'old_pass': self.last_passwords}

        else:
            return _('Your new password can not be identical to any of the previously entered.')
