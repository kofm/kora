Security
========

.. warning::

    Deploying Kora on an open network can expose your application and underlying infrastructure to various security risks, including unauthorized access and potential attacks. Acquire adequate knowledge in network security and follow best practices before making your Kora instance accessible beyond a trusted environment.

Authentication Failure Monitoring with fail2ban
-----------------------------------------------

To enhance security, you can use **fail2ban**, an intrusion prevention software framework that monitors log files for repeated failed login attempts and blocks the offending IP addresses through firewall rules.

Failed login attempts in Kora are logged in the file ``kora_auth.log`` found at ``/app/kora_auth.log`` within the web service container. Entries follow this format:


.. code-block:: text

   WARNING FAILED LOGIN for user '<username>' from 127.0.0.1

For example:


.. code-block:: text

    [2023-04-14 13:28:01,791] WARNING FAILED LOGIN for user 'antani' from 127.0.0.1

fail2ban can be configured to parse the Kora authentication log by monitoring this specific pattern string to automatically detect and block repeated failed login attempts. For more detailed information about fail2ban, visit the official website: https://www.fail2ban.org/

To enable external monitoring of ``kora_auth.log`` by fail2ban or similar tools on the host machine, update your ``docker-compose.yml`` file to bind mount the log file. Add the following volume mapping to the ``web`` service configuration:

.. code-block:: yaml

   services:
     web:
       # ... existing configuration ...
       volumes:
         - static_files:/var/www/static
         - ./kora_auth.log:/app/kora_auth.log

Make sure the file ``kora_auth.log`` exists on the host at the root of your project directory or adjust the path accordingly.
