from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from django.contrib.admin.widgets import FilteredSelectMultiple


from .models import (DocumentStateLog, State, StateTransition,
                     DocumentTypeStateCollection)


admin.site.register(DocumentStateLog)
admin.site.register(DocumentTypeStateCollection)
admin.site.register(State)
admin.site.register(StateTransition)
