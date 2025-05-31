from textual.theme import Theme
import meine.app as app

def get_theme_colors():

    _theme: Theme = app.app.current_theme

    return {
        "primary": _theme.primary,
        "secondary": _theme.secondary,
        "warning": _theme.warning,
        "error": _theme.error,
        "success": _theme.success,
        "accent": _theme.accent,
        "foreground": _theme.foreground,
        "background": _theme.background,
        "surface": _theme.surface,
        "panel": _theme.panel,
        "boost": _theme.boost,
    }
