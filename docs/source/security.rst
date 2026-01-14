########
Security
########

.. warning::

    Deploying Kora on an open network can expose your application and data to various security risks, including unauthorized access and potential attacks. Acquire adequate knowledge in network security and follow best practices before making your Kora instance accessible beyond a trusted environment.

**********************************************
Authentication Failure Monitoring and fail2ban
**********************************************

Kora can optionally log failed authentication attempts in a format suitable for tools such as ``fail2ban`` (https://www.fail2ban.org/). When enabled, Kora writes failed login attempts to a dedicated log file. This feature is intended for deployments that are exposed to untrusted networks (for example, public-facing instances) and is **disabled by default**. Local-only or LAN-only deployments typically do not require this functionality.

Enabling failed authentication logging
======================================

Failed authentication logging is enabled by setting ``AUTHLOG_ENABLED`` to a :ref:`truthy value <bools>`.

.. code-block:: text

   AUTHLOG_ENABLED=1

Log format
==========

Each failed login attempt will produce a single log line in the following format:

.. code-block:: text

   <date-time> FAILED LOGIN user='<username>' client_ip=127.0.0.1

For example:

.. code-block:: text

    2026-01-13 10:11:12 FAILED LOGIN user='antani' client_ip=127.0.0.1

If the client IP address cannot be determined reliably (see below), the entry will look like this:

.. code-block:: text

   2026-01-13 10:11:12 FAILED LOGIN user='antani' client_ip=- proxy_ip=172.18.0.5 (missing or invalid X-Real-IP; fail2ban will not work)

Lines with ``client_ip=-`` are **intentionally not suitable for fail2ban** and should not be matched by any jail.

Client IP address handling
==========================

Kora does not attempt to infer client IP addresses from multiple headers or guess trusted networks.

The following strict rule is applied:

- Only the ``X-Real-IP`` HTTP header is accepted as a valid client IP
- If ``X-Real-IP`` is missing or invalid, no ban candidate IP is logged

For the time being, Kora intentionally does not fall back to ``REMOTE_ADDR`` and ignores ``X-Forwarded-For``, even if present. This design avoids a common and dangerous misconfiguration where fail2ban ends up banning the reverse proxy itself instead of the real client.

For this feature to work, it is therefore **required** that:

- Kora is deployed behind a reverse proxy (e.g. nginx)
- The proxy is correctly configured to forward ``X-Real-IP``

Log file location
=================

By default, failed authentication attempts are written to:

.. code-block:: text

   /var/log/kora/auth.log

The log path can be overridden using the environment variable:

.. code-block:: text

   AUTHLOG_FILE_PATH=/custom/path/auth.log

The log file is written using a file-based handler compatible with external log rotation tools.

Example configuration
=====================

Kora does not ship or manage fail2ban configuration. The following example is provided for reference only.

To allow fail2ban (or similar tools) running on the host system to access the authentication log, the log file or its parent directory must be bind-mounted from the container.

The recommended approach is to mount a directory by setting up a ``docker-compose.override.yml``:

.. code-block:: yaml

   services:
     web:
       environment:
         - AUTHLOG_ENABLED=true
         - AUTHLOG_FILE_PATH=/var/log/kora/auth.log
       volumes:
         - ./logs:/var/log/kora

Create ./logs/ on the host and ensure it is writable by the container. This allows the host to manage log rotation and permissions more easily.


``filter.d/kora-login.conf``

.. code-block:: conf

    [Definition]
    failregex   = ^\s*FAILED LOGIN user='.*' client_ip=<HOST>$
    ignoreregex =


``jail.d/kora-login.local``

.. code-block:: conf

    [kora-login]
    enabled = true
    filter = kora-login
    logpath = /absolute/path/to/your/kora-docker/logs/auth.log
    backend = polling
    maxretry = 3
    findtime = 600
    bantime = 3600
    action = iptables-multiport[name=kora-login, port="80,443", protocol=tcp]


Recommended basic ``nginx`` headers configuration:

.. code-block:: conf

    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-Proto $scheme;

Common misconfigurations
=======================

If fail2ban does not trigger as expected:

- Ensure ``AUTHLOG_ENABLED`` is set and applied
- Verify that nginx forwards ``X-Real-IP``
- Check that log lines contain ``client_ip=<address>`` and not ``client_ip=-``
- Ensure the fail2ban jail matches the exact log format
