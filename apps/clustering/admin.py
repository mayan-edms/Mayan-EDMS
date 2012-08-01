from __future__ import absolute_import

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Node


class NodeAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'cpuload', 'heartbeat', 'memory_usage')


admin.site.register(Node, NodeAdmin)
