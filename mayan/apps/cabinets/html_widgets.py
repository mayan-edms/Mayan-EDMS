from django.template.loader import render_to_string

from .permissions import permission_cabinet_view


def widget_document_cabinets(document, user):
    """
    A tag widget that displays the tags for the given document
    """
    return render_to_string(
        template_name='cabinets/document_cabinets_widget.html', context={
            'cabinets': document.get_cabinets(
                permission=permission_cabinet_view, user=user
            )
        }
    )


def widget_single_cabinet(cabinet):
    return render_to_string(
        template_name='cabinets/cabinet_widget.html', context={
            'cabinet': cabinet
        }
    )
