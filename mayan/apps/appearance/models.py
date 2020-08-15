from django.conf import settings
from django.db import models, transaction
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from .events import event_theme_created, event_theme_edited


class Theme(models.Model):
    label = models.CharField(
        db_index=True, help_text=_('A short text describing the theme.'),
        max_length=128, unique=True, verbose_name=_('Label')
    )
    stylesheet = models.TextField(
        blank=True, help_text=_(
            'The CSS stylesheet to change the appearance of the different '
            'user interface elements.'
        ), verbose_name=_('Stylesheet')
    )

    class Meta:
        ordering = ('label',)
        verbose_name = _('Theme')
        verbose_name_plural = _('Themes')

    def __str__(self):
        return force_text(self.label)

    def get_absolute_url(self):
        return reverse(
            viewname='appearance:theme_edit', kwargs={
                'theme_id': self.pk
            }
        )

    def save(self, *args, **kwargs):
        _user = kwargs.pop('_user', None)

        with transaction.atomic():
            is_new = not self.pk
            super().save(*args, **kwargs)
            if is_new:
                event_theme_created.commit(
                    actor=_user, target=self
                )
            else:
                event_theme_edited.commit(
                    actor=_user, target=self
                )


class UserThemeSetting(models.Model):
    user = models.OneToOneField(
        on_delete=models.CASCADE, related_name='theme_settings',
        to=settings.AUTH_USER_MODEL, verbose_name=_('User')
    )
    theme = models.ForeignKey(
        blank=True, null=True, on_delete=models.CASCADE,
        related_name='user_setting', to=Theme, verbose_name=_('Theme')
    )

    class Meta:
        verbose_name = _('User theme setting')
        verbose_name_plural = _('User theme settings')

    def __str__(self):
        return force_text(self.user)
