from django.views.generic import FormView, TemplateView

from .forms import SettingsForm

#class EditorView(TemplateView):
#    template_name = 'settings_editor/editor_window.html'


class EditorView(FormView):
    template_name = 'main/generic_form.html'
    form_class = SettingsForm
