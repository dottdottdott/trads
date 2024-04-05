from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from solidsocial.serializers.post import PostSerializer
from solidsocial.models import Post
from solidsocial.solidclient.social import init_solid_client

class PostAPI(APIView):
    def get(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        post_serializer = PostSerializer(post)
        return Response(post_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        sc = init_solid_client(True)
        post = Post.objects.get(pk=pk)
        sc.delete(post.url)
        post.delete()
        return Response("deleted", status=status.HTTP_200_OK)
