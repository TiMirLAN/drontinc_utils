# coding=utf-8
from __future__ import unicode_literals
from drontinc.fields import PgTextArrayField
from django.db import models
__author__ = 'timirlan'


class PgTaggedMixin(models.Model):
    tags = PgTextArrayField(
        null=True,
        blank=True,
        max_length=20,
        verbose_name="Тэги"
    )

    class Meta:
        abstract = True