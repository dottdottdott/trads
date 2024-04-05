from os.path import basename
from django.template.loader import render_to_string
import requests
from solidsocial.serializers.message import MessageSerializer
from solidsocial.serializers.author import AuthorSerializer
from solidsocial.serializers.reaction import ReactionSerializer
from solidsocial.serializers.post import PostSerializer
from solidsocial.serializers.vcard import VcardSerializer
from solidsocial.solidclient.client import SolidClient
from solidsocial.serializers.preview import PreviewSerializer
from solidsocial.models import Author, Preview, Vcard, Post, Message
from dssd.settings import SOLID_SETTINGS, DEMO
from urllib.parse import urlparse
from django.core.files.images import ImageFile
from io import BytesIO
from solidsocial.util.preview import generate_preview
import re
import json
from datetime import datetime
from django.template.loader import render_to_string
from solidsocial.util.helpers import get_base_url
from urllib.parse import urlparse
import threading


def check_cache_author(url):
    """
    Check if specific author is in cache and return author id
    """
    try:
        pk = Author.objects.get(url=url).pk
    except:
        pk = None
    return pk


def check_cache_post(url):
    """
    Check if a specifc post is allready in cache and return post id
    """
    try:
        pk = Post.objects.get(url=url).pk
    except:
        pk = None
    return pk


def check_cache_vcard(author):
    """
    Check if specific author allready has vcard data in cache and return true or false
    """
    return True if author in [a.author for a in list(Vcard.objects.all())] else False

def init_solid_client(login=False):
    """ 
    Initialize the solid client
    Optionally using the solid credentials provided in the django settings
    """
    if login:
        return SolidClient(SOLID_SETTINGS['idp'], SOLID_SETTINGS['user'], True, SOLID_SETTINGS['password'])
    else:
        return SolidClient()

def init_social_containers():
    """
    Create all the containers neccessary to use solid social demo in users pod
    All the read and write privalages are set accordingly
    """
    ubase = get_base_url(SOLID_SETTINGS['wid'])
    sc = init_solid_client(True)

    if not sc.check_exists(sf:=f"{ubase}/social/"):
        sc.new_folder(sf)
        publicacl = render_to_string("blocks/aclfolder.ttl", {"public": True})
        sc.new_folder(f"{sf}posts/")
        sc.put(f"{sf}posts/.acl", publicacl, 'text/turtle')
        sc.new_folder(f"{sf}reactions/")
        sc.put(f"{sf}reactions/.acl", publicacl, 'text/turtle')
        sc.new_folder(f"{sf}media/")
        sc.put(f"{sf}media/.acl", publicacl, 'text/turtle')
        inboxacl = render_to_string("blocks/aclfolder.ttl", {"inbox": True})
        sc.new_folder(f"{sf}inbox/")
        sc.put(f"{sf}inbox/.acl", inboxacl, 'text/turtle')
        sc.new_folder(f"{sf}outbox/")
    print("getting user")
    get_author(sc, SOLID_SETTINGS['wid'], False)



def ser_vcard(url, resp, inc_author=True):
    data = {}
    if inc_author:
        data['author'] = Author.objects.filter(url=url).first().pk
    if 'hasTelephone' in resp:
        #data['telephone'] = ''.join[a.split(':')[1] for a in data['hasTelephone'] if a.startswith('tel:')]
        data['telephone'] = ''.join([a.split(':')[1] for a in resp['hasTelephone'] if a.startswith('tel:')])
    if 'hasEmail' in resp:
        data['email'] = ''.join([a.split(':')[1] for a in resp['hasEmail'] if a.startswith('mailto:')])
    for f in ['bday', 'role', 'note']:
        if f in resp:
            data[f] = resp[f]
    if 'hasAddress' in resp:
        data['address'] = json.dumps(resp['hasAddress'])
    print(data)
    serializer = VcardSerializer(data=data)
    return serializer

# ACL
def create_priv_acl(url):
    """
    Create a private acl file for a given file on a pod
    Grant only access to all followees to the given url
    """
    furls = [get_base_url(a) for a in list(Author.objects.filter(followed=True).values_list('url', flat=True))]
    filename = urlparse(url).path
    fileacl = render_to_string("blocks/aclfile.ttl", {"file": filename, "webid": SOLID_SETTINGS['wid'], "authors": furls})
    sc = init_solid_client(True)
    sc.put(f"{url}.acl", fileacl, 'text/turtle')


def background_update(author_id=None):
    """
    Start background task to update cache
    """
    t = threading.Thread(target=update_cache, args=[author_id], daemon=True)
    t.start()

def update_cache(author_id=None):
    """
    Updates cache containt
    author_id will limit it to only one author, otherwiese all followees
    """
    authors = []
    if author_id:
        try:
            author = Author.objects.get(pk=author_id)
            #if author.last_check >= last:
            #    return Response("Nothing to Update", status=status.HTTP_204_NO_CONTENT)
            authors.append({'last': author.last_check, 'url': author.url, 'id': author.pk})
        except:
            return "Author not found"
    else:
        for author in Author.objects.filter(followed=True):
            authors.append({'last': author.last_check, 'url': author.url, 'id': author.pk})
    sc = init_solid_client(True)
    for author in authors:
        url = f"{get_base_url(author['url'])}/social/posts/"
        update_posts(sc, url, author['id'])
    updated = Post.objects.filter(url__in=[a['url'] for a in authors])
    serializer = PostSerializer(updated)


