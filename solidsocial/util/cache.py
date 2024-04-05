from solidsocial.serializers.author import AuthorSerializer
from solidsocial.serializers.reaction import ReactionSerializer
from solidsocial.serializers.post import PostSerializer
from solidsocial.models import Author, Post, Reaction, Message
from solidsocial.util.model import get_me
from dssd.settings import SOLID_SETTINGS, DEMO
from solidsocial.solidclient.social import init_social_containers

def get_own_id():
    try:
        return Author.objects.get(url=SOLID_SETTINGS['wid']).id
    except:
       return None 

def get_me():
    try:
        me = Author.objects.get(url=SOLID_SETTINGS['wid'])
        return {'id': me.id, 'photo': f"/media/{me.photo}", 'url': me.url}
    except:
        init_social_containers()
def check_cache_message(url):
    try:
        pk = Message.objects.get(url=url).pk
    except:
        pk = None
    return pk


def get_feed(fstart=0, fend=50, updatedate=None):
    """
    Return all the sorted data needed to render a Feed
    """


    # only get posts for Feed update
    if updatedate:
        posts = Post.objects.filter(pdate__gte=updatedate)
    else:
        posts = Post.objects.all()
    postserializer = PostSerializer(posts, many=True)
    posts_data = list(postserializer.data)
    posts_data = sorted(posts_data, key=lambda k: k['cdate'], reverse=True)
    
    # Remove own posts for Demo use
    if DEMO:
        posts_data = [p for p in posts_data if p['author'] != get_me()['id']]

    # Slice for regular Feed update
    if not updatedate:
        s = slice(fstart,fend)
        posts_data = posts_data[s]

    # Get all original Posts, that posts in the Feed responded to
    responded = []
    for rp in [ p for p in posts_data if p['response'] ]:
        responded.append(rp['response'])
        rp['response'] = PostSerializer(Post.objects.get(pk=rp['response'])).data

    # Create a dict of all authors, sortet by id
    authors = Author.objects.all()
    authorserializer = AuthorSerializer(authors, many=True)
    authors_data = {}
    for a in authorserializer.data:
        index = a['id']
        authors_data[index] = a

    # Get all reactions for Posts in the Feed
    reactions = Reaction.objects.filter(targetpost__in=[ p['id'] for p in posts_data ])
    reactionserializer = ReactionSerializer(reactions, many=True)
    reactions_data = {}
    for a in reactionserializer.data:
        index = a['targetpost']
        if index not in reactions_data:
            reactions_data[index] = []
        reactions_data[index].append(a)

    return posts_data, authors_data, reactions_data, responded


