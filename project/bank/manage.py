#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""

    # There are several configuration files in this project.
    # At the moment:
    # - config.settings.debug_settings
    # - config.settings.product_settings
    #       * product_settings requires " path('__debug__/', include('debug_toolbar.urls')) " to be removed from urlspatterns in config.urls
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.debug_settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
