from ipaddress import ip_address


def _valid_ip(s: str) -> bool:
    try:
        ip_address(s)
        return True
    except ValueError:
        return False


def get_client_ip(request):
    real_ip = request.META.get("HTTP_X_REAL_IP", "").strip()
    if real_ip and _valid_ip(real_ip):
        return real_ip
    return None
