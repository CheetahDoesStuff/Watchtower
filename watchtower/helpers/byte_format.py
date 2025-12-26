def format_bytes(bytes):
    units = ("B", "KB", "MB", "GB", "TB", "PB")
    i = 0
    while bytes >= 1024 and i < len(units) - 1:
        bytes /= 1024
        i += 1

    return f"{round(bytes, 1)} {units[i]}"
