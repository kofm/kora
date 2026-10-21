APPEARANCES = ("auto", "light", "dark")


def normalize_appearance(value):
    return value if value in APPEARANCES else "auto"
