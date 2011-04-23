from django.contrib import admin

from folders.models import Folder, FolderDocument


class FolderDocumentInline(admin.StackedInline):
    model = FolderDocument
    extra = 1
    classes = ('collapse-open',)
    allow_add = True


class FolderAdmin(admin.ModelAdmin):
    inlines = [FolderDocumentInline]


admin.site.register(Folder, FolderAdmin)
