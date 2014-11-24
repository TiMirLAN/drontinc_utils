from django.core.exceptions import ValidationError
from django import forms
from django.db import models
__author__ = 'timirlan'


class PgArrayCharField(forms.CharField):
    def prepare_value(self, value):
        if isinstance(value, list):
            value = ', '.join(value)
        return super(PgArrayCharField, self).prepare_value(value)


class PgTextArrayField(models.Field):
    def db_type(self, connection):
        return 'text ARRAY[%s]' % self.max_length

    def get_prep_value(self, value):
        print '>>', value
        if value is None:
            v = u"{}"
        elif isinstance(value, unicode):
            v = u"{%s}" % value
        else:
            raise ValidationError('Not convertabe')
        print '==', v
        return super(PgTextArrayField, self).get_prep_value(v)

    def formfield(self, **kwargs):
        defaults = dict(
            form_class=PgArrayCharField
        )
        defaults.update(kwargs)
        return super(PgTextArrayField, self).formfield(**defaults)