
from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string
try:
  from django.utils.translation import gettext_lazy as _
except ImportError:
  from django.utils.translation import ugettext_lazy as _

from django_password_validators.settings import get_password_hasher


class UserPasswordHistoryConfig(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False
    )
    date = models.DateTimeField(
        _('When created salt'),
        auto_now_add=True,
        editable=False
    )
    salt = models.CharField(
        verbose_name=_('Salt for the user'),
        max_length=120,
        editable=False,
    )
    iterations = models.IntegerField(
        _('The number of iterations for hasher'),
        default=None,
        editable=False,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('Configuration')
        verbose_name_plural = _('Configurations')
        unique_together = (("user", "iterations",),)
        ordering = ['-user', 'iterations', ]

    def make_password_hash(self, password):
        """
        Generates a password  hash for the given password.

        Args:
            passaword - the password is not encrypted form
        """
        hasher = get_password_hasher()()
        return hasher.encode(password, self.salt, self.iterations)

    def _gen_password_history_salt(self):
        salt_max_length = self._meta.get_field('salt').max_length
        self.salt = get_random_string(length=salt_max_length)

    def save(self, *args, **kwargs):
        # When there is no salt as defined for a given user,
        # then we create the salt.
        if not self.salt:
            self._gen_password_history_salt()
        # We take iterations from the default Hasher
        if not self.iterations:
            self.iterations = get_password_hasher().iterations
        return super(UserPasswordHistoryConfig, self).save(*args, **kwargs)

    def __str__(self):
        return '%s [%d]' % (self.user, self.iterations)


class PasswordHistory(models.Model):
    user_config = models.ForeignKey(
        UserPasswordHistoryConfig,
        on_delete=models.CASCADE,
        editable=False
    )
    password = models.CharField(
        _('Password hash'),
        max_length=255,
        editable=False
    )
    date = models.DateTimeField(
        _('Date'),
        auto_now_add=True,
        editable=False
    )

    class Meta:
        verbose_name = 'Old password'
        verbose_name_plural = 'Password history'
        unique_together = (("user_config", "password",),)
        ordering = ['-user_config', 'password', ]

    def __str__(self):
        return '%s [%s]' % (self.user_config.user, self.date)
