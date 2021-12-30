from mayan.apps.appearance.classes import Icon

icon_otp_detail = Icon(driver_name='fontawesome', symbol='shield-alt')
icon_otp_disable = Icon(
    driver_name='fontawesome-dual', primary_symbol='shield-alt',
    secondary_symbol='minus'
)
icon_otp_enable = Icon(
    driver_name='fontawesome-dual', primary_symbol='shield-alt',
    secondary_symbol='plus'
)
