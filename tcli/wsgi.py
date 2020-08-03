"""
WSGI config for tcli project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

#from my_project import MyWSGIApp

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tcli.settings')

application = get_wsgi_application()

#application = MyWSGIApp()
#application = WhiteNoise(application, root='../../static')
#application.add_files('../../inventory/static/, prefix='more-files/')
#application.add_files('../../locations/static/, prefix='more-files/')
#application.add_files('../../equipment/static/, prefix='more-files/')
