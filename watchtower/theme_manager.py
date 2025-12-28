import weakref
import platformdirs
import pathlib
import tomllib
from loguru import logger as l

_DEFAULT_THEMES = """["Modern"]
bg = "#191c24"
fg-1 = "#1F232D"
fg-2 = "#242935"
fg-3 = "#2A2F3C"
text = "hsl(0, 0%, 75%)"
text-header = "hsl(0, 0%, 85%)"
border = "rgb(46, 50, 66)"
section-text = "hsl(0, 0%, 50%)"
button-bg = "rgb(44, 50, 63)"
button-kill-bg = "#a32626"
bar-meter = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(230,120,120), stop:1 rgb(231,89,236))"

["Modern (Light)"]
bg = "#d8dced"
fg-1 = "#c8cbdb"
fg-2 = "#babdcc"
fg-3 = "#9aaebf"
text = "hsl(0, 0%, 25%)"
text-header = "hsl(0, 0%, 15%)"
border = "#9699a8"
section-text = "hsl(0, 0%, 50%)"
button-bg = "#babdcc"
button-kill-bg = "#e63c3c"
bar-meter = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(230,120,120), stop:1 rgb(231,89,236))"
"""


class ThemeManager:
    _theme = None
    _listeners = []

    _themes_path = (
        pathlib.Path(platformdirs.user_config_dir("Watchtower", "Cheetah"))
        / "themes.toml"
    )
    _themes_path.parent.mkdir(parents=True, exist_ok=True)
    _themes_path.touch(exist_ok=True)
    l.info(f"Loading themes from {_themes_path}")

    if not _themes_path.exists() or _themes_path.stat().st_size == 0:
        _themes_path.write_text(_DEFAULT_THEMES)

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
