import weakref
import platformdirs
import pathlib
import tomllib
from loguru import logger as l


class ThemeManager:
    _theme = None
    _listeners = []

    _themes_path = (
        pathlib.Path(platformdirs.user_config_dir("Watchtower", "Cheetah"))
        / "themes.toml"
    )
    l.info(f"Loading themes from {_themes_path}")

    with open(_themes_path, "rb") as f:
        _themes = tomllib.load(f)

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
        return cls._themes[cls._theme]  # ty:ignore[invalid-argument-type]

    @classmethod
    def get_theme_names(cls):
        return cls._themes.keys()

    @classmethod
    def register(cls, fn):
        if hasattr(fn, "__self__") and fn.__self__ is not None:
            cls._listeners.append(weakref.WeakMethod(fn))
        else:
            cls._listeners.append(weakref.ref(fn))