def update_posts(sc, url, id):
    """
    Update cache containt for one specific author
    """
    files = sc.get_foldercontent(url)
    for f in files:
                #if timezone.make_aware(datetime.fromtimestamp(f['date'])) > author['last']:
        get_post(sc, f['url'], id)
    Author.objects.filter(pk=id).update(last_check=datetime.now())

def get_post(sc, rurl,  author_id=None):
    """
    Add a specific post to the cache
    """
    data = {}
    if (postpk:= check_cache_post(rurl)) is None:
        if author_id:
            data['author'] = author_id
        else:
            if  (authorpk:= check_cache_author(uurl:=f"{rurl.replace(urlparse(rurl).path, '/profile/card#me')}")) is None:
                data['author'] = get_author(sc, uurl)['id']
            else:
                data['author'] = authorpk
        resp = sc.get_post(rurl)
        if not resp:
            return None
        data['cdate'] = datetime.fromisoformat(resp['meta']['date'])
        data['url'] = rurl
        data['checksum'] = resp['checksum']
        if resp['content']:
            data['content'] = resp['content']
            blanklinks = re.sub(r"(^| )(https?:\/\/.*?\..*?)($| )", r"\1[Link](\2) ", data['content'], flags=re.DOTALL)
            if link:=re.search(r"\[.*?\]\((.*?)\)", blanklinks):
                get_preview(link.group(1))
        if "media" in resp['meta']:
            media =  ImageFile(BytesIO(sc.get_media(resp['meta']['media'])), basename(urlparse(resp['meta']['media']).path))
            resp['meta'].pop('media')
            data['media'] = media
        if "response" in resp['meta']:
            respost = get_post(sc, resp['meta']['response'])
            data['response'] = respost['id']
        if "signature" in resp:
            data['signature'] = resp['signature']
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            print(serializer.errors)
            return None
    else:
        serializer = PostSerializer(Post.objects.get(pk=postpk))
        return serializer.data
        

def get_vcard(sc, url, inc_author=True, serialize=True):
    """
    Add vcard information for an author to the cache
    """
    if not url.endswith('/profile/card#me'):
        url = f"{url}/profile/card#me"
    resp = sc.get_vcard(url)
    if serialize:
        return ser_vcard(url, resp, inc_author=inc_author)
    else:
        return resp


def get_preview(url):
    """
    Create a link preview, store in cache and return it
    """
    try:
        if Preview.objects.filter(url = url).exists():
            preview_serializer = PreviewSerializer(Preview.objects.filter(url=url).first())
        else:
            preview_data = generate_preview(url)
            preview_data['image'] = ImageFile(BytesIO(requests.get(preview_data['image']).content), basename(urlparse(preview_data['image']).path))
            preview_serializer = PreviewSerializer(data = preview_data)
            if preview_serializer.is_valid():
                preview_serializer.save()
            else:
                return None
        return preview_serializer.data
    except:
        return None


def get_author(sc, url, recursive=True):
    """
    Add a specific author to cache
    """

    # change url to apropriate format
    if not url.endswith('/profile/card#me'):
        url = f"{url}/profile/card#me"
    if url.startswith('@'):
        url = url.replace('@', 'https://')
    if not url.startswith('http'):
        url = f"https://{url}"

    # load vcard date (needed for name, key, picture)
    vcard = sc.get_vcard(url)
    author = {'name': vcard['fn'], 'url': url, 'last_check': datetime.fromtimestamp(0)}

    # get profice picture if availible
    if 'hasPhoto' in vcard:
        photo =  ImageFile(BytesIO(sc.get_media(vcard['hasPhoto'])), basename(urlparse(vcard['hasPhoto']).path))
        author['photo'] = photo

    # get pub key if availible
    if 'hasKey' in vcard:
        author['key'] = str(sc.get_media(vcard['hasKey']))

    author_serializer = AuthorSerializer(data=author)
    if author_serializer.is_valid():
        author_serializer.save()
        vcard_serializer = ser_vcard(url, vcard)
        if vcard_serializer.is_valid():
            vcard_serializer.save()
        else:
            print(vcard_serializer.errors)
        
        # if author was added directly also load author posts and reactions
        if not recursive:
            update_posts(sc, f"{get_base_url(author['url'])}/social/posts/", author_serializer.data['id'])
        return author_serializer.data
    else:
        print(author_serializer.errors)
        return None

def get_message(sc, rurl, received=False, recepient=None):
    if (msgpk:= check_cache_message(rurl)) is None:
        resp = sc.get_post(rurl)
        if not resp:
            return None
        data = {
                'cdate': datetime.fromisoformat(resp['meta']['date']), 
                'content': resp['content'],
                'url': rurl,
                }
        if received:
            data['correspondent'] = Author.objects.get(url=resp['meta']['from']).id
            data['received'] = True
        else:
            data['correspondant'] = recepient
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            print(serializer.errors)
        return None
    else:
        if received:
            return None
        return Message.objects.get(pk=msgpk)

def new_reaction(post, author, signature=None):
    sc = init_solid_client(True)
    if pk:= check_cache_post(post):
        post = Post.objects.get(pk=pk)
        post_creator = post.author
    else:
        return None
    content = f"{author} liked {post.url}"
    data={
        'targetpost': pk, 
        'author': check_cache_author(author), 
        'content': content, 
        }
    if not DEMO:
        resp = sc.new_message(post_creator.url, content )
        if not resp['status'] == 201:
            return None
        data['url']=resp['url']
    else:
        data['url']=f"DEMO-{content}"

    serializer = ReactionSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    else:
        print(serializer.errors)
    return None
