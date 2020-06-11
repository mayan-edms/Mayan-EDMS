from django import forms

from mayan.apps.views.widgets import TextAreaDiv

from .classes import Dependency


class DependenciesLicensesForm(forms.Form):
    text = forms.CharField(
        label='',
        widget=TextAreaDiv(
            attrs={
                'class': 'full-height scrollable',
                'data-height-difference': 270,
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(DependenciesLicensesForm, self).__init__(*args, **kwargs)
        copyright_texts = []

        for dependency in Dependency.get_all():
            copyright_text = dependency.get_copyright()
            if copyright_text:
                copyright_texts.append('-' * len(dependency.get_label()))
                copyright_texts.append(dependency.get_label().strip())
                copyright_texts.append('-' * len(dependency.get_label()))

                # Implement word wrapping at 79 columns.
                for line in copyright_text.split('\n'):
                    line_length = 0
                    new_line = []

                    for word in line.strip().split():
                        if line_length + len(word) > 79:
                            copyright_texts.append(' '.join(new_line))
                            new_line = [word]
                            line_length = 0
                        else:
                            new_line.append(word)
                            line_length = line_length + len(word)

                    copyright_texts.append(' '.join(new_line))

                copyright_texts.append('\n')

        self.fields['text'].initial = '\n'.join(copyright_texts)
