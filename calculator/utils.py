from django.db.models.query import QuerySet

from calculator.models import Crop, CropParameter
from parameters.models import VarietalParameter


def get_available_params(queryset: QuerySet) -> set:
    available_params = {x["parameter__code"] for x in queryset}
    return available_params


def get_params(queryset: QuerySet, params_list: list) -> list:
    queryset = queryset.filter(parameter__code__in=params_list).distinct("parameter__code")
    return list(queryset)


def get_all_params(Model: CropParameter | VarietalParameter, **kwargs) -> QuerySet:
    return Model.objects.filter(**kwargs).values(
        "parameter",
        "parameter__code",
        "value",
        "parameter__measure_unit",
        "parameter__name",
    )


def get_crop_params_list(crop: Crop) -> list:
    """
    Return crop parameters, filling missing values from the crop's variety.
    """
    cropparams = get_all_params(CropParameter, crop=crop)
    found_cropparams = get_available_params(cropparams)
    found_varparams = set()
    params_list = list(cropparams)
    varparams = get_all_params(VarietalParameter, variety=crop.variety)
    found_varparams = get_available_params(varparams) - found_cropparams
    params_list += get_params(varparams, found_varparams)
    return sorted(params_list, key=lambda d: d["parameter__code"])


def generate_zigzag_pairs(xmax, ymax, block_width=2, start_corner="NW"):
    """
    Yield (x, y) pairs that cover a xmax × ymax grid in column–blocks of
    `block_width`, zig‑zagging through the grid.

    Coordinate system
    -----------------
    (1, 1)  →  north‑west corner
    x grows → east        (1 … xmax)
    y grows → south       (1 … ymax)

    Parameters
    ----------
    xmax, ymax : int
        Grid dimensions (1‑based indexing).
    block_width : int, optional
        Width of each vertical block of columns; default is 2.
    start_corner : {'NW', 'NE', 'SW', 'SE'}, optional
        Corner at which to begin the walk (case‑insensitive).
        Default is 'NW'.

    Yields
    ------
    (x, y) : tuple[int, int]
        Coordinates visited in the required order.
    """
    start_corner = start_corner.upper()
    if start_corner not in {"NW", "NE", "SW", "SE"}:
        raise ValueError("start_corner must be one of 'NW', 'NE', 'SW', 'SE'")

    west_start = start_corner[1] == "W"  # first block at the W edge?
    north_start = start_corner[0] == "N"  # first row at the N edge?

    n_blocks = (xmax + block_width - 1) // block_width
    # order in which we visit the column‑blocks
    block_indices = range(n_blocks) if west_start else range(n_blocks - 1, -1, -1)

    for step_idx, block in enumerate(block_indices):
        # Columns covered by the current block (always in ascending x)
        start_x = block * block_width + 1
        end_x = min(xmax, start_x + block_width - 1)
        xs = list(range(start_x, end_x + 1))

        # Alternate x direction inside each block
        reverse_x = (step_idx % 2 == 1) if west_start else (step_idx % 2 == 0)
        if reverse_x:
            xs.reverse()

        # Alternate y direction inside each block
        #  – If we start in the north, the **first** block goes south (ascending y)
        #  – If we start in the south, the **first** block goes north (descending y)
        ascending_y = (step_idx % 2 == 0) if north_start else (step_idx % 2 == 1)
        ys = range(1, ymax + 1) if ascending_y else range(ymax, 0, -1)

        for y in ys:
            for x in xs:
                yield (x, y)
