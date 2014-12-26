# coding=utf-8
from __future__ import unicode_literals
from django.db import models
from django.utils.timezone import now

# Create your models here.


class CreatedAndChangedDateTimeMixin(models.Model):
    """
    Миксин даты создания/изменения объекта.
    Подразумевается, что эти даты остаются неизменными, если нужна изменяемая дата,
     то поле для неё должно быть созданно отдельно.
    """
    created_at = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
        editable=False,
        verbose_name="Дата создания"
    )
    modified_at = models.DateTimeField(
        db_index=True,
        auto_now=True,
        editable=True,
        verbose_name=u"Дата последнего изменения"
    )

    def get_creation_datetime(self):
        return self.created_at

    def get_last_modification_datetime(self):
        return self.modified_at

    class Meta:
        abstract = True
