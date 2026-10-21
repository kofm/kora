from .appearance import normalize_appearance
from .version import __version__


def kora(request):
    appearance = normalize_appearance(request.session.get("appearance"))
    return {
        "kora_version": __version__,
        "appearance": appearance,
        "appearance_theme": "dark" if appearance == "dark" else "light",
    }
