import re


def smart_truncate_string(text, min_length=10, suffix="..."):
    """If the `text` is more than `min_length` characters long, it
    will be cut at the next word-boundary and `suffix` will be
    appended."""
    pattern = rf"^(.{{{min_length - 1},}}?\S)\s.*"
    return re.sub(pattern, r"\1" + suffix, text)
