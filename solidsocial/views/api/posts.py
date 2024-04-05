from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from solidsocial.serializers.author import AuthorSerializer
from solidsocial.serializers.post import PostSerializer
from solidsocial.models import Author, Post
from dssd.settings import SOLID_SETTINGS, DEMO
from solidsocial.util.cache import get_feed
import re
import uuid
from solidsocial.solidclient.social import create_priv_acl, init_solid_client, get_preview

class PostsAPI(APIView):
    parser_classes = (MultiPartParser,)

    def get(self, request, format=None):
        # Get all Post of specific author
        if 'author' in request.GET:
            try:
                posts = Post.objects.filter(author=request.GET.get('author'))
            except:
                return Response("Author not found", status=status.HTTP_400_BAD_REQUEST)

        # Create a feed
        elif 'feed' in request.GET:
            start = 0 if 'start' not in request.GET else request.GET.get('start')
            posts_data, authors_data, reactions_data, responded_data = get_feed(int(start), int(request.GET.get('feed')))
            html = render_to_string("blocks/feedblock.html", {
                "posts": posts_data, 
                "authors": authors_data,
                "reactions": reactions_data,
                "responded": responded_data,
                })
            return Response(html)
        else:
            posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if not request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        media = None if "media" not in request.data else [request.data['media'], request.data['media'].content_type]
        meta = {} if "meta" not in request.data else request.data['meta']
        if "response" in request.data:
            ref = Post.objects.get(pk=request.data['response'])
            meta['response'] = ref.url
        sign = False if "sign" not in request.data else True
        #if not DEMO:
        sc = init_solid_client(True)
        newpost = sc.new_post(request.data['content'] if 'content' in request.data else None, meta, media, sign)
        #else:
        #    newpost = { 'date': datetime.now().isoformat(' ', 'seconds'),
        #            'url': uuid.uuid4().hex}
        data = {
                'cdate': newpost['date'],
                'url': newpost['url'],
                'author': Author.objects.filter(url=SOLID_SETTINGS['wid'])[0].pk,
                }
        if 'content' in request.data:
            data['content'] = request.data['content']
        if "media" in request.data:
            request.data['media'].seek(0)
            media =  request.data['media']
            data['media'] = media
        if 'signature' in newpost:
            data['signature'] = newpost['signature']
        if 'response' in request.data:
            data['response'] = ref.id
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            if 'content' in data:
                blanklinks = re.sub(r"(^| )(https?:\/\/.*?\..*?)($| )", r"\1[Link](\2)\3", data['content'])
                if link:=re.search(r"\[.*?\]\((.*?)\)", blanklinks):
                    get_preview(link.group(1))
        else:
            print(serializer.errors)
        if "html" in request.data:
            author_serializer = AuthorSerializer(Author.objects.get(pk=serializer.data['author']))
            newpost['html'] = render_to_string("blocks/feedpost.html", {"post": serializer.data, "author": author_serializer.data, "reactions": { }})
        if "priv" in request.data:
            create_priv_acl(data['url'])
        return Response(newpost)
