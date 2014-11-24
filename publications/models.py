# coding=utf-8
from __future__ import unicode_literals
from django.db import models
from pytils.translit import slugify


class SlugAndTitleMixin(models.Model):
    TITLE_MAX_LENGTH = 400
    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        verbose_name="Title"
    )
    slug = models.SlugField(
        max_length=int(TITLE_MAX_LENGTH*1.2),
        unique=True,
        db_index=True,
        verbose_name="SID",
        help_text="Уникальный тестовй идентификатор объекта. Используется для построения урлов"
    )

    def __unicode__(self):
        return '<%s: "%s">' % (self.__class__.__name__, self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(SlugAndTitleMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class PublishedManager(models.Manager):
    def published(self):
        return self.get_queryset().filter(status_code=2)

    def drafted(self, with_published=False):
        kwargs = dict(status_code__gte=1) if with_published else dict(status_code=1)
        return self.get_queryset().filter(**kwargs)

    def visible(self, is_admin=False):
        return self.drafted(True) if is_admin else self.published()


class StatusMixin(models.Model):
    STATUSES = {
        0: 'Скрыто',
        1: 'Черновик',
        2: 'Опубликовано'
    }

    status_code = models.SmallIntegerField(
        choices=STATUSES.items(),
        default=STATUSES.items()[0][0],
        db_index=True,
        verbose_name=u"Статус",
    )

    objects = PublishedManager()

    def get_status(self):
        return self.STATUSES[self.status_code]

    class Meta:
        abstract = True


class AbstractSimplePublication(SlugAndTitleMixin, StatusMixin, models.Model):
    content = models.TextField(
        null=True,
        blank=True,
        verbose_name="Контент"
    )

    class Meta:
        verbose_name = "Простая публикация"
        verbose_name_plural = "Простые публикации"
        abstract = True