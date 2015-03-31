
from django.conf import settings


def toggles(request):
    return {
        'TOGGLE': settings.TOGGLE,
    }
