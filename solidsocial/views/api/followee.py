from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from solidsocial.models import Author
from solidsocial.solidclient.social import init_solid_client, update_posts, get_base_url

class FolloweeAPI(APIView):
    def get(self, request, pk, format=None):
        author = Author.objects.get(pk=pk)
        return Response(author.followed)

    def put(self, request, pk, format=None):
        if 'follow' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        author = Author.objects.filter(pk=pk).update(followed=request.data['follow'])
        if request.data['follow']:
            author = Author.objects.get(pk=pk)
            sc = init_solid_client(True)
            update_posts(sc, f"{get_base_url(author.url)}/social/posts/", pk)
        return Response("updated", status=status.HTTP_200_OK)
