from __future__ import absolute_import, unicode_literals

from mayan.apps.appearance.classes import Icon

icon_about = Icon(driver_name='fontawesome', symbol='info')
icon_add_all = Icon(
    driver_name='fontawesome-layers', data=[
        {'class': 'far fa-circle'},
        {'class': 'fas fa-plus', 'transform': 'shrink-6'}
    ]
)
icon_assign_remove_add = Icon(driver_name='fontawesome', symbol='plus')
icon_assign_remove_remove = Icon(driver_name='fontawesome', symbol='minus')
icon_confirm_form_submit = Icon(driver_name='fontawesome', symbol='check')
icon_confirm_form_cancel = Icon(driver_name='fontawesome', symbol='times')
icon_current_user_locale_profile_details = Icon(
    driver_name='fontawesome', symbol='globe'
)
icon_current_user_locale_profile_edit = Icon(
    driver_name='fontawesome', symbol='globe'
)
icon_documentation = Icon(driver_name='fontawesome', symbol='book')
icon_fail = Icon(
    driver_name='fontawesome', symbol='times'
)
icon_forum = Icon(
    driver_name='fontawesome', symbol='life-ring'
)
icon_license = Icon(
    driver_name='fontawesome', symbol='certificate'
)
icon_menu_about = Icon(
    driver_name='fontawesome', symbol='info'
)
icon_menu_user = Icon(
    driver_name='fontawesome', symbol='user-circle'
)
icon_object_errors = Icon(
    driver_name='fontawesome', symbol='exclamation-triangle'
)
icon_object_error_list = Icon(
    driver_name='fontawesome', symbol='exclamation-triangle'
)
icon_object_error_list_clear = Icon(
    driver_name='fontawesome', symbol='times'
)
icon_ok = Icon(
    driver_name='fontawesome', symbol='check'
)
icon_remove_all = Icon(
    driver_name='fontawesome-layers', data=[
        {'class': 'far fa-circle'},
        {'class': 'fas fa-minus', 'transform': 'shrink-6'}
    ]
)
icon_setup = Icon(
    driver_name='fontawesome', symbol='cog'
)
icon_social_facebook = Icon(
    driver_name='fontawesomecss', css_classes='fab fa-facebook'
)
icon_social_instagram = Icon(
    driver_name='fontawesomecss', css_classes='fab fa-instagram'
)
icon_social_paypal = Icon(
    driver_name='fontawesomecss', css_classes='fab fa-paypal'
)
icon_social_twitter = Icon(
    driver_name='fontawesomecss', css_classes='fab fa-twitter'
)
icon_sort_down = Icon(driver_name='fontawesome', symbol='sort-down')
icon_sort_up = Icon(driver_name='fontawesome', symbol='sort-up')
icon_source_code = Icon(driver_name='fontawesome', symbol='code-branch')
icon_support = Icon(
    driver_name='fontawesome', symbol='phone'
)
icon_tools = Icon(
    driver_name='fontawesome', symbol='wrench'
)
icon_wiki = Icon(driver_name='fontawesome', symbol='book')
