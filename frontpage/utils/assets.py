from django.templatetags.static import static

from frontpage.layouts import BaseLayout

ASSET_TYPES = ["css", "js", "hs"]


def _ensure_assets(context: dict) -> dict:
    b = context.setdefault("template_assets", {k: [] for k in ASSET_TYPES})
    for k in ASSET_TYPES:
        b.setdefault(k, [])
    return b


def add_asset(context: dict, asset_type: str, path: str):
    """Register an asset URL in a template context.

    Add an asset `path` of a supported type to the template `context`,
    ensuring that the asset is resolved to an absolute URL and
    registered only once.  Assets collected in the context are
    automatically included by the base template (see
    `frontpage/base.html`).

    Parameters
    ----------
    context : dict
        Template rendering context. The internal assets structure is
        created if it does not already exist.
    asset_type : str
        Asset category key (e.g. `"css"`, `"js"`). Must be one of
        `ASSET_TYPES`.
    path : str
        Static asset path or absolute URL. Relative paths are resolved
        using Django’s `static()` helper. Absolute URLs (starting with
        `/` or containing `"://"`) are used as-is. Duplicate assets
        are ignored.

    Raises
    ------
    KeyError
        If `asset_type` is not a supported asset type.

    """
    if asset_type not in ASSET_TYPES:
        raise KeyError(f"Unknown asset type: '{asset_type}'")

    assets = _ensure_assets(context)
    url = path if (path.startswith("/") or "://" in path) else static(path)
    lst = assets[asset_type]
    if url not in lst:
        lst.append(url)


def add_layout_assets(context, layout: BaseLayout):
    """Register all assets required by a `BaseLayout` class in the template context.

    Collect all assets declared by the given `layout` instance and
    register them into the template `context`, for automatic inclusion
    in the base template (see `frontpage/base.html`).

    Parameters
    ----------
    context : dict
        Template context to which the layout assets are added.
    layout : BaseLayout
        Layout instance.

    """
    for asset_type, assets in layout.assets.items():
        for asset in assets:
            add_asset(context, asset_type, asset)


def require_js(context, path):
    add_asset(context, "js", path)


def require_hs(context, path):
    add_asset(context, "hs", path)


def require_css(context, path):
    add_asset(context, "css", path)
