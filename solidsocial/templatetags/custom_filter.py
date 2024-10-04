from django import template
from django.template.defaultfilters import stringfilter
from urllib.parse import urlparse 
from solidsocial.models import Preview
from solidsocial.serializers.preview import PreviewSerializer
import re
import markdown as md
from datetime import datetime
import json

register = template.Library()


# Use Variable as key for dict
@register.filter
def keyvalue(dict, key):    
    if key in dict:
        return dict[key]
    return None

@register.filter
def sublist(list, key):
    if list:
        if key in list[0]:
            return [ a[key] for a in list ]
    return None

@register.filter
def countwithout(list, exclude):
    if list:
        if exclude in list:
            list.remove(exclude)
        return len(list)
    return None

@register.filter
@stringfilter
def pod_to_user(url):
    return f"@{urlparse(url).netloc}"

@register.filter
@stringfilter
def dateformat(date):
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z").strftime("%d.%m.%Y - %H:%M")

@register.filter
def multiline(data):
    datalist = json.loads(data)
    html = '<ul>'
    for el in datalist:
        html += f"<li>{el}</li>"
    html += '</ul>'

    return html

trust_groups = [
        (-1, "t-warn", "Post was rated untrustworthy"),
        (2, "t-attantion", "Post is highly unlikely to be trustworthy"),
        (4, "t-below", "Post may not be trustworthy"),
        (5, "t-neutral", "Post was rated neutral"),
        (7, "t-mid", "Post was rated trustworthy"),
        (9, "t-high", "Post was rated very trustworthy"),
        ]

@register.filter
def trust_to_class(tvalue):
    match = min(trust_groups, key=lambda x:abs(x[0]-tvalue))
    html = f'<div data-tooltip="{match[2]}" class="trust-indicator tooltip-right"><i class="fa-solid fa-circle fa-2xs {match[1]}"></i></div>'
    return html
    #return f'{match[1]}" data-tooltip="{match[2]}'
    #return f'{match[1]}'

@register.filter
@stringfilter
def md_to_html(content):
    content = re.sub(r"(^| )(https?:\/\/.*?\..*?)($| )", r"\1[Link](\2)\3", content, flags=re.DOTALL)
    html = md.markdown(content, extensions=['markdown.extensions.extra'])
    if link:=re.search(r"\[.*?\]\((.*?)\)", content):
        if (preview:=Preview.objects.filter(url = link.group(1))).exists():
            preview_serializer = PreviewSerializer(preview.first())
            preview = f'''
            <div class="link-preview">
                <a href="{ preview_serializer.data['url'] }"><img class="preview-image" alt="Link Vorschaubild" src="{ preview_serializer.data['image'] }"></a>
                <div class="preview-name"><a href="{ preview_serializer.data['url'] }">{ preview_serializer.data['title'] }</a></div>
                <div class="preview-description">{ preview_serializer.data['description'] }</div>
            </div>
            '''
            # remove content if it's only the like - used for shared links
            if content == re.search(r"(\[.*?\]\(.*?\))",content).group(1):
                html = ""
            return f'{preview}<div class="post-text">{html}</div>'
    return f'<div class="post-text">{html}</div>'


