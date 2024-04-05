import hashlib
import markdown
import uuid
from datetime import datetime
from rdflib import Namespace, Graph, URIRef
from urllib.parse import urlparse, urldefrag
from .solid.auth import Auth
from .solid.solid_api import SolidAPI
from solidsocial.util.pgp import sign_message, check_signature, check_signed

def get_base_url(url):
    rurl = f"{url.replace(urlparse(url).path, '')}"
    return(urldefrag(rurl)[0])

def get_wid(url):
    return f"{get_base_url(url)}/profile/card#me"

def _is_empty(generator):
    for element in generator:
        return False
    return True

def _get_uuid():
    return uuid.uuid4().hex

def _get_currentdate():
    return datetime.now().isoformat(' ', 'seconds')

def _get_netloc(wid):
    if wid.endswith('/profile/card#me'):
        return wid.replace('/profile/card#me', '')

def _striptrail(string):
    if string.endswith('\n'):
        return _striptrail(string[:-1])
    return string


class SolidClient:
    def __init__(self, idp=None, username=None, login=False, password=None):
        self.auth = Auth()
        self.api = SolidAPI(self.auth)
        if login:
            self.auth.login(f"https://{idp}", username, password)
            self.baseurl = f"https://{username}.{idp}"

    def get(self, location):
        return self.api.get(location)

    def delete(self, location):
        return self.api.delete(location)

    def put(self, location, content, mime):
        return self.api.put_file(location, content, mime)

    def check_exists(self, url):
        return self.api.item_exists(url)
    
    def new_folder(self, path):
        return self.api.create_folder(path) 

    def new_post(self, message, meta=None, media=None, sign=False):
        if not self.auth.is_login:
            return "Not logged in"
        postid = _get_uuid()
        date = _get_currentdate()
        metablock = f"date: {date}"
        if meta:
            for k in meta:
                metablock += f"\n{k}: meta{k}"
        if media:
            fname = f"{_get_uuid()}.{media[1].split('/')[1]}"
            self.new_media(mediaurl:=f"{self.baseurl}/social/media/{fname}", media[0], media[1])
            metablock += f"\nmedia: {mediaurl}"
        md = f"---\n{metablock}\n---\n{message}"
        if sign:
            signature = sign_message(md)
            md += f"\n{signature}"
        resp = self.api.put_file(
                url:=f"{self.baseurl}/social/posts/{postid}", 
                md,
                'text/markdown'
                )
        rdata = {'response': resp.text, 'date': date, 'url': url}
        if media:
            rdata['mediaurl'] = mediaurl
        if sign:
            rdata['signature'] = signature
        return rdata
    
    def new_message(self, recipient, content, meta=None):
        uuid = _get_uuid()
        target=f"{_get_netloc(recipient)}/social/inbox/{uuid}"
        metablock = f"date: {_get_currentdate()}"
        if meta:
            for k in meta:
                metablock += f"\n{k}: meta{k}"
        resp = self.api.put_file(
                target, 
                f"---\n{metablock}\n---\n{content}",
                'text/markdown'
                )
        return {'text': resp.text, 'status': resp.status_code, 'url': target, 'uuid': uuid}

    def new_media(self, location, filep, mtype):
        resp = self.put(location, filep, mtype)
        return resp

    def get_foldercontent(self, location):
        resp = self.api.read_folder(location)
        return [{'url': f.url, 'date': f.date, 'size': f.size} for f in resp.files]

    def get_post(self, location):
        try:
            resp = self.get(location)
        except:
            return None
        if sig:=check_signed(resp.text):
            valid, text = check_signature(resp.text, get_wid(location))
            if not valid:
                return None
        else:
            text = resp.text
        md = markdown.Markdown(extensions=['meta'])
        md.convert(text)
        postdata = {
                'content': _striptrail('\n'.join(md.lines)), 
                'meta': {key: md.Meta[key][0] for key in md.Meta},
                'checksum': hashlib.md5(resp.text.encode("utf-8")).hexdigest()
                }
        if sig:
            postdata['signature'] = valid
            postdata['fullmsg'] = text
        return postdata

    def get_posts(self, locations):
        return [ self.get_post(l) for l in locations ]

    def get_media(self, location):
        return self.get(location).content

    def get_vcard(self, location):
        VCARD = Namespace('http://www.w3.org/2006/vcard/ns#')
        url = location if location.endswith("/card#me") else f"{location}/profile/card#me"
        resp = self.get(url)
        g = Graph().parse(data=resp.text, publicID=url, format='turtle')
        this = URIRef(url)
        elements = ['hasTelephone', 'hasPhoto', 'fn', 'bday', 'role', 'hasEmail', 'note', 'hasAddress', 'hasKey']
        card = {}
        for e in elements:
            if not _is_empty(g.objects(this, VCARD[e])):
                val = next(g.objects(this, VCARD[e]))
                if type(val) is URIRef and not _is_empty(g.objects(val)):
                    card[e] = [str(i) for i in g.objects(val)]
                else:
                    card[e] = str(val)
        return card
