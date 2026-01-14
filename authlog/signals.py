import logging

from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver

from .ip import get_client_ip

logger = logging.getLogger("authlog.failed_login")


@receiver(user_login_failed)
def log_failed_login(sender, credentials, request, **kwargs):
    if request is None:
        return

    credentials = credentials or {}
    username = credentials.get("username") or "<unknown>"

    client_ip = get_client_ip(request)
    proxy_ip = request.META.get("REMOTE_ADDR")

    if client_ip:
        logger.warning("FAILED LOGIN user=%r client_ip=%s", username, client_ip)
    else:
        logger.warning(
            "FAILED LOGIN user=%r client_ip=- proxy_ip=%s (missing or invalid X-Real-IP; fail2ban will not work)",
            username,
            proxy_ip,
        )
