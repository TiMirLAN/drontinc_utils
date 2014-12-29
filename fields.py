# coding=utf-8
from django.core.exceptions import ValidationError
from django import forms
from django.db import models
__author__ = 'timirlan'


class PgArrayCharField(forms.CharField):
    def prepare_value(self, value):
        if isinstance(value, list):
            value = ', '.join(value)
        return super(PgArrayCharField, self).prepare_value(value)


# ARRAYS

class ArrayIndexLookup(models.Lookup):
    """
    Хм. Даже я уже забыл, что эта штука должна делать...
    """
    lookup_name = 'array_index'

    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        print rhs_params
        params = lhs_params + rhs_params
        return '%s <> %s' % (lhs, rhs), params


class ArrayContainsLookup(models.Lookup):
    """
    Lookup проверки содержимого массива
    """
    lookup_name = 'array_contains'

    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        new_rhs_params = [p.replace('{', 'ARRAY[').replace('}', ']') for p in rhs_params]
        return '%s @> %s' % (lhs, rhs), lhs_params + rhs_params


# TODO добавить функцию получения одного/нескольких элементов массива sql запросом (Model.objects.filter(*).values_list)
class PgTextArrayField(models.Field):
    # TODO сделать одно поле PgArrayField с выбираемым типом элементов.
    def db_type(self, connection):
        return 'text ARRAY[%s]' % self.max_length

    def get_prep_value(self, value):
        if value is None:
            v = u"{}"
        elif isinstance(value, dict):
            v = value
        elif isinstance(value, list) or isinstance(value, tuple):
            v = u"{%s}" % u','.join([
                i for i in value
            ])
        elif isinstance(value, unicode) or isinstance(value, str):
            v = u"{%s}" % value
        else:
            raise ValidationError('Not convertabe')
        return super(PgTextArrayField, self).get_prep_value(v)

    def formfield(self, **kwargs):
        defaults = dict(
            form_class=PgArrayCharField
        )
        defaults.update(kwargs)
        return super(PgTextArrayField, self).formfield(**defaults)
PgTextArrayField.register_lookup(ArrayIndexLookup)
PgTextArrayField.register_lookup(ArrayContainsLookup)