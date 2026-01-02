from pathlib import Path
from loguru import logger as l

Desktop_file = """\
[Desktop Entry]
Type=Application
Name=Watchtower
GenericName=Task Manager & System Monitor
Comment=Task Manager & System Monitor
Exec=watchtower
Terminal=false
Categories=Utility;
"""


def install():
    path = Path.home() / ".local/share/applications/watchtower.desktop"
    path.parent.mkdir(parents=True, exist_ok=True)
    l.info(f"Checking if desktop entry already exists at {path}")

    if path.exists():
        l.info(
            "Desktop entry already exists, if you want to overwrite it please delete the file. Aborting..."
        )
        return
    else:
        l.info(f"Creating desktop entry at {path}")
        path.write_text(Desktop_file)
