from dssd.settings import SOLID_SETTINGS
from solidsocial.models import Author

def get_own_id():
    return Author.objects.get(url=SOLID_SETTINGS['wid']).id

def get_me():
     me = Author.objects.get(url=SOLID_SETTINGS['wid'])
     return {'id': me.id, 'photo': f"/media/{me.photo}", 'url': me.url}
