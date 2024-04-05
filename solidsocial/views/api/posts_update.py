from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from solidsocial.serializers.post import PostSerializer
from solidsocial.models import Author, Post
from solidsocial.solidclient.social import init_solid_client, get_base_url, update_posts

class PostsUpdateAPI(APIView):
    def get(self, request, format=None):
        if 'last' not in request.GET:
            return Response("Last Update DateTime required", status=status.HTTP_400_BAD_REQUEST)
        last = datetime.fromtimestamp(int(request.GET.get('last')))
        update_limit = datetime.now()-timedelta(minutes=5)
        if last > update_limit:
            return Response("Update Limit of 5min not reached yet", status=status.HTTP_425_TOO_EARLY)
        authors = []
        if 'author_id' in request.GET:
            try:
                author = Author.objects.get(pk=request.GET.get('author_id'))
                #if author.last_check >= last:
                #    return Response("Nothing to Update", status=status.HTTP_204_NO_CONTENT)
                authors.append({'last': author.last_check, 'url': author.url, 'id': author.pk})
            except:
                return Response("Author not found", status=status.HTTP_400_BAD_REQUEST)
        else:
            for author in Author.objects.all():
                #if author.last_check >= last:
                authors.append({'last': author.last_check, 'url': author.url, 'id': author.pk})
        sc = init_solid_client(True)
        print(authors)
        for author in authors:
            url = f"{get_base_url(author['url'])}/social/posts/"
            update_posts(sc, url, author['id'])
        updated = Post.objects.filter(url__in=[a['url'] for a in authors])
        serializer = PostSerializer(updated)
        return Response(serializer.data, status=status.HTTP_200_OK)
