from django.core.exceptions import ValidationError
try:
  from django.utils.translation import gettext as _, ngettext
except ImportError:
  from django.utils.translation import ugettext as _, ungettext as ngettext


class PasswordCharacterValidator():

    def __init__(
            self,
            min_length_digit=1,
            min_length_alpha=1,
            min_length_special=1,
            min_length_lower=1,
            min_length_upper=1,
            special_characters="~!@#$%^&*()_+{}\":;'[]"
    ):
        self.min_length_digit = min_length_digit
        self.min_length_alpha = min_length_alpha
        self.min_length_special = min_length_special
        self.min_length_lower = min_length_lower
        self.min_length_upper = min_length_upper
        self.special_characters = special_characters

    def validate(self, password, user=None):
        validation_errors = []
        if len([char for char in password if char.isdigit()]) < self.min_length_digit:
            validation_errors.append(ValidationError(
                ngettext(
                    'This password must contain at least %(min_length)d digit.',
                    'This password must contain at least %(min_length)d digits.',
                    self.min_length_digit
                ),
                params={'min_length': self.min_length_digit},
                code='min_length_digit',
            ))
        if len([char for char in password if char.isalpha()]) < self.min_length_alpha:
            validation_errors.append(ValidationError(
                ngettext(
                    'This password must contain at least %(min_length)d letter.',
                    'This password must contain at least %(min_length)d letters.',
                    self.min_length_alpha
                ),
                params={'min_length': self.min_length_alpha},
                code='min_length_alpha',
            ))
        if len([char for char in password if char.isupper()]) < self.min_length_upper:
            validation_errors.append(ValidationError(
                ngettext(
                    'This password must contain at least %(min_length)d upper case letter.',
                    'This password must contain at least %(min_length)d upper case letters.',
                    self.min_length_upper
                ),
                params={'min_length': self.min_length_upper},
                code='min_length_upper_characters',
            ))
        if len([char for char in password if char.islower()]) < self.min_length_lower:
            validation_errors.append(ValidationError(
                ngettext(
                    'This password must contain at least %(min_length)d lower case letter.',
                    'This password must contain at least %(min_length)d lower case letters.',
                    self.min_length_lower
                ),
                params={'min_length': self.min_length_lower},
                code='min_length_lower_characters',
            ))
        if len([char for char in password if char in self.special_characters]) < self.min_length_special:
            validation_errors.append(ValidationError(
                ngettext(
                    'This password must contain at least %(min_length)d special character.',
                    'This password must contain at least %(min_length)d special characters.',
                    self.min_length_special
                ),
                params={'min_length': self.min_length_special},
                code='min_length_special_characters',
            ))
        if validation_errors:
            raise ValidationError(validation_errors)

    def get_help_text(self):
        validation_req = []
        if self.min_length_alpha:
            validation_req.append(
                ngettext(
                    "%(min_length)s letter",
                    "%(min_length)s letters",
                    self.min_length_alpha
                ) % {'min_length': self.min_length_alpha}
            )
        if self.min_length_digit:
            validation_req.append(
                ngettext(
                    "%(min_length)s digit",
                    "%(min_length)s digits",
                    self.min_length_digit
                ) % {'min_length': self.min_length_digit}
            )
        if self.min_length_lower:
            validation_req.append(
                ngettext(
                    "%(min_length)s lower case letter",
                    "%(min_length)s lower case letters",
                    self.min_length_lower
                ) % {'min_length': self.min_length_lower}
            )
        if self.min_length_upper:
            validation_req.append(
                ngettext(
                    "%(min_length)s upper case letter",
                    "%(min_length)s upper case letters",
                    self.min_length_upper
                ) % {'min_length': self.min_length_upper}
            )
        if self.special_characters:
            validation_req.append(
                ngettext(
                    "%(min_length_special)s special character, such as %(special_characters)s",
                    "%(min_length_special)s special characters, such as %(special_characters)s",
                    self.min_length_special
                ) % {'min_length_special': str(self.min_length_special), 'special_characters': self.special_characters}
            )
        return _("This password must contain at least") + ' ' + ', '.join(validation_req) + '.'
