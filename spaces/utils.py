from django.db.models import Max
from spaces.models import Area

def get_max_order(location) -> int:
    existing_areas = Area.objects.filter(location=location)
    if not existing_areas:
        return 1
    else:
        current_max = existing_areas.aggregate(max_order=Max('order'))['max_order']
        return current_max + 1
    
