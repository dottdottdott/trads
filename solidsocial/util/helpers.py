from urllib.parse import urlparse, urldefrag

def get_base_url(url):
    rurl = f"{url.replace(urlparse(url).path, '')}"
    return(urldefrag(rurl)[0])

def get_wid(url):
    return f"{get_base_url(url)}/profile/card#me"


