from __future__ import absolute_import, unicode_literals

# Celery 애플리케이션을 import하여 Django가 이를 인식하도록 함
from .celery import app as celery_app

__all__ = ('celery_app',)
