from solidsocial.util.cache import get_me
from dssd.settings import DEMO

def add_static_info(request):
    return {
            'me': get_me(),
            'demo': DEMO
            }
