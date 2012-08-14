from .sets import THEME_ICONSETS, DEFAULT_THEME

def get_icon_name(icon):
    return THEME_ICONSETS[DEFAULT_THEME]['icons'][icon]


def get_sprite_name(icon):
    return THEME_ICONSETS[DEFAULT_THEME]['sprites'][icon]
