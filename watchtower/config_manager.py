import pathlib
import tomllib
import platformdirs
from loguru import logger as l


def _deep_merge(a, b):
    return {
        k: _deep_merge(a[k], b[k])
        if k in a and isinstance(a[k], dict) and isinstance(b[k], dict)
        else b.get(k, a.get(k))
        for k in a | b
    }


class ConfigManager:
    _config_path = (
        pathlib.Path(platformdirs.user_config_dir("Watchtower", "Cheetah"))
        / "config.toml"
    )

    _config_path.parent.mkdir(parents=True, exist_ok=True)
    _config_path.touch(exist_ok=True)

    _default_config = {
        "misc": {
            "default-sort": "ram",
            "default-theme": "Modern",
        }
    }

    l.info(f"Loading config from {_config_path}")

    _config = _deep_merge(
        _default_config, tomllib.loads(_config_path.read_text() or "")
    )

    @classmethod
    def get_config(cls):
        return cls._config
