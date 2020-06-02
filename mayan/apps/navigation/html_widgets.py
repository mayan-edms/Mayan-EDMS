from django.template.loader import render_to_string


class SourceColumnLinkWidget:
    template_name = 'navigation/source_column_link_widget.html'

    def render(self, name=None, value=None):
        return render_to_string(
            template_name=self.template_name, context={
                'column': self.column, 'value': value
            }
        )
