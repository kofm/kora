Configuration
=============

Environment Variables
---------------------

Many *kora* settings can be customized using `environment variables
<https://en.wikipedia.org/wiki/Environment_variable>`_. You can define
these variables in your environment (for example, in a `.env` file) to
modify *kora*'s core behavior.

Example of an environment configuration file: ::

    SECRET_KEY='foo'
    POSTGRES_PASSWORD='postgres'
    NGINX_PORT=8002
    ALLOWED_HOSTS='web'
    CSRF_TRUSTED_ORIGINS='http://localhost:8002/* http://web'

The `kora-docker` bundle includes a `env.example` template you can
copy and use with default options or modify to suit your configuration
preferences. There can be different types of setting:

- **Booleans**. For boolean variables (true/false or yes/no), the
  following values will enable the setting: `true`, `yes`, `1`, or
  `on`. Any other value will be treated as `false`, and disable the
  feature. For example:

::

   MY_SETTING='true'

- **Lists**. Lists are used to supply multiple values to a single setting
  and should be specified as space-separated values. For example:

::

   MY_OTHER_SETTING='value1 value2 value3'


- **Strings**. Used for plain text values. Strings should generally be
  enclosed in single quotes to preserve spaces and special
  characters. For example:

::

    STRING_SETTING='My Application'

- **Numbers**. Generally, these values are specified without quotes for
  clarity, but quoting is allowed. For example:

::

    NUMBER_SETTING=8080
    ANOTHER_NUMBER_SETTING=0.75

Environment variable values should generally be quoted using single
quotes (see examples) to prevent interpretation by the shell,
especially when values contain spaces, wildcards, or special
characters.

When to use quotes:

- **Lists**: Values are space-separated within the quotes.
- **Booleans**: Quotes are optional but recommended for clarity.
- **Strings with special characters**: Such as `*`, `&`, `?`, etc.

When in doubt, use quotes.

.. note::

    The following code snippets show the default values.

Site Visibility
~~~~~~~~~~~~~~~


.. option:: PUBLIC

    Boolean. Determines whether accessing your *kora* installation
    requires a password. By default (False), the application restricts
    access to logged-in users with a username and password.When set to
    `true`, the following sections will be accessible **read-only** by
    anyone:

    - Plants > Species, Varieties, and Protections

    - Describe > Descriptions, Protocols, and Entities

::

    PUBLIC='false'

Auditing Interaction
~~~~~~~~~~~~~~~~~~~~

(Provided by the third-party `django-easy-audit
<https://github.com/soynatan/django-easy-audit>`_ module). The
following environment variables control auditing features that log
`CRUD
<https://en.wikipedia.org/wiki/Create,_read,_update_and_delete>`_
operations, user access, and page views. Useful for detailed tracking
and auditing of user activity within your *kora* instance.

.. option:: DJANGO_EASY_AUDIT_WATCH_AUTH_EVENTS

    Boolean. Determines whether to log user authentication events such as
    logins, logouts, and failed login attempts.

::

   DJANGO_EASY_AUDIT_WATCH_AUTH_EVENTS='false'  

   
.. option:: DJANGO_EASY_AUDIT_WATCH_REQUEST_EVENTS

	    Boolean. Determines whether to log URL requests made by users, i.e.,
	    which pages they visit.

::

   DJANGO_EASY_AUDIT_WATCH_REQUEST_EVENTS='false'

.. option:: DJANGO_EASY_AUDIT_WATCH_MODEL_EVENTS

	    Boolean. Determines whether to log when objects are created, updated,
	    or deleted.

::

    DJANGO_EASY_AUDIT_WATCH_MODEL_EVENTS='true'

.. option:: DJANGO_EASY_AUDIT_UNREGISTERED_CLASSES_EXTRA

	    List. Specifies models whose CRUD operations should not be
	    logged.

::

   DJANGO_EASY_AUDIT_UNREGISTERED_CLASSES_EXTRA='auth.group'

Django-Related Settings
~~~~~~~~~~~~~~~~~~~~~~~

.. option:: DEV

	    Boolean. Indicates whether the application is running in
	    development mode.  When set to `false` (the default), the
	    application runs in production mode, which disables
	    debugging features and enables performance improvements.
	    Use `true` only during development or troubleshooting.

::

   DEV='false'

.. option:: SECRET_KEY

	    String. A secret key used by Django for security purposes
	    such as sessions and password resets.  This key should be
	    unique and kept private to protect your application.

::

   SECRET_KEY='foo'

.. option:: ALLOWED_HOSTS

    List. Specifies the host/domain names that Django considers valid for
    serving the application. Requests with a Host header not matching an
    entry in this list will be blocked. This helps prevent HTTP Host
    header attacks and ensures your application only responds to expected
    hosts.

    In the default containerized setup, `'web'` corresponds to the service
    name defined within the Docker network, allowing internal routing and
    communication between containers.

    When deploying *kora* in different environments, such as on a local
    machine, network server, or cloud instance, it is important to adjust
    `ALLOWED_HOSTS` accordingly. 

    Failing to set `ALLOWED_HOSTS` properly may result in "Bad Request
    (400)" errors when accessing the application from outside the default
    container network.


::

   ALLOWED_HOSTS='web'
   # Example configuration for a local network deployment
   ALLOWED_HOSTS='web localhost 192.168.1.50'

.. option:: CSRF_TRUSTED_ORIGINS

    List of URLs. These are trusted addresses allowed to submit forms or
    requests to Django, helping protect against certain web attacks. The
    defaults cover typical local and container access.

    When deploying *kora* in a local area network (LAN) using the
    containerized *kora-docker* bundle, the setting `CSRF_TRUSTED_ORIGINS`
    must be edited to specify the IP of the host machine to make requests
    without triggering CSRF protection errors.

::

   CSRF_TRUSTED_ORIGINS='http://localhost:8002/* http://web'

   # Example configuration for a typical LAN install might look like this:
   CSRF_TRUSTED_ORIGINS='http://localhost:8002/* http://web http://192.168.1.50:8002'


`kora-docker` Settings
~~~~~~~~~~~~~~~~~~~~~~~~~~

These settings control aspects of the *kora-docker* bundle, which packages *kora* in a containerized environment for easy deployment and management.

.. option:: POSTGRES_PASSWORD

	    String. Password for the PostgreSQL database administrator.
	    The default `'postgres'` is adequate for local development, but you should change it for production.

::

   POSTGRES_PASSWORD='postgres'

.. option:: NGINX_PORT

	    Number. The port on your computer where the web server listens for incoming requests.

	    Default `8002` is a sensible choice that avoids conflicts with common services.

::

   NGINX_PORT=8002

.. option:: DB_HOST

	    String. The name of the database host or service.
	    In Docker setups, `'db'` usually refers to the database container and works without changes.

::

   DB_HOST='db'

.. option:: DB_PORT

    Number. The port on which the PostgreSQL database is listening inside the container.

    Port `5432` is the standard PostgreSQL port and typically does not need to be changed.
    Because this port is not exposed outside the containers, using the default keeps things secure.

::

   DB_PORT=5432

.. note::

   The provided default values are recommended for most users and setups.
   Docker Compose creates a private network allowing containers to communicate
   using these defaults without exposing services unnecessarily.
   This helps keep your system safe while simplifying configuration.
