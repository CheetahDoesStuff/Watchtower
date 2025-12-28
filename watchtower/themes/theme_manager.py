import weakref


class ThemeManager:
    _theme = None
    _listeners = []

    @classmethod
    def set_theme(cls, name):
        cls._theme = name
        for ref in cls._listeners[:]:
            fn = ref()
            if fn is None:
                cls._listeners.remove(ref)
            else:
                fn()

    @classmethod
    def get_theme(cls):
        from watchtower.themes.themes import themes

        return themes[cls._theme]

    @classmethod
    def get_theme_names(cls):
        from watchtower.themes.themes import themes

        return themes.keys()

    @classmethod
    def register(cls, fn):
        if hasattr(fn, "__self__") and fn.__self__ is not None:
            cls._listeners.append(weakref.WeakMethod(fn))
        else:
            cls._listeners.append(weakref.ref(fn))
