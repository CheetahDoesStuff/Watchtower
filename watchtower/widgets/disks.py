from pathlib import Path
import json
import subprocess
import psutil

from watchtower.widgets.section import Section
from watchtower.widgets.meter import Meter
from PyQt6.QtCore import QTimer


def disk_type(name):
    if name.startswith("nvme"):
        return "NVME"
    r = Path(f"/sys/block/{name}/queue/rotational").read_text().strip()
    return "HDD" if r == "1" else "SSD"


def physical_disks():
    out = subprocess.check_output(
        ["lsblk", "-b", "-o", "NAME,TYPE,SIZE", "--json"], text=True
    )
    disks = json.loads(out)["blockdevices"]
    real_disks = []

    for d in disks:
        if d["type"] != "disk":
            continue
        # ignore devices with 0 size
        if int(d.get("size", 0)) == 0:
            continue
        # ignore disks with no partitions
        if not d.get("children"):
            continue
        real_disks.append(d)

    return real_disks


class DiskSection(Section):
    def __init__(self):
        super().__init__("Storage")

        self.meters = {}

        for disk in physical_disks():
            name = disk["name"]
            label = disk_type(name)
            meter = Meter(f"{label}")
            self.meters[name] = meter
            self.addWidget(meter)

        timer = QTimer(self)
        timer.timeout.connect(self.update_meters)
        timer.start(500)

    def update_meters(self):
        usage = {}
        for p in psutil.disk_partitions(all=False):
            u = psutil.disk_usage(p.mountpoint)
            usage[p.device] = (u.used, u.total)

        for disk, meter in self.meters.items():
            used = total = 0
            for dev, (u, t) in usage.items():
                if dev.startswith(f"/dev/{disk}"):
                    used += u
                    total += t
            if total:
                meter.set(round(used / (total / 100)))
                GB = 1024**3
                meter.percentage.setText(
                    f"{round(used / GB, 1) if used / GB < 1000 else round(used / GB / 10244, 1)}GB / {round(total / GB, 1)}GB"
                )
