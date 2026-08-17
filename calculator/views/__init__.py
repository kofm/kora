from .crop import CropDeleteView, CropSort, crop_detail
from .fieldbook import fieldbook_create, fieldbook_detail
from .observation import parameter_observation_create, trait_observation_create

__all__ = [
    "crop_detail",
    "CropDeleteView",
    "CropSort",
    "fieldbook_create",
    "fieldbook_detail",
    "trait_observation_create",
    "parameter_observation_create",
]
