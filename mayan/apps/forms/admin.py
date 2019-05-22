from __future__ import unicode_literals

from django.contrib import admin

from .models import FieldChoice, FormTemplate, FormTemplateField


@admin.register(FieldChoice)
class FieldChoiceAdmin(admin.ModelAdmin):
    list_display = ('label', 'dotted_path')


class FormTemplateFieldInline(admin.StackedInline):
    model = FormTemplateField
    extra = 1
    classes = ('collapse-open',)
    allow_add = True


@admin.register(FormTemplate)
class FormTemplateAdmin(admin.ModelAdmin):
    inlines = (FormTemplateFieldInline,)
    list_display = ('name', 'label', 'enabled')
