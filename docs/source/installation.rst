Installing and Updating
#######################

This section provides platform-specific guidance to install Kora using Docker. 

Quick start - Windows
=====================

Requirements
------------

- Docker Desktop
  (https://docs.docker.com/desktop/install/windows-install/)
- Git for Windows (https://git-scm.com/download/win)

Installation
------------

1. From the Start menu open ``Git Bash`` application
2. In the Git Bash window paste the following lines (using the right
   click menu or the key combination Shift+Ins), then press Enter:

.. code:: bash

   cd C:/ && \
   git clone --depth 1 --recursive --shallow-submodule https://github.com/kofm/kora-docker && \
   cd kora-docker && \
   cp env.example .env && \
   docker-compose up -d

3. After the whole process complete (it should take few minutes), you
   should be able to reach Kora via the following address in your
   browser of choice: http://localhost:8002
  
   Remember to :ref:`create a user <access-control>` to be able to log in.

Quick start - Linux
===================

Requirements
------------


You will need an up to date version of ``git``, ``docker``, and
``docker-compose``.

Installation
------------


1. Clone the repo in your favourite directory (e.g. ~/Documents)

.. code:: bash

   git clone --depth 1 --recursive --shallow-submodule https://github.com/kofm/kora-docker 

2. CD into directory

.. code:: bash

   cd kora-docker

3. Copy the provided ``env.example`` example file as ``.env`` and
   personalize its contents with your favourite editor

.. code:: bash

   cp env.example .env

4. Start the containers.

.. code:: bash

   docker-compose up

That’s it!

After the containers start and you see the Kora ASCII banner, simply type the following in your browesr ``http://localhost:8002``

Enjoy!

.. _access-control:

Main Account Creation
=====================

By default, access to Kora is password protected. Before accessing your new installation, you must create an administrator account using the provided utility `ko` (select menu option #6).

It is possible to allow certain sections of the application to be viewed without user authentication. This can be configured by setting the :option:`PUBLIC` environment variable.

Updating
========

When a new version is released, update the application using the convenience script `ko`. Open a shell (Git Bash on Windows) and navigate to the installation directory (assuming Windows installation on `C:/`):

.. code:: bash

   cd C:/kora-docker
   ./ko

From the menu, select **option 1** to update the application. The script will stop the container, update the application, and restart the containers automatically.

FAQ
===

Windows - I can access the app locally, but not from another machine on the same network.
-----------------------------------------------------------------------------------------

If your app works on the host machine at ``http://localhost:<PORT>`` or
``http://<HOST-IP>:<PORT>``, but isn’t reachable from another device on
the same LAN, it’s possible that Windows Firewall is blocking inbound
traffic.

Fix: Allow the port through Windows Firewall
--------------------------------------------


.. warning::

   Allowing inbound traffic through Windows Firewall exposes the host machine to network connections on the specified port. This can introduce security risks if not managed properly. Ensure you have adequate networking knowledge before modifying firewall settings and exposing services to your local network.


On the host machine, open PowerShell as **Administrator** and run:

.. code:: powershell

   New-NetFirewallRule -DisplayName "Allow Docker App Port" `
     -Direction Inbound `
     -Protocol TCP `
     -LocalPort <PORT> `
     -Action Allow

Replace ``<PORT>`` with the one your app uses, e.g. if using the default (8002):

.. code:: powershell

   New-NetFirewallRule -DisplayName "Allow Docker App Port" `
     -Direction Inbound `
     -Protocol TCP `
     -LocalPort 8002 `
     -Action Allow

Also Check:
-----------

- Make sure the host’s network profile is set to **Private** (not Public) in ``Settings > Network & Internet > [Your Connection]``.
