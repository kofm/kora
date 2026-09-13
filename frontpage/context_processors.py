from .version import __version__


def kora(request):
    return {
        "kora_version": __version__,
    }
