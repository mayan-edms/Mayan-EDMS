from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Menu

from .icons import icon_menu_documents

menu_documents = Menu(
    icon_class=icon_menu_documents, label=_('Documents'),
    name='documents'
)
