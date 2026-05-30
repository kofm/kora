def format_decimal(value, places=2):
    if value is None:
        return "-"

    return f"{value:.{places}f}".rstrip("0").rstrip(".")
