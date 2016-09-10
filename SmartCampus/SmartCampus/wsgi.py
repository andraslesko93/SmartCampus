"""
WSGI config for SmartCampus project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os


import site
site.addsitedir('/smartcampus/myprojectenv/lib/python2.7/site-packages')
import sys
sys.path.append('/smartcampus/SmartCampus')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SmartCampus.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

